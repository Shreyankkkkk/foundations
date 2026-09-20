#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Strategy_Hybrid.h"

static SearchDirection currentDir = SEARCH_LEFT;
static unsigned long lastArcSwitchTime = 0;
static bool firstArcCompleted = false;
static int lastCorrection = 0;
static int lastSeenDirection = 0;

static int activeSideOverride = 0;
static int pendingSideOverride = 0;
static unsigned long pendingSideOverrideSince = 0;

void beginSearchArc(SearchDirection initialDir) {
    currentDir = initialDir;
    lastArcSwitchTime = millis();
    firstArcCompleted = false;

    activeSideOverride = 0;
    pendingSideOverride = 0;
    pendingSideOverrideSince = 0;

    lastCorrection = 0;
    lastSeenDirection = 0;
    resetHammerState();
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

// A side sensor must request the same override for SIDE_TURN_CONFIRM_MS before
// it takes effect. Releasing it is instant (less overshoot).
static void updateSideOverride(int requested) {
    if (requested == 0) {
        activeSideOverride = 0;
        pendingSideOverride = 0;
        return;
    }
    if (requested == activeSideOverride) {
        pendingSideOverride = 0;
        return;
    }
    if (pendingSideOverride != requested) {
        pendingSideOverride = requested;
        pendingSideOverrideSince = millis();
        return;
    }
    if (millis() - pendingSideOverrideSince >= SIDE_TURN_CONFIRM_MS) {
        activeSideOverride = requested;
        pendingSideOverride = 0;
    }
}

void approachTarget(const OpponentReadings &r) {
    const bool frontLeftSees  = isOpponentDetected(r.frontLeft);
    const bool frontRightSees = isOpponentDetected(r.frontRight);
    const bool leftSees       = isOpponentDetected(r.left);
    const bool rightSees      = isOpponentDetected(r.right);

    const int frontDelta = r.frontRight - r.frontLeft;   // > 0: opponent is more to the right
    const int frontMax   = max(r.frontLeft, r.frontRight);

    // A side sensor only takes over when the opponent is NOT seen in front.
    int requestedSideOverride = 0;
    if (!frontLeftSees && !frontRightSees) {
        if (rightSees && !leftSees)      requestedSideOverride = STRATEGY1_MAX_CORRECTION;
        else if (leftSees && !rightSees) requestedSideOverride = -STRATEGY1_MAX_CORRECTION;
    }
    updateSideOverride(requestedSideOverride);
    const int sideOverride = activeSideOverride;

    int correction = 0;
    if (sideOverride != 0) {
        correction = sideOverride;
    } else if (abs(frontDelta) >= STRATEGY1_ERROR_DEADBAND) {
        correction = constrain(
            frontDelta * STRATEGY1_KP_NUMERATOR / STRATEGY1_KP_DENOMINATOR,
            -STRATEGY1_MAX_CORRECTION, STRATEGY1_MAX_CORRECTION);
    }

    // Remember which way the opponent is (used if we lose it).
    if (frontLeftSees && frontRightSees)        lastSeenDirection = 0;
    else if (frontRightSees && !frontLeftSees)  lastSeenDirection = 1;
    else if (frontLeftSees && !frontRightSees)  lastSeenDirection = -1;
    else if (rightSees && !leftSees)            lastSeenDirection = 1;
    else if (leftSees && !rightSees)            lastSeenDirection = -1;
    else                                        lastSeenDirection = 0;

    lastCorrection = correction;

    // During a push, ONE front sensor is enough to keep pushing at full power.
    const bool squareOn    = frontLeftSees && frontRightSees;
    const bool keepPushing = (millis() < attackDeadline) && (frontLeftSees || frontRightSees);

    if (sideOverride == 0 && (squareOn || keepPushing)) {
        // Opponent squarely in front: push at full hammer power, with only a small steering trim.
        int trim = constrain(correction, -PUSH_MAX_CORRECTION, PUSH_MAX_CORRECTION);
        lastCorrection = trim;
        commitAttack(trim, frontMax);
    } else {
        // Still lining up: steer at approach speed.
        drive(constrain(STRATEGY1_BASE_SPEED + correction, -255, 255),
              constrain(STRATEGY1_BASE_SPEED - correction, -255, 255));
    }
}

int getLastCorrection() {
    return lastCorrection;
}

int getLastSeenDirection() {
    return lastSeenDirection;
}