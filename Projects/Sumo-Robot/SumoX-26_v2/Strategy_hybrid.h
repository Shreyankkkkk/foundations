#ifndef STRATEGY_HYBRID_H
#define STRATEGY_HYBRID_H

#include "Robot.h"
#include "Sensors.h"

void beginSearchArc(SearchDirection initialDir);
void updateSearchArc();

bool anyOpponentDetected(const OpponentReadings &readings);
void approachTarget(const OpponentReadings &readings);
int getLastCorrection();
int getLastSeenDirection();   // -1 = left, 0 = straight ahead/unknown, +1 = right

#endif