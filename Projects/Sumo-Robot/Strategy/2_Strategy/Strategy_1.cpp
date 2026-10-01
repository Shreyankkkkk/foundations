#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Strategy_1.h"

#if ACTIVE_STRATEGY == 1

static SearchDirection currentDir        = SEARCH_LEFT;
static unsigned long   lastArcSwitchTime = 0;
static bool            firstArcCompleted = false;

static bool            squaredPending = false;
static unsigned long   squaredSince   = 0;

void beginSearchArc(SearchDirection initialDir) {
    currentDir        = initialDir;
    lastArcSwitchTime = millis();
    firstArcCompleted = false;

    squaredPending = false;
    squaredSince   = 0;
    cancelAttack();
}

void updateSearchArc() {
    unsigned long now = millis();
    unsigned long targetInterval =
        firstArcCompleted ? SEARCH_ARC_FLIP_MS : SEARCH_FIRST_ARC_MS;

    if (now - lastArcSwitchTime >= targetInterval) {
        currentDir = (currentDir == SEARCH_LEFT) ? SEARCH_RIGHT : SEARCH_LEFT;
        lastArcSwitchTime = now;
        firstArcCompleted = true;
    }

    if (currentDir == SEARCH_LEFT) {
        drive(SEARCH_SLOW_SPEED, SEARCH_FAST_SPEED);
    } else {
        drive(SEARCH_FAST_SPEED, SEARCH_SLOW_SPEED);
    }
}

bool anyOpponentDetected(const OpponentReadings &readings) {
    return isOpponentDetected(readings.frontLeft) ||
           isOpponentDetected(readings.frontRight) ||
           isOpponentDetected(readings.left) ||
           isOpponentDetected(readings.right);
}

TargetSide getTargetSide(const OpponentReadings &readings) {
    int front     = max(readings.frontLeft, readings.frontRight);
    int strongest = max(front, max(readings.left, readings.right));

    if (strongest < DIST_THRESHOLD) {
        return TARGET_NONE;
    }
    if (front >= readings.left && front >= readings.right) {
        return TARGET_FRONT;
    }
    return (readings.left >= readings.right) ? TARGET_LEFT : TARGET_RIGHT;
}

void approachTarget(const OpponentReadings &readings) {
    int front      = max(readings.frontLeft, readings.frontRight);
    int frontDelta = readings.frontRight - readings.frontLeft;

    // --- Side sensors: hard override, not a proportional term -------------
    // Only fires when the opponent has genuinely left the front cone: that
    // side is above threshold, the other side is not, and the side reading
    // beats both front sensors.
    bool overrideRight = (readings.right >= DIST_THRESHOLD) &&
                         (readings.left  <  DIST_THRESHOLD) &&
                         (readings.right >  front);
    bool overrideLeft  = (readings.left  >= DIST_THRESHOLD) &&
                         (readings.right <  DIST_THRESHOLD) &&
                         (readings.left  >  front);

    int  correction = 0;
    bool overriding = false;

    if (overrideRight) {
        correction = STRATEGY1_MAX_CORRECTION;
        overriding = true;
    } else if (overrideLeft) {
        correction = -STRATEGY1_MAX_CORRECTION;
        overriding = true;
    } else if (abs(frontDelta) >= STRATEGY1_ERROR_DEADBAND) {
        long scaled = (long)frontDelta * STRATEGY1_KP_NUMERATOR /
                      STRATEGY1_KP_DENOMINATOR;
        correction = (int)constrain(scaled,
                                    (long)-STRATEGY1_MAX_CORRECTION,
                                    (long)STRATEGY1_MAX_CORRECTION);
    }

    // --- Squared up? ------------------------------------------------------
    // Requires the reading to hold for SQUARED_CONFIRM_MS so one lucky sample
    // cannot launch a full-speed charge at nothing.
    bool squared = !overriding &&
                   (front >= DIST_THRESHOLD) &&
                   (abs(frontDelta) < STRATEGY1_ERROR_DEADBAND);

    if (squared) {
        if (!squaredPending) {
            squaredPending = true;
            squaredSince   = millis();
        }
        if (millis() - squaredSince >= SQUARED_CONFIRM_MS) {
            attack();   // also refreshes the commit latch
            return;
        }
    } else {
        squaredPending = false;
    }

    // --- Blind zone ------------------------------------------------------
    // If we are mid-charge and the front readings have collapsed, that is
    // almost certainly contact, not a lost target — the GP2Y0A21 cannot see
    // inside 10 cm. Keep pushing until the latch expires or an edge fires.
    if (attackCommitted()) {
        holdAttack();
        return;
    }

    // --- Proportional steer ----------------------------------------------
    // Positive correction means the target is to the right, so the LEFT
    // wheel runs faster and the robot curves right.
    drive(constrain(STRATEGY1_BASE_SPEED + correction, -255, 255),
          constrain(STRATEGY1_BASE_SPEED - correction, -255, 255));
}

#endif
