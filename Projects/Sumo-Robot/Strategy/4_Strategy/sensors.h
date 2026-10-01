#ifndef SENSORS_H
#define SENSORS_H
#include "Hardware.h"

struct OpponentReadings { int left, center, right; };

struct OpponentDetection {
    bool left, center, right;
    bool leftEngaged, centerEngaged, rightEngaged;
};

struct EdgeReadings { bool front, back; };

void initSensors();
void primeOpponentSensors();

OpponentReadings readOpponentSensors();
OpponentDetection detectOpponent(const OpponentReadings &r);
bool anyOpponentDetected(const OpponentDetection &d);
bool anyEngaged(const OpponentDetection &d);

EdgeReadings readEdgeSensors();
bool anyEdgeDetected(const EdgeReadings &e);

#endif