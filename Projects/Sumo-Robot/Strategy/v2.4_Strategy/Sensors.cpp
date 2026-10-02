#include <Arduino.h>
#include "Hardware.h"
#include "Sensors.h"
#include "Map.h"

// ============================================================
// OPPONENT SENSOR PIPELINE — confirm-count debounce, not median
// ============================================================
struct ChannelState
{
    int pin;
    int sensorIndex; // -1 left, 0 center, +1 right — matches Map.h's whichSensor convention
    int raw;
    int strongCount;  // consecutive samples >= STRONG_THRESHOLD
    int presentCount; // consecutive samples >= WEAK_THRESHOLD (strong samples count too)
    int absentCount;  // consecutive samples <  WEAK_THRESHOLD
    bool detected;
    bool near;
};

static ChannelState ch[3]; // 0=left, 1=center, 2=right
static unsigned long lastSampleMs = 0;

// Median of ADC_OVERSAMPLE_N reads. Dummy read first: the ADC sample cap still holds the previous channel.
static int readFiltered(int pin)
{
    (void)analogRead(pin);
    int buf[ADC_OVERSAMPLE_MAX];
    for (int i = 0; i < ADC_OVERSAMPLE_N; i++)
    {
        int v = analogRead(pin);
        int j = i - 1;
        while (j >= 0 && buf[j] > v)
        {
            buf[j + 1] = buf[j];
            j--;
        }
        buf[j + 1] = v; // insertion sort as we go
    }
    return buf[ADC_OVERSAMPLE_N / 2];
}

static void resetChannel(ChannelState &c, int pin, int sensorIndex)
{
    c.pin = pin;
    c.sensorIndex = sensorIndex;
    c.raw = readFiltered(pin);
    c.strongCount = 0;
    c.presentCount = 0;
    c.absentCount = 0;
    c.detected = false;
    c.near = false;
}

static void updateChannel(ChannelState &c)
{
    c.raw = readFiltered(c.pin);
    bool strong = (c.raw >= STRONG_THRESHOLD);
    bool present = (c.raw >= WEAK_THRESHOLD);

    c.strongCount = strong ? c.strongCount + 1 : 0;
    if (present)
    {
        c.absentCount = 0;
        if (c.presentCount < 1000) c.presentCount++;
    }
    else
    {
        c.presentCount = 0;
        if (c.absentCount < 1000) c.absentCount++;
    }

    if (present && !strong && isPhantomDetection(c.sensorIndex, c.raw))
    { // weak-band only; strong readings are never gated
        c.strongCount = 0;
        c.presentCount = 0;
        c.detected = false;
    }
    else if (c.strongCount >= STRONG_CONFIRM_SAMPLES || c.presentCount >= WEAK_CONFIRM_SAMPLES)
    {
        c.detected = true;
    }
    else if (c.absentCount >= CLEAR_CONFIRM_SAMPLES)
    {
        c.detected = false; // a single noisy dip no longer drops a real target
    }

    if (c.detected && c.raw >= NEAR_THRESHOLD)
        c.near = true;
    if (!c.detected)
        c.near = false;
}

void initSensors()
{
    analogReadResolution(SENSOR_ADC_BITS); // VERIFY: Serial.print a saturated reading, confirm it tops out near 1023 not 4095

    pinMode(OPPONENT_LEFT, INPUT);
    pinMode(OPPONENT_CENTER, INPUT);
    pinMode(OPPONENT_RIGHT, INPUT);
    pinMode(EDGE_FRONT, INPUT);
    pinMode(EDGE_BACK, INPUT);

    primeOpponentSensors();
}

void primeOpponentSensors()
{
    resetChannel(ch[0], OPPONENT_LEFT, -1);
    resetChannel(ch[1], OPPONENT_CENTER, 0);
    resetChannel(ch[2], OPPONENT_RIGHT, +1);
    lastSampleMs = millis();
}

void updateOpponentSensors()
{
    if (millis() - lastSampleMs < SENSOR_SAMPLE_INTERVAL_MS)
        return;
    lastSampleMs = millis();
    for (int i = 0; i < 3; i++)
        updateChannel(ch[i]);
}

OpponentReadings getOpponentReadings()
{
    OpponentReadings r;
    r.left = ch[0].raw;
    r.center = ch[1].raw;
    r.right = ch[2].raw;
    return r;
}

OpponentDetection getOpponentDetection()
{
    OpponentDetection d;
    d.left = ch[0].detected;
    d.leftNear = ch[0].near;
    d.center = ch[1].detected;
    d.centerNear = ch[1].near;
    d.right = ch[2].detected;
    d.rightNear = ch[2].near;
    return d;
}

bool anyOpponentDetected(const OpponentDetection &d)
{
    return d.left || d.center || d.right;
}

bool anyContact(const OpponentDetection &d)
{
    OpponentReadings r = getOpponentReadings();
    bool leftContact = d.leftNear && r.left >= CONTACT_BAND_LOW && r.left <= CONTACT_BAND_HIGH;
    bool centerContact = d.centerNear && r.center >= CONTACT_BAND_LOW && r.center <= CONTACT_BAND_HIGH;
    bool rightContact = d.rightNear && r.right >= CONTACT_BAND_LOW && r.right <= CONTACT_BAND_HIGH;
    return leftContact || centerContact || rightContact;
}

float estimateFarRangeCm(int rawAdc)
{
    // Placeholder 2-point fit: (10cm -> 650), (80cm -> 100). Linear in ADC domain, NOT physically accurate —
    // replace with the real 8-point table. Only meaningful for rawAdc in roughly [100, 650].
    const float d1 = 10.0f, v1 = 650.0f;
    const float d2 = 80.0f, v2 = 100.0f;
    float clamped = constrain((float)rawAdc, v2, v1);
    return d1 + (clamped - v1) * (d2 - d1) / (v2 - v1);
}

// ============================================================
// EDGE SENSORS — unchanged v4 double-read confirm
// ============================================================
static int edgeWhiteState = EDGE_WHITE_STATE;

void calibrateEdgePolarity()
{
    int f0 = digitalRead(EDGE_FRONT), b0 = digitalRead(EDGE_BACK);
    bool stable = true;
    unsigned long t = millis();
    while (millis() - t < EDGE_CAL_MS)
        if (digitalRead(EDGE_FRONT) != f0 || digitalRead(EDGE_BACK) != b0)
            stable = false;
    if (stable && f0 == b0) // both sensors agree on black: white is the opposite state
        edgeWhiteState = (f0 == HIGH) ? LOW : HIGH;
    // otherwise keep the EDGE_WHITE_STATE fallback
}

static EdgeReadings readEdgesOnce()
{
    EdgeReadings e;
    e.front = (digitalRead(EDGE_FRONT) == edgeWhiteState);
    e.back = (digitalRead(EDGE_BACK) == edgeWhiteState);
    return e;
}

EdgeReadings readEdgeSensors()
{
    EdgeReadings first = readEdgesOnce();
    if (!first.front && !first.back)
        return first;

    delayMicroseconds(200);
    EdgeReadings second = readEdgesOnce();
    first.front = first.front && second.front;
    first.back = first.back && second.back;
    return first;
}

bool anyEdgeDetected(const EdgeReadings &e)
{
    return e.front || e.back;
}