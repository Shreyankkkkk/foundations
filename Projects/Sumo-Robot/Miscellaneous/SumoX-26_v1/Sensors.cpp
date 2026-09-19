// ============================================================================
// SumoX-26 — Sensors.cpp
// ----------------------------------------------------------------------------
// The actual sensor-reading detail lives here. Nothing outside this file
// should ever call analogRead/digitalRead on a sensor pin directly.
//
// Two things about the opponent filter that are easy to get wrong:
//
//  1. Sampling is gated to SENSOR_SAMPLE_INTERVAL_MS. The GP2Y0A21 only
//     refreshes its output every ~38 ms. Reading it in a tight loop returns
//     the same held value over and over, so a buffer filled at loop speed
//     contains five copies of one sample and filters nothing.
//
//  2. The filter takes the MEDIAN, not the mean. The Sharp's typical failure
//     is one wildly wrong sample. A mean spreads that error across the whole
//     window; a median throws it away completely.
// ============================================================================

#include <Arduino.h>
#include "Hardware.h"
#include "Sensors.h"

static int frontLeftBuffer[SENSOR_SAMPLES];
static int frontRightBuffer[SENSOR_SAMPLES];
static int leftBuffer[SENSOR_SAMPLES];
static int rightBuffer[SENSOR_SAMPLES];
static int bufferIndex = 0;
static unsigned long lastOpponentSample = 0;

// The filtered result is only recomputed when a new sample lands, so calling
// readOpponentSensors() every loop iteration costs almost nothing.
static OpponentReadings cachedReadings = {0, 0, 0, 0};

// Edge confirmation state: a corner only changes its reported value after
// EDGE_CONFIRM_READS consecutive identical raw reads.
static bool edgeConfirmed[4]  = {false, false, false, false};
static bool edgeLastRaw[4]    = {false, false, false, false};
static int  edgeAgreeCount[4] = {0, 0, 0, 0};

static bool serialDebugReady = false;

// ---------------------------------------------------------------------------

// Applies one channel's offset and gain from Hardware.h, so that comparisons
// between two different physical sensors are meaningful.
static int calibrateReading(int raw, int offset, int gain) {
    long calibrated = (long)(raw + offset) * (long)gain / 1000L;
    return (int)constrain(calibrated, 0L, (long)ADC_MAX);
}

// Insertion sort on a copy, then take the middle element. SENSOR_SAMPLES is
// small and odd, so this is both cheap and unambiguous.
static int medianBuffer(const int *buffer) {
    int sorted[SENSOR_SAMPLES];
    for (int i = 0; i < SENSOR_SAMPLES; i++) {
        sorted[i] = buffer[i];
    }
    for (int i = 1; i < SENSOR_SAMPLES; i++) {
        int value = sorted[i];
        int j = i - 1;
        while (j >= 0 && sorted[j] > value) {
            sorted[j + 1] = sorted[j];
            j--;
        }
        sorted[j + 1] = value;
    }
    return sorted[SENSOR_SAMPLES / 2];
}

static void recomputeCachedReadings() {
    cachedReadings.frontLeft  = calibrateReading(
        medianBuffer(frontLeftBuffer),  OPPONENT_OFFSET_FL,    OPPONENT_GAIN_FL);
    cachedReadings.frontRight = calibrateReading(
        medianBuffer(frontRightBuffer), OPPONENT_OFFSET_FR,    OPPONENT_GAIN_FR);
    cachedReadings.left       = calibrateReading(
        medianBuffer(leftBuffer),       OPPONENT_OFFSET_LEFT,  OPPONENT_GAIN_LEFT);
    cachedReadings.right      = calibrateReading(
        medianBuffer(rightBuffer),      OPPONENT_OFFSET_RIGHT, OPPONENT_GAIN_RIGHT);
}

// ---------------------------------------------------------------------------

void initSensors() {
    // AVR boards are fixed at 10 bits and do not provide this function, so it
    // is guarded. On the UNO Q this sets the ADC to match ADC_MAX.
#if !defined(ARDUINO_ARCH_AVR)
    analogReadResolution(ADC_RESOLUTION_BITS);
#endif

    pinMode(OPPONENT_FRONT_LEFT,  INPUT);
    pinMode(OPPONENT_FRONT_RIGHT, INPUT);
    pinMode(OPPONENT_LEFT,        INPUT);
    pinMode(OPPONENT_RIGHT,       INPUT);

    pinMode(EDGE_FRONT_LEFT,  INPUT);
    pinMode(EDGE_FRONT_RIGHT, INPUT);
    pinMode(EDGE_BACK_LEFT,   INPUT);
    pinMode(EDGE_BACK_RIGHT,  INPUT);

    // Pre-fill every buffer with a real reading so the first median is not
    // skewed toward zero. Spaced out so they are genuinely distinct samples
    // rather than five copies of one held output.
    bufferIndex = 0;
    for (int i = 0; i < SENSOR_SAMPLES; i++) {
        frontLeftBuffer[i]  = analogRead(OPPONENT_FRONT_LEFT);
        frontRightBuffer[i] = analogRead(OPPONENT_FRONT_RIGHT);
        leftBuffer[i]       = analogRead(OPPONENT_LEFT);
        rightBuffer[i]      = analogRead(OPPONENT_RIGHT);
        delay(SENSOR_SAMPLE_INTERVAL_MS);
    }
    lastOpponentSample = millis();
    recomputeCachedReadings();

    // Prime the edge confirmation state from the current pin values so the
    // first real read does not have to wait for agreement.
    EdgeReadings raw = readEdgeSensorsRaw();
    bool initial[4] = {raw.frontLeft, raw.frontRight, raw.backLeft, raw.backRight};
    for (int i = 0; i < 4; i++) {
        edgeConfirmed[i]  = initial[i];
        edgeLastRaw[i]    = initial[i];
        edgeAgreeCount[i] = EDGE_CONFIRM_READS;
    }
}

void initSensorDebug() {
    Serial.begin(115200);
    // Wait up to a second for a terminal. On boards with native USB serial,
    // prints issued before the host attaches are simply thrown away, which is
    // why bench output can look like the sensors are dead.
    unsigned long start = millis();
    while (!Serial && (millis() - start) < 1000) {
        ;
    }
    serialDebugReady = true;
}

void printSensorDebug(OpponentReadings readings, EdgeReadings edges) {
    if (!serialDebugReady) return;

    Serial.print(F("OPP [FL FR L R]: "));
    Serial.print(readings.frontLeft);  Serial.print(' ');
    Serial.print(readings.frontRight); Serial.print(' ');
    Serial.print(readings.left);       Serial.print(' ');
    Serial.print(readings.right);

    Serial.print(F(" | EDGE [FL FR BL BR]: "));
    Serial.print(edges.frontLeft  ? F("WHITE") : F("black")); Serial.print(' ');
    Serial.print(edges.frontRight ? F("WHITE") : F("black")); Serial.print(' ');
    Serial.print(edges.backLeft   ? F("WHITE") : F("black")); Serial.print(' ');
    Serial.println(edges.backRight ? F("WHITE") : F("black"));
}

OpponentReadings readOpponentSensors() {
    unsigned long now = millis();
    if (now - lastOpponentSample >= SENSOR_SAMPLE_INTERVAL_MS) {
        frontLeftBuffer[bufferIndex]  = analogRead(OPPONENT_FRONT_LEFT);
        frontRightBuffer[bufferIndex] = analogRead(OPPONENT_FRONT_RIGHT);
        leftBuffer[bufferIndex]       = analogRead(OPPONENT_LEFT);
        rightBuffer[bufferIndex]      = analogRead(OPPONENT_RIGHT);
        bufferIndex = (bufferIndex + 1) % SENSOR_SAMPLES;
        lastOpponentSample = now;
        recomputeCachedReadings();
    }
    return cachedReadings;
}

EdgeReadings readEdgeSensorsRaw() {
    EdgeReadings edges;
    edges.frontLeft  = (digitalRead(EDGE_FRONT_LEFT)  == EDGE_WHITE_STATE_FL);
    edges.frontRight = (digitalRead(EDGE_FRONT_RIGHT) == EDGE_WHITE_STATE_FR);
    edges.backLeft   = (digitalRead(EDGE_BACK_LEFT)   == EDGE_WHITE_STATE_BL);
    edges.backRight  = (digitalRead(EDGE_BACK_RIGHT)  == EDGE_WHITE_STATE_BR);
    return edges;
}

EdgeReadings readEdgeSensors() {
    EdgeReadings raw = readEdgeSensorsRaw();
    bool current[4] = {raw.frontLeft, raw.frontRight, raw.backLeft, raw.backRight};

    for (int i = 0; i < 4; i++) {
        if (current[i] == edgeLastRaw[i]) {
            if (edgeAgreeCount[i] < EDGE_CONFIRM_READS) {
                edgeAgreeCount[i]++;
            }
        } else {
            edgeLastRaw[i]    = current[i];
            edgeAgreeCount[i] = 1;
        }

        if (edgeAgreeCount[i] >= EDGE_CONFIRM_READS) {
            edgeConfirmed[i] = edgeLastRaw[i];
        }
    }

    EdgeReadings edges;
    edges.frontLeft  = edgeConfirmed[0];
    edges.frontRight = edgeConfirmed[1];
    edges.backLeft   = edgeConfirmed[2];
    edges.backRight  = edgeConfirmed[3];
    return edges;
}

bool isOpponentDetected(int reading) {
    return reading > DIST_THRESHOLD;
}

bool anyEdgeDetected(EdgeReadings edges) {
    return edges.frontLeft || edges.frontRight || edges.backLeft || edges.backRight;
}
