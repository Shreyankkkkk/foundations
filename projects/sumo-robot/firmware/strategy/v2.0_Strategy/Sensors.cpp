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
    int strongCount;
    int weakCount;
    bool detected;
    bool near;
};

static ChannelState ch[3]; // 0=left, 1=center, 2=right
static unsigned long lastSampleMs = 0;

static void resetChannel(ChannelState &c, int pin, int sensorIndex)
{
    c.pin = pin;
    c.sensorIndex = sensorIndex;
    c.raw = analogRead(pin);
    c.strongCount = 0;
    c.weakCount = 0;
    c.detected = false;
    c.near = false;
}

static void updateChannel(ChannelState &c)
{
    c.raw = analogRead(c.pin);

    if (c.raw >= STRONG_THRESHOLD)
    {
        c.strongCount++;
        c.weakCount = 0;
        if (c.strongCount >= STRONG_CONFIRM_SAMPLES)
            c.detected = true;
    }
    else if (c.raw >= WEAK_THRESHOLD)
    {
        if (isPhantomDetection(c.sensorIndex, c.raw))
        {
            c.weakCount = 0;
            c.strongCount = 0;
            c.detected = false;
        }
        else
        {
            c.weakCount++;
            c.strongCount = 0;
            if (c.weakCount >= WEAK_CONFIRM_SAMPLES)
                c.detected = true;
        }
    }
    else
    {
        c.strongCount = 0;
        c.weakCount = 0;
        c.detected = false;
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
static EdgeReadings readEdgesOnce()
{
    EdgeReadings e;
    e.front = (digitalRead(EDGE_FRONT) == EDGE_WHITE_STATE);
    e.back = (digitalRead(EDGE_BACK) == EDGE_WHITE_STATE);
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