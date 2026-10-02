#ifndef SENSORS_H
#define SENSORS_H
#include "Hardware.h"

struct OpponentReadings
{
    int left, center, right;
}; // latest raw ADC per sensor

struct OpponentDetection
{
    bool left, center, right;             // confirmed detection (>= WEAK_THRESHOLD, debounced)
    bool leftNear, centerNear, rightNear; // contact latch: has been >= NEAR_THRESHOLD since last "not detected"
};

struct EdgeReadings
{
    bool front, back;
};

void initSensors();
void primeOpponentSensors(); // resets all per-sensor state (counters, latches) — call after any state reset

void updateOpponentSensors(); // call every tick; self-throttles to SENSOR_SAMPLE_INTERVAL_MS internally

OpponentReadings getOpponentReadings();
OpponentDetection getOpponentDetection();

bool anyOpponentDetected(const OpponentDetection &d);
bool anyContact(const OpponentDetection &d); // true if latched-near AND currently reading in the contact band — replaces v4's anyEngaged

// Coarse ADC->cm estimate, valid ONLY in the monotonic far region (roughly 10-80cm).
// Placeholder 2-point linear fit until the real 8-point bench table replaces it.
// Used by Map.cpp for the phantom-gate ray-circle check — not accurate enough for anything else.
float estimateFarRangeCm(int rawAdc);

void calibrateEdgePolarity(); // call once while the robot sits on the black surface
EdgeReadings readEdgeSensors();
bool anyEdgeDetected(const EdgeReadings &e);

#endif