#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Strategy_2.h"

#if ACTIVE_STRATEGY == 2

static SearchDirection currentDir        = SEARCH_LEFT;
static unsigned long   lastArcSwitchTime = 0;
static bool            firstArcCompleted = false;

enum ApproachSteering {
    STEER_STRAIGHT,
    STEER_LEFT,
    STEER_RIGHT
};

static ApproachSteering approachSteering = STEER_STRAIGHT;

// Pending steering request. `pendingValid` is a separate flag rather than
// using STEER_STRAIGHT as a "nothing pending" sentinel — STEER_STRAIGHT is a
// legitimate request, and conflating the two made a straight request commit
// one confirmation earlier than a left or right request.
static ApproachSteering pendingSteering  = STEER_STRAIGHT;
static unsigned long    pendingSince     = 0;
static bool             pendingValid     = false;

static void clearPendingSteering() {
    pendingSteering = STEER_STRAIGHT;
    pendingSince    = 0;
    pendingValid    = false;
}

void beginSearchArc(SearchDirection initialDir) {
    currentDir        = initialDir;
    lastArcSwitchTime = millis();
    firstArcCompleted = false;

    approachSteering = STEER_STRAIGHT;
    clearPendingSteering();
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
    int left  = readings.left;
    int right = readings.right;
    int front = max(readings.frontLeft, readings.frontRight);
    int side  = max(left, right);

    // Front sensors are strongest and above threshold — charge.
    if (front >= DIST_THRESHOLD && front >= side) {
        approachSteering = STEER_STRAIGHT;
        clearPendingSteering();
        attack();   // also refreshes the commit latch
        return;
    }

    // Blind zone: mid-charge with the front readings collapsed is contact,
    // not a lost target. The GP2Y0A21 cannot see inside 10 cm. Keep pushing
    // until the commit latch expires or an edge fires.
    if (attackCommitted()) {
        holdAttack();
        return;
    }

    int sideDelta = right - left;

    ApproachSteering requested = STEER_STRAIGHT;
    if (sideDelta > SIDE_TURN_MARGIN) {
        requested = STEER_RIGHT;
    } else if (sideDelta < -SIDE_TURN_MARGIN) {
        requested = STEER_LEFT;
    }

    // Hysteresis: once turning, keep turning until the error falls well
    // inside the margin, so the robot does not chatter on the boundary.
    int releaseMargin = SIDE_TURN_MARGIN - SIDE_TURN_HYSTERESIS;
    if (approachSteering == STEER_RIGHT && sideDelta > releaseMargin) {
        requested = STEER_RIGHT;
    } else if (approachSteering == STEER_LEFT && sideDelta < -releaseMargin) {
        requested = STEER_LEFT;
    }

    // Time-based confirmation. A loop-count threshold was satisfied in well
    // under a millisecond and confirmed nothing.
    if (requested != approachSteering) {
        if (pendingValid && requested == pendingSteering) {
            if (millis() - pendingSince >= SIDE_TURN_CONFIRM_MS) {
                approachSteering = requested;
                clearPendingSteering();
            }
        } else {
            pendingSteering = requested;
            pendingSince    = millis();
            pendingValid    = true;
        }
    } else {
        clearPendingSteering();
    }

    if (approachSteering == STEER_RIGHT) {
        drive(APPROACH_SPEED, TURN_SPEED);
    } else if (approachSteering == STEER_LEFT) {
        drive(TURN_SPEED, APPROACH_SPEED);
    } else {
        drive(APPROACH_SPEED, APPROACH_SPEED);
    }
}

#endif
