#ifndef STRATEGY_2_H
#define STRATEGY_2_H

#include "Robot.h"
#include "Sensors.h"

// Baseline strategy: search with a moving arc, turn toward the strongest
// target reading, then commit to a straight attack when squared up.
void beginSearchArc(SearchDirection initialDir);
void updateSearchArc();

bool anyOpponentDetected(const OpponentReadings &readings);
TargetSide getTargetSide(const OpponentReadings &readings);
void approachTarget(const OpponentReadings &readings);
int getLastCorrection();

#endif