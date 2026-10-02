#ifndef STRATEGY_1_H
#define STRATEGY_1_H

#include "Robot.h"
#include "Sensors.h"

// ============================================================================
// Strategy 1 — Flanking. Proportional steering during the approach.
//
// Identical to Strategy 2 in every respect except approachTarget(): instead
// of a hard on/off differential turn, the heading error drives a continuously
// variable arc, so the robot keeps closing distance while it corrects. That
// sometimes lands a side or rear hit instead of a wedge-to-wedge collision.
//
// SENSOR PAIRING DECISION (the one design choice the formula does not make
// for you): the FRONT pair drives the proportional error, for fine centring.
// The SIDE sensors are a hard override, not a proportional term — if the
// opponent has left the front cone entirely, a gentle curve will never catch
// it, so we turn hard instead. Keep this consistent if you retune.
// ============================================================================

void beginSearchArc(SearchDirection initialDir);
void updateSearchArc();

bool anyOpponentDetected(const OpponentReadings &readings);
TargetSide getTargetSide(const OpponentReadings &readings);
void approachTarget(const OpponentReadings &readings);

// ===================== STRATEGY 1 TUNABLES =====================
// Proportional gain, expressed as a fraction so there is no floating point
// in the control path: correction = error * NUMERATOR / DENOMINATOR.
//
// `error` is a difference between two ADC readings, so at the 12-bit setting
// it can reach a few thousand while `correction` is capped at 255. Start LOW
// and increase: too high oscillates, too low tracks sluggishly.
const int STRATEGY1_KP_NUMERATOR   = 1;
const int STRATEGY1_KP_DENOMINATOR = 8;

// Below this much error, steering is treated as zero. Without it, sensor
// noise makes the robot jitter constantly while driving straight. Also
// doubles as the squared-up window before committing to a charge.
const int STRATEGY1_ERROR_DEADBAND = 80;

// Cruise speed during the approach.
const int STRATEGY1_BASE_SPEED = 165;

// Cap on the steering correction. At 255 with a base speed of 165 the inner
// wheel can go negative, which lets the robot pivot hard enough to catch an
// opponent at ninety degrees instead of arcing helplessly past it.
const int STRATEGY1_MAX_CORRECTION = 255;

#endif
