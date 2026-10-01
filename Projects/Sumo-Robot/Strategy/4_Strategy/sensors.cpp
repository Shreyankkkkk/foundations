#include <Arduino.h>
#include "Hardware.h"
#include "Sensors.h"

static int leftBuffer[SENSOR_SAMPLE];
static int centerBuffer[SENSOR_SAMPLE];
static int rightBuffer[SENSOR_SAMPLE];

static int bufferIndex = 0;
static unsigned long lastOpponentSample = 0;

// Median of one sensor's own rolling buffer
static int medianOf(const int *buffer) {
    int sorted[SENSOR_SAMPLE];
    for (int i = 0; i < SENSOR_SAMPLE; i++) sorted[i] = buffer[i];
    for (int i = 1; i < SENSOR_SAMPLE; i++) {
        int value = sorted[i];
        int j = i - 1;
        while (j >= 0 && sorted[j] > value) {
            sorted[j + 1] = sorted[j];
            j--;
        }
        sorted[j + 1] = value;
    }
    return sorted[SENSOR_SAMPLE / 2];
}

void initSensors() {
    analogReadResolution(10); // 0-1023; if compiler rejects, remove this line and use default 10-bit resolution

    pinMode(OPPONENT_LEFT, INPUT);
    pinMode(OPPONENT_CENTER, INPUT);
    pinMode(OPPONENT_RIGHT, INPUT);

    pinMode(EDGE_FRONT, INPUT);
    pinMode(EDGE_BACK, INPUT);

    primeOpponentSensors();
}

void primeOpponentSensors() {
    for (int i = 0; i < SENSOR_SAMPLE; i++) {
        leftBuffer[i] = analogRead(OPPONENT_LEFT);
        centerBuffer[i] = analogRead(OPPONENT_CENTER);
        rightBuffer[i] = analogRead(OPPONENT_RIGHT);    
    }
    bufferIndex = 0;
    lastOpponentSample = millis();
}

OpponentReadings readOpponentSensors() {
    if (millis() - lastOpponentSample >= SENSOR_SAMPLE_INTERVAL_MS) {
        leftBuffer[bufferIndex] = analogRead(OPPONENT_LEFT);
        centerBuffer[bufferIndex] = analogRead(OPPONENT_CENTER);
        rightBuffer[bufferIndex] = analogRead(OPPONENT_RIGHT);

        bufferIndex = (bufferIndex + 1) % SENSOR_SAMPLE;
        lastOpponentSample = millis();
    }

    OpponentReadings r;
    r.left = medianOf(leftBuffer);
    r.center = medianOf(centerBuffer);
    r.right = medianOf(rightBuffer);

    return r;
}

OpponentDetection detectOpponent(const OpponentReadings &r) {
    OpponentDetection d;
    
    d.left   = r.left   > DETECT_THRESHOLD_L;
    d.center = r.center > DETECT_THRESHOLD_C;
    d.right  = r.right  > DETECT_THRESHOLD_R;

    d.leftEngaged   = r.left   > ENGAGE_THRESHOLD_L;
    d.centerEngaged = r.center > ENGAGE_THRESHOLD_C;
    d.rightEngaged  = r.right  > ENGAGE_THRESHOLD_R;

    return d;
}

bool anyOpponentDetected(const OpponentDetection &d) {
    return d.left || d.center || d.right;
}

bool anyEngaged(const OpponentDetection &d) {
    return d.leftEngaged || d.centerEngaged || d.rightEngaged;
}

static EdgeReadings readEdgesOnce() {
    EdgeReadings e;

    e.front = (digitalRead(EDGE_FRONT) == EDGE_WHITE_STATE);
    e.back  = (digitalRead(EDGE_BACK)  == EDGE_WHITE_STATE);

    return e;
}

EdgeReadings readEdgeSensors() {
    EdgeReadings first = readEdgesOnce();
    if (!first.front && !first.back) return first;

    delayMicroseconds(200);
    EdgeReadings second = readEdgesOnce();
    first.front = first.front && second.front;
    first.back  = first.back  && second.back;

    return first;
}

bool anyEdgeDetected(const EdgeReadings &e) {
    return e.front || e.back;
}

