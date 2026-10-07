// ============================================================================
// SumoX-26 — Robot.cpp
// ----------------------------------------------------------------------------
// Shared sumo-specific behavior — attack, edge recovery, repositioning,
// startup — that both Strategy1 and Strategy2 call into. Nothing in here is
// strategy-specific.
// ============================================================================

#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Robot.h"
#if ACTIVE_STRATEGY == 1
#include "Strategy_1.h"
#elif ACTIVE_STRATEGY == 2
#include "Strategy_2.h"
#else
#error "ACTIVE_STRATEGY must be 1 or 2"
#endif

void initRobot() {
    initMotors();
    initSensors();

    pinMode(START_BUTTON, INPUT_PULLUP);
    pinMode(ROUND_BUTTON, INPUT_PULLUP);
}

void waitForStart() {
    stopMotors();
    cancelAttack();

    // Alternate which way the opening arc curves from round to round. The
    // robots start roughly 20-40 cm apart on the centre lines, so an opening
    // that is identical every single round is an opening the other team can
    // plan against. Deterministic, not random — the rulebook's tie-break
    // criteria reward consistent deliberate movement.
    static SearchDirection nextSearchDirection = SEARCH_LEFT;

    while (true) {
        if (digitalRead(START_BUTTON) != LOW) {
            stopMotors();
            continue;
        }

        if (digitalRead(ROUND_BUTTON) != LOW) {
            continue;
        }

        unsigned long buttonDetectedAt = millis();
        bool heldLow = true;
        while (millis() - buttonDetectedAt < START_DEBOUNCE_MS) {
            if (digitalRead(ROUND_BUTTON) != LOW) {
                heldLow = false;
                break;
            }
        }
        if (!heldLow) {
            continue;
        }

        unsigned long countdownStart = millis();
        inhibitMotionUntil(countdownStart + START_COUNTDOWN_MS);

        // Sensors may be read during the countdown, but no motor command can
        // produce movement until the deadline — drive() enforces that
        // centrally, so nothing here can accidentally bypass it. An edge is
        // deliberately NOT recovered here: moving before five seconds is a
        // rulebook warning, and a warning costs more than a bad start spot.
        unsigned long lastEdgeCheck = countdownStart;
        bool stillArmed = true;
        while (millis() - countdownStart < START_COUNTDOWN_MS) {
            if (digitalRead(START_BUTTON) != LOW) {
                stillArmed = false;
                stopMotors();
                break;
            }
            unsigned long now = millis();
            if (now - lastEdgeCheck >= START_EDGE_CHECK_INTERVAL_MS) {
                lastEdgeCheck = now;
                readEdgeSensors();       // keeps the confirmation filter warm
                readOpponentSensors();   // keeps the median window warm
            }
        }

        if (!stillArmed) {
            continue;
        }

        // Round boundary. No search or attack state may leak from the
        // previous round.
        cancelAttack();
        beginSearchArc(nextSearchDirection);
        nextSearchDirection =
            (nextSearchDirection == SEARCH_LEFT) ? SEARCH_RIGHT : SEARCH_LEFT;
        return;
    }
}

// ===================== ATTACK COMMIT LATCH =====================
// See the ATTACK_COMMIT_MS comment in Robot.h for why this exists.

static bool          attackLatched     = false;
static unsigned long attackCommitUntil = 0;

void attack() {
    attackLatched     = true;
    attackCommitUntil = millis() + ATTACK_COMMIT_MS;
    drive(ATTACK_SPEED, ATTACK_SPEED);
}

void holdAttack() {
    drive(ATTACK_SPEED, ATTACK_SPEED);
}

bool attackCommitted() {
    if (!attackLatched) {
        return false;
    }
    // Rollover-safe "has the deadline passed yet".
    if ((long)(millis() - attackCommitUntil) >= 0) {
        attackLatched = false;
        return false;
    }
    return true;
}

void cancelAttack() {
    attackLatched     = false;
    attackCommitUntil = 0;
}

// ===================== EDGE RECOVERY =====================

static bool timeoutRepositionActive = false;

bool edgeRecover(const EdgeReadings &edges) {
    // An edge beats everything, including a push in progress.
    cancelAttack();

    drive(0, 0);
    delay(EDGE_BRAKE_MS);

    unsigned long startTime = millis();
    unsigned long clearedAt = 0;
    bool clearPending = false;
    EdgeReadings initialEdges = edges;

    while (true) {
        EdgeReadings current = readEdgeSensors();
        if (anyEdgeDetected(current)) {
            clearPending = false;
            clearedAt = 0;
        }

        unsigned long elapsed = millis() - startTime;

        if (elapsed > EDGE_RECOVER_MAX_MS) {
            stopMotors();

            bool initialFront = initialEdges.frontLeft || initialEdges.frontRight;
            bool initialBack  = initialEdges.backLeft  || initialEdges.backRight;

            if (initialFront && initialBack) {
                // Edges detected at both ends. There is no direction that is
                // safe to translate in, so hold position and let the main
                // loop drop back to search. Better to be pushed than to
                // drive ourselves out.
                stopMotors();
                return true;
            }

            // DIRECTION OF TRAVEL, not "which edge fired":
            //   front edge fired -> danger is ahead  -> travel BACKWARDS (true)
            //   back edge fired  -> danger is behind -> travel FORWARDS (false)
            timeoutRepositionActive = true;
            reposition(initialFront);
            timeoutRepositionActive = false;

            // Recovery never confirmed a clear edge, so the caller should not
            // trust any positional state it was holding.
            return true;
        }

        int speed = (elapsed > EDGE_ESCALATE_MS) ? EDGE_RECOVER_MAX_SPEED
                                                 : EDGE_RECOVER_SPEED;

        bool retreating = elapsed < EDGE_RETREAT_MS;
        // Hold the original trigger for the mandatory retreat, then switch to
        // live readings so a genuinely clear edge can end recovery instead of
        // pivoting forever on stale state.
        EdgeReadings activeEdges = retreating ? initialEdges : current;
        bool front = activeEdges.frontLeft || activeEdges.frontRight;
        bool back  = activeEdges.backLeft  || activeEdges.backRight;

        if (retreating && front) {
            drive(-speed, -speed);
        }
        else if (retreating && back) {
            drive(speed, speed);
        }
        else if (front && back) {
            // Both ends over the line. Nothing is safe to translate into, so
            // rotate in place and re-evaluate.
            drive(-speed, speed);
        }
        else if (front) {
            // Geometry, so the pivots actually help instead of just spinning:
            //
            // The front-left corner sits forward and to the left of centre.
            // To pull it back over black we need to move BACKWARDS (away from
            // the line) and rotate CLOCKWISE (which carries that corner to
            // the right, toward the middle of the ring). Clockwise means the
            // right wheel goes more negative than the left. Both wheels stay
            // negative so the robot never creeps forward while it turns.
            if (activeEdges.frontLeft && activeEdges.frontRight) {
                // Squarely facing the line. Straight back is exactly right —
                // there is no side to favour.
                drive(-speed, -speed);
            } else if (activeEdges.frontLeft) {
                drive(-speed / 2, -speed);      // reverse + clockwise
            } else {
                drive(-speed, -speed / 2);      // reverse + counter-clockwise
            }
        }
        else if (back) {
            // Mirror image: travel FORWARDS, and rotate so the triggering
            // rear corner sweeps toward the middle. Both wheels stay positive.
            if (activeEdges.backLeft && activeEdges.backRight) {
                drive(speed, speed);
            } else if (activeEdges.backLeft) {
                drive(speed / 2, speed);        // forward + counter-clockwise
            } else {
                drive(speed, speed / 2);        // forward + clockwise
            }
        }
        else {
            // Nothing triggered and the mandatory retreat is over. Stop and
            // require the all-clear to hold briefly before resuming.
            stopMotors();

            if (!clearPending) {
                clearPending = true;
                clearedAt = millis();
            } else if (millis() - clearedAt >= EDGE_CONFIRM_CLEAR_MS) {
                stopMotors();
                return false;
            }
        }
    }
}

bool reposition(bool reverse) {
    unsigned long startTime = millis();
    int speed = reverse ? -REPOSITION_SPEED : REPOSITION_SPEED;

    while (millis() - startTime < REPOSITION_MS) {
        EdgeReadings edges = readEdgeSensors();
        if (anyEdgeDetected(edges)) {
            if (!timeoutRepositionActive) {
                edgeRecover(edges);
                return false;
            }
            // We are already the fallback for a recovery that timed out.
            // Recursing again would just keep nudging toward the line, so
            // stop here and let the caller decide.
            stopMotors();
            return false;
        }
        drive(speed, speed);
    }

    stopMotors();
    return true;
}
