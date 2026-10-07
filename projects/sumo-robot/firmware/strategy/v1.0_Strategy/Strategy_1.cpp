#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Strategy_1.h"

#if ACTIVE_STRATEGY == 1

static SearchDirection currentDir = SEARCH_LEFT;
static unsigned long lastArcSwitchTime = 0;
static bool firstArcCompleted = false;
static int lastCorrection = 0;

void beginSearchArc(SearchDirection initialDir) {
    currentDir = initialDir;
    lastArcSwitchTime = millis();
    firstArcCompleted = false;
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
    int strongest = max(max(readings.frontLeft, readings.frontRight),
                        max(readings.left, readings.right));
    if (strongest < DIST_THRESHOLD) {
        return TARGET_NONE;
    }
    if (readings.frontLeft >= readings.left &&
        readings.frontLeft >= readings.right &&
        readings.frontLeft >= readings.frontRight) {
        return TARGET_FRONT;
    }
    if (readings.frontRight >= readings.left &&
        readings.frontRight >= readings.right) {
        return TARGET_FRONT;
    }
    return readings.left >= readings.right ? TARGET_LEFT : TARGET_RIGHT;
}

void approachTarget(const OpponentReadings &readings) {
    int frontDelta = readings.frontRight - readings.frontLeft;
    int front = max(readings.frontLeft, readings.frontRight);
    int sideOverride = 0;
    if (readings.right >= DIST_THRESHOLD && readings.left < DIST_THRESHOLD) {
        sideOverride = STRATEGY1_MAX_CORRECTION;
    } else if (readings.left >= DIST_THRESHOLD && readings.right < DIST_THRESHOLD) {
        sideOverride = -STRATEGY1_MAX_CORRECTION;
    }

    int error = sideOverride != 0 ? sideOverride : frontDelta;
    int correction = 0;
    if (sideOverride != 0) {
        correction = sideOverride;
    } else if (abs(error) >= STRATEGY1_ERROR_DEADBAND) {
        correction = constrain(
            error * STRATEGY1_KP_NUMERATOR / STRATEGY1_KP_DENOMINATOR,
            -STRATEGY1_MAX_CORRECTION, STRATEGY1_MAX_CORRECTION);
    } else {
        correction = 0;
    }
    lastCorrection = correction;

    if (sideOverride == 0 && front >= DIST_THRESHOLD && abs(frontDelta) < STRATEGY1_ERROR_DEADBAND) {
        hammerAttack(correction);
    } else {
        drive(constrain(STRATEGY1_BASE_SPEED + correction, -255, 255),
              constrain(STRATEGY1_BASE_SPEED - correction, -255, 255));
    }
}

int getLastCorrection() {
    return lastCorrection;
}

#endif
