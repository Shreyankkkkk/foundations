#ifndef STRATEGY_1_H
#define STRATEGY_1_H

#include "Robot.h"
#include "Sensors.h"

// Proportional-steering strategy interface.
void beginSearchArc(SearchDirection initialDir);
void updateSearchArc();

bool anyOpponentDetected(const OpponentReadings &readings);
TargetSide getTargetSide(const OpponentReadings &readings);
void approachTarget(const OpponentReadings &readings);

#endif