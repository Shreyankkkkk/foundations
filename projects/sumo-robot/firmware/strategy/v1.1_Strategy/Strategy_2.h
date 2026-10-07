#ifndef STRATEGY_2_H
#define STRATEGY_2_H

#include "Robot.h"
#include "Sensors.h"

// ============================================================================
// Strategy 2 — Baseline. Build and prove this one first.
//
// Search with a moving arc, turn toward the strongest target reading with a
// hard on/off differential turn, then commit to a straight attack once the
// front sensors are the strongest. This is the shape most competitive sumo
// code actually uses, and it is the safety net Strategy 1 is measured against.
//
// Steering tunables (SIDE_TURN_MARGIN, SIDE_TURN_HYSTERESIS,
// SIDE_TURN_CONFIRM_MS) live in Robot.h with the rest of the shared numbers.
// ============================================================================

void beginSearchArc(SearchDirection initialDir);
void updateSearchArc();

bool anyOpponentDetected(const OpponentReadings &readings);
TargetSide getTargetSide(const OpponentReadings &readings);
void approachTarget(const OpponentReadings &readings);

#endif
