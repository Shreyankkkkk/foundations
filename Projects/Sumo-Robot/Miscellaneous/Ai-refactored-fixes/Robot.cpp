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
static unsigned long lastSwitchesOnMs = 0;

// The raw, unfiltered pin state.
static bool switchesRawOn() {
    return digitalRead(START_BUTTON) == LOW && digitalRead(ROUND_BUTTON) == LOW;
}

// "Are both switches ON right now?" with a glitch filter:
//  * raw ON  -> motors enabled, returns true.
//  * raw OFF -> motors gated off IMMEDIATELY (a real OFF stops the robot at once),
//               but the answer stays true until the OFF has lasted SWITCH_GLITCH_MS.
// Without this, one vibration blip on a rocker/lever connector would reset the
// state machine and trigger a fresh 5.2 s frozen countdown in the middle of a match.
bool switchesOn() {
    const unsigned long now = millis();
    if (switchesRawOn()) {
        lastSwitchesOnMs = now;
        setMotorsEnabled(true);
        return true;
    }
    setMotorsEnabled(false);
    return (now - lastSwitchesOnMs) < SWITCH_GLITCH_MS;
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
    // Start "long ago" so the filter reports OFF until a real ON is seen.
    lastSwitchesOnMs = millis() - SWITCH_GLITCH_MS;
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
        // A gap since the last call means a fresh push: start at FULL power.
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
// Convention: drive(left, right), positive = forward.
// ---------------------------------------------------------------------------

// Pick the motion that moves the corner(s) that saw white AWAY from the line.
// 'straight' = plain straight retreat (used for the first EDGE_RETREAT_MS).
static void driveAwayFromEdge(const EdgeReadings &e, int speed, bool straight) {
    bool front = e.frontLeft  || e.frontRight;
    bool back  = e.backLeft   || e.backRight;
    bool left  = e.frontLeft  || e.backLeft;
    bool right = e.frontRight || e.backRight;

    if (front && back) {
        if (left && !right)      drive(speed, speed / 2);   // line along the left side: arc forward-right
        else if (right && !left) drive(speed / 2, speed);   // line along the right side: arc forward-left
        else                     drive(-speed, speed);      // trapped or lifted: spin
    }
    else if (front) {
        if (straight || (e.frontLeft && e.frontRight)) drive(-speed, -speed);
        else if (e.frontLeft)  drive(-speed / 2, -speed);   // reverse, nose swings right (away from left line)
        else                   drive(-speed, -speed / 2);   // reverse, nose swings left (away from right line)
    }
    else if (back) {
        if (straight || (e.backLeft && e.backRight)) drive(speed, speed);
        else if (e.backLeft)   drive(speed / 2, speed);     // forward, tail swings right (away from left line)
        else                   drive(speed, speed / 2);     // forward, tail swings left (away from right line)
    }
    else {
        stopMotors();   // unreachable by construction (callers only pass edges); kept as a safe default
    }
}

// Fallback if recovery takes too long: drive straight away from the line for a moment.
// Only stops early if the line appears on the side we are moving TOWARD.
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

    // Brake for EDGE_BRAKE_MS, polling the switches instead of a blocking delay().
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
    const bool faceOutward  = initialFront && !initialBack;   // nose was at the line -> turn around when clear

    // Which way to turn around: away from the side that saw the line.
    static bool alternateClockwise = true;
    bool turnClockwise;
    if (edges.frontLeft && !edges.frontRight)      turnClockwise = true;    // line on the left -> swing right
    else if (edges.frontRight && !edges.frontLeft) turnClockwise = false;   // line on the right -> swing left
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

        // Took too long: fallback move, then give control back.
        // The robot may have turned since the start, so decide the direction from
        // what the sensors see NOW, not from the edges that started the recovery.
        if (elapsed > EDGE_RECOVER_MAX_MS) {
            stopMotors();
            const bool nowFront = current.frontLeft || current.frontRight;
            const bool nowBack  = current.backLeft  || current.backRight;
            if (nowFront && !nowBack)      repositionAway(true);
            else if (nowBack && !nowFront) repositionAway(false);
            return;
        }

        // ---- Stage 2: turn away from the line ----
        if (turning) {
            if (anyEdgeDetected(current)) {
                turning = false;          // touched a line while turning: go back to escaping
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

        // ---- Stage 1: get away from the line ----
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

        // No line visible: stop and confirm it stays clear.
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
// Maneuvers (pivot in place, then drive forward or backward)
// ---------------------------------------------------------------------------

// Checked every loop inside a maneuver. Returns false if the maneuver must stop.
// stopOnOpponent: true  = stop as soon as any opponent sensor fires (after losing a target)
//                 false = ignore the opponent (opening move)
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

static bool executeRandomStart() {
    const long count = (long)(sizeof(START_PALETTE) / sizeof(START_PALETTE[0]));
    const StartRoutine &s = START_PALETTE[random(0, count)];
    const bool pivotLeft = (random(0, 2) == 0);   // write "true" here to always pivot left
    return executeManeuver(s.pivotMs, s.moveMs, pivotLeft, s.reverse, false);
}

// ---------------------------------------------------------------------------
// Start sequence. Main loop calls this ONCE each time the switches go ON.
// ---------------------------------------------------------------------------

// Sensor self-test light during the countdown: steady = all four edge sensors
// see black, blinking = at least one sees white (check it before the round!).
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
        // 1) Wait here until both switches are ON and steady. RAW reads on purpose:
        //    arming must not be helped along by the glitch filter.
        if (!switchesRawOn()) {
            stopMotors();
            continue;
        }
        unsigned long steadySince = millis();
        bool steady = true;
        while (millis() - steadySince < START_DEBOUNCE_MS) {
            if (!switchesRawOn()) {
                steady = false;
                break;
            }
        }
        if (!steady) continue;

        // 2) Countdown: no movement allowed until it finishes.
        //    (Filtered check here: a blip must not restart a countdown that is
        //    already running; a real OFF still cancels it.)
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
        if (!stillArmed) continue;    // switch flicked off: wait for ON again, new countdown

        // 3) Go: fresh sensor data, opening move, then search.
        abortAttack();
        executeRandomStart();
        primeOpponentSensors();       // the opening move doesn't sample sensors: refresh them

        beginSearchArc(nextSearchDirection);
        nextSearchDirection = (nextSearchDirection == SEARCH_LEFT) ? SEARCH_RIGHT : SEARCH_LEFT;
        return;
    }
}
