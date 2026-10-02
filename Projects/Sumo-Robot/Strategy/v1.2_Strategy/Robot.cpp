// ============================================================================
// SumoX-26 — Robot.cpp
// Shared sumo behaviour: start, attack, edge recovery, maneuvers.
// ============================================================================

#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Robot.h"
#include "Strategy_Hybrid.h"

unsigned long attackDeadline = 0;

// ---------------------------------------------------------------------------
// Switches
// ---------------------------------------------------------------------------
static unsigned long lastStartOnMs = 0;
static unsigned long lastRoundOnMs = 0;

static bool startRawOn() {
    return digitalRead(START_BUTTON) == LOW;
}
static bool roundRawOn() {
    return digitalRead(ROUND_BUTTON) == LOW;
}
static bool bothRawOn() {
    return startRawOn() && roundRawOn();
}

// True while START_BUTTON alone is held — standby: sensors sampling, motors idle.
bool startOn() {
    if (startRawOn()) {
        lastStartOnMs = millis();
        return true;
    }
    return (millis() - lastStartOnMs) < SWITCH_GLITCH_MS;
}

// True only when BOTH switches are held — round active, motors enabled.
bool switchesOn() {
    bool start = startOn();

    bool round;
    if (roundRawOn()) {
        lastRoundOnMs = millis();
        round = true;
    } else {
        round = (millis() - lastRoundOnMs) < SWITCH_GLITCH_MS;
    }

    bool active = start && round;
    setMotorsEnabled(active);
    return active;
}

void abortAttack() {
    attackDeadline = millis();
}

void initRobot() {
    initMotors();
    initSensors();

    pinMode(START_BUTTON, INPUT_PULLUP);
    pinMode(ROUND_BUTTON, INPUT_PULLUP);
#ifdef LED_BUILTIN
    pinMode(LED_BUILTIN, OUTPUT);
#endif
    lastStartOnMs = millis() - SWITCH_GLITCH_MS;
    lastRoundOnMs = millis() - SWITCH_GLITCH_MS;
}

// ---------------------------------------------------------------------------
// Hammer attack (240 <-> 190 pulsing)
// ---------------------------------------------------------------------------
static unsigned long lastHammerToggle = 0;
static unsigned long lastHammerCall = 0;
static bool hammerHigh = true;

void resetHammerState() {
    lastHammerToggle = 0;
    lastHammerCall = 0;
    hammerHigh = true;
}

static void hammerSpeed(int correction) {
    unsigned long now = millis();
    if (now - lastHammerCall > 2 * HAMMER_PERIOD_MS) {
        hammerHigh = true;
        lastHammerToggle = now;
    } else if (now - lastHammerToggle >= HAMMER_PERIOD_MS) {
        hammerHigh = !hammerHigh;
        lastHammerToggle = now;
    }
    lastHammerCall = now;

    int baseSpeed = hammerHigh ? ATTACK_SPEED : (ATTACK_SPEED - HAMMER_AMPLITUDE);
    drive(constrain(baseSpeed + correction, 0, 255),
          constrain(baseSpeed - correction, 0, 255));
}

void commitAttack(int correction, int frontReading) {
    unsigned long window = (frontReading >= PUSH_READING) ? PUSH_COMMIT_MS : ATTACK_COMMIT_MS;
    attackDeadline = millis() + window;
    hammerSpeed(correction);
}

void hammerDrive(int correction) {
    hammerSpeed(correction);
}

// ---------------------------------------------------------------------------
// Edge recovery
// ---------------------------------------------------------------------------
static void driveAwayFromEdge(const EdgeReadings &e, int speed, bool straight) {
    bool front = e.frontLeft  || e.frontRight;
    bool back  = e.backLeft   || e.backRight;
    bool left  = e.frontLeft  || e.backLeft;
    bool right = e.frontRight || e.backRight;

    if (front && back) {
        if (left && !right)      drive(speed, speed / 2);
        else if (right && !left) drive(speed / 2, speed);
        else                     drive(-speed, speed);
    }
    else if (front) {
        if (straight || (e.frontLeft && e.frontRight)) drive(-speed, -speed);
        else if (e.frontLeft)  drive(-speed / 2, -speed);
        else                   drive(-speed, -speed / 2);
    }
    else if (back) {
        if (straight || (e.backLeft && e.backRight)) drive(speed, speed);
        else if (e.backLeft)   drive(speed / 2, speed);
        else                   drive(speed, speed / 2);
    }
    else {
        stopMotors();
    }
}

static void repositionAway(bool goBack) {
    unsigned long startTime = millis();
    int speed = goBack ? -REPOSITION_SPEED : REPOSITION_SPEED;

    while (millis() - startTime < REPOSITION_MS) {
        if (!switchesOn()) break;
        EdgeReadings e = readEdgeSensors();
        bool blocked = goBack ? (e.backLeft || e.backRight) : (e.frontLeft || e.frontRight);
        if (blocked) break;
        drive(speed, speed);
    }
    stopMotors();
}

void edgeRecover(const EdgeReadings &edges) {
    abortAttack();
    drive(0, 0);

    unsigned long brakeStart = millis();
    while (millis() - brakeStart < EDGE_BRAKE_MS) {
        if (!switchesOn()) {
            stopMotors();
            return;
        }
    }

    const EdgeReadings initialEdges = edges;
    const bool initialFront = edges.frontLeft || edges.frontRight;
    const bool initialBack  = edges.backLeft  || edges.backRight;
    const bool faceOutward  = initialFront && !initialBack;

    static bool alternateClockwise = true;
    bool turnClockwise;
    if (edges.frontLeft && !edges.frontRight)      turnClockwise = true;
    else if (edges.frontRight && !edges.frontLeft) turnClockwise = false;
    else { turnClockwise = alternateClockwise; alternateClockwise = !alternateClockwise; }

    unsigned long startTime = millis();
    unsigned long clearedAt = 0;
    unsigned long turnStart = 0;
    bool turning = false;

    while (true) {
        if (!switchesOn()) {
            stopMotors();
            return;
        }

        EdgeReadings current = readEdgeSensors();
        unsigned long now = millis();
        unsigned long elapsed = now - startTime;

        if (elapsed > EDGE_RECOVER_MAX_MS) {
            stopMotors();
            const bool nowFront = current.frontLeft || current.frontRight;
            const bool nowBack  = current.backLeft  || current.backRight;
            if (nowFront && !nowBack)      repositionAway(true);
            else if (nowBack && !nowFront) repositionAway(false);
            return;
        }

        if (turning) {
            if (anyEdgeDetected(current)) {
                turning = false;
                clearedAt = 0;
            } else if (now - turnStart >= EDGE_TURN_MS) {
                stopMotors();
                return;
            } else {
                if (turnClockwise) drive(EDGE_TURN_SPEED, -EDGE_TURN_SPEED);
                else               drive(-EDGE_TURN_SPEED, EDGE_TURN_SPEED);
                continue;
            }
        }

        int speed = (elapsed > EDGE_ESCALATE_MS) ? EDGE_RECOVER_MAX_SPEED : EDGE_RECOVER_SPEED;

        if (elapsed < EDGE_RETREAT_MS) {
            driveAwayFromEdge(initialEdges, speed, true);
            clearedAt = 0;
            continue;
        }

        if (anyEdgeDetected(current)) {
            driveAwayFromEdge(current, speed, false);
            clearedAt = 0;
            continue;
        }

        stopMotors();
        if (clearedAt == 0) clearedAt = now;
        if (now - clearedAt >= EDGE_CONFIRM_CLEAR_MS) {
            if (faceOutward) {
                turning = true;
                turnStart = now;
            } else {
                return;
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Maneuvers
// ---------------------------------------------------------------------------
static bool maneuverSafe(bool stopOnOpponent) {
    if (!switchesOn()) {
        stopMotors();
        return false;
    }
    EdgeReadings edges = readEdgeSensors();
    if (anyEdgeDetected(edges)) {
        edgeRecover(edges);
        return false;
    }
    if (stopOnOpponent && anyOpponentDetected(readOpponentSensors())) {
        return false;
    }
    return true;
}

static bool executeManeuver(unsigned long pivotMs, unsigned long moveMs,
                            bool pivotLeft, bool reverse, bool stopOnOpponent) {
    const int moveSpeed = reverse ? -OFFSET_SPEED : OFFSET_SPEED;

    unsigned long phaseStart = millis();
    while (millis() - phaseStart < pivotMs) {
        if (!maneuverSafe(stopOnOpponent)) return false;
        if (pivotLeft) drive(-OFFSET_SPEED, OFFSET_SPEED);
        else           drive(OFFSET_SPEED, -OFFSET_SPEED);
    }

    phaseStart = millis();
    while (millis() - phaseStart < moveMs) {
        if (!maneuverSafe(stopOnOpponent)) return false;
        drive(moveSpeed, moveSpeed);
    }

    stopMotors();
    return true;
}

bool executeBalancedOffset() {
    return executeManeuver(OFFSET_PIVOT_MS, OFFSET_FORWARD_MS, true, false, true);
}

// No longer called by waitForStart() — kept as an unused fallback option.
// Harmless to leave (unused-function warning only); delete if you don't want it.
static bool executeRandomStart() {
    const long count = (long)(sizeof(START_PALETTE) / sizeof(START_PALETTE[0]));
    const StartRoutine &s = START_PALETTE[random(0, count)];
    const bool pivotLeft = (random(0, 2) == 0);
    return executeManeuver(s.pivotMs, s.moveMs, pivotLeft, s.reverse, false);
}

static bool pivotInPlace(unsigned long ms, bool pivotLeft, int speed) {
    unsigned long phaseStart = millis();
    while (millis() - phaseStart < ms) {
        if (!maneuverSafe(false)) return false;
        if (pivotLeft) drive(-speed, speed);
        else           drive(speed, -speed);
    }
    return true;
}

static bool driveStraight(unsigned long ms, int speed) {
    unsigned long phaseStart = millis();
    while (millis() - phaseStart < ms) {
        if (!maneuverSafe(false)) return false;
        drive(speed, speed);
    }
    return true;
}

// Opening move: pivot toward a random side, drive forward (the "step"),
// then pivot 45° back the OPPOSITE way. Nets out facing roughly the
// original heading, offset diagonally. Edge-safe at every phase via
// maneuverSafe() — a detected edge aborts straight into edgeRecover().
bool executeDiagonalStart() {
    const bool firstPivotLeft = (random(0, 2) == 0);

    if (!pivotInPlace(DIAGONAL_TURN_MS, firstPivotLeft, DIAGONAL_TURN_SPEED)) {
        stopMotors();
        return false;
    }
    if (!driveStraight(DIAGONAL_DRIVE_MS, DIAGONAL_DRIVE_SPEED)) {
        stopMotors();
        return false;
    }
    if (!pivotInPlace(DIAGONAL_TURN_MS, !firstPivotLeft, DIAGONAL_TURN_SPEED)) {
        stopMotors();
        return false;
    }

    stopMotors();
    return true;
}

// ---------------------------------------------------------------------------
// Start sequence
// ---------------------------------------------------------------------------
static void showSelfTest(bool sensorSeesWhite) {
#ifdef LED_BUILTIN
    bool on = sensorSeesWhite ? (((millis() / 100) % 2) == 0) : true;
    digitalWrite(LED_BUILTIN, on ? HIGH : LOW);
#else
    (void)sensorSeesWhite;
#endif
}

void waitForStart() {
    stopMotors();
    static SearchDirection nextSearchDirection = SEARCH_LEFT;

    while (true) {
        if (!bothRawOn()) {
            stopMotors();
            continue;
        }
        unsigned long steadySince = millis();
        bool steady = true;
        while (millis() - steadySince < START_DEBOUNCE_MS) {
            if (!bothRawOn()) {
                steady = false;
                break;
            }
        }
        if (!steady) continue;

        randomSeed(micros());
        unsigned long countdownStart = millis();
        inhibitMotionUntil(countdownStart + START_COUNTDOWN_MS);

        bool stillArmed = true;
        while (millis() - countdownStart < START_COUNTDOWN_MS) {
            if (!switchesOn()) {
                stillArmed = false;
                stopMotors();
                break;
            }
            showSelfTest(anyEdgeDetected(readEdgeSensors()));
        }
        showSelfTest(false);
        if (!stillArmed) continue;

        abortAttack();
        executeDiagonalStart();
        primeOpponentSensors();

        beginSearchArc(nextSearchDirection);
        nextSearchDirection = (nextSearchDirection == SEARCH_LEFT) ? SEARCH_RIGHT : SEARCH_LEFT;
        return;
    }
}