#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Strategy_2.h"

#if ACTIVE_STRATEGY == 2

static SearchDirection currentDir = SEARCH_LEFT;
static unsigned long lastArcSwitchTime = 0;
static bool firstArcCompleted = false;

enum ApproachSteering {
    STEER_STRAIGHT,
    STEER_LEFT,
    STEER_RIGHT
};

static ApproachSteering approachSteering = STEER_STRAIGHT;
static ApproachSteering pendingSteering = STEER_STRAIGHT;
static unsigned long pendingSteeringSince = 0;
static bool pendingSteeringValid = false;

void beginSearchArc(SearchDirection initialDir) {
    currentDir = initialDir;
    lastArcSwitchTime = millis();
    firstArcCompleted = false;
    approachSteering = STEER_STRAIGHT;
    pendingSteering = STEER_STRAIGHT;
    pendingSteeringSince = 0;
    pendingSteeringValid = false;
}

void updateSearchArc() {
    unsigned long now = millis();
    unsigned long targetInterval = firstArcCompleted ? SEARCH_ARC_FLIP_MS : SEARCH_FIRST_ARC_MS;
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
    int frontLeft = readings.frontLeft;
    int frontRight = readings.frontRight;
    int left = readings.left;
    int right = readings.right;

    int strongest = max(max(frontLeft, frontRight), max(left, right));
    if (strongest < DIST_THRESHOLD) {
        return TARGET_NONE;
    }
    // Front sensors win if they are the strongest.
    if (frontLeft >= frontRight && frontLeft >= left && frontLeft >= right) {
        return TARGET_FRONT;
    }
    if (frontRight >= frontLeft && frontRight >= left && frontRight >= right) {
        return TARGET_FRONT;
    }
    if (left >= right && left >= DIST_THRESHOLD) {
        return TARGET_LEFT;
    }
    if (right >= left && right >= DIST_THRESHOLD) {
        return TARGET_RIGHT;
    }

    return TARGET_NONE;
}

void approachTarget(const OpponentReadings &readings) {
    int left = readings.left;
    int right = readings.right;
    int front = max(readings.frontLeft, readings.frontRight);
    int side = max(left, right);

    if (front >= DIST_THRESHOLD && front >= side) {
        approachSteering = STEER_STRAIGHT;
        pendingSteering = STEER_STRAIGHT;
        pendingSteeringSince = 0;
        hammerAttack((right - left) * STRATEGY2_PUSH_KP);
        return;
    }

    int sideDelta = right - left;
    ApproachSteering requestedSteering = STEER_STRAIGHT;
    if (sideDelta > SIDE_TURN_MARGIN) {
        requestedSteering = STEER_RIGHT;
    } else if (sideDelta < -SIDE_TURN_MARGIN) {
        requestedSteering = STEER_LEFT;
    }

    int releaseMargin = SIDE_TURN_MARGIN - SIDE_TURN_HYSTERESIS;
    if (approachSteering == STEER_RIGHT && sideDelta > releaseMargin) {
        requestedSteering = STEER_RIGHT;
    } else if (approachSteering == STEER_LEFT && sideDelta < -releaseMargin) {
        requestedSteering = STEER_LEFT;
    }

    if (requestedSteering != approachSteering) {
        if (pendingSteeringValid && requestedSteering == pendingSteering) {
            if (millis() - pendingSteeringSince >= SIDE_TURN_CONFIRM_MS) {
                approachSteering = requestedSteering;
                pendingSteering = STEER_STRAIGHT;
                pendingSteeringSince = 0;
                pendingSteeringValid = false;
            }
        } else {
            pendingSteering = requestedSteering;
            pendingSteeringSince = millis();
            pendingSteeringValid = true;
        }
    } else {
        pendingSteering = STEER_STRAIGHT;
        pendingSteeringSince = 0;
        pendingSteeringValid = false;
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
