// ============================================================================
// SumoX-26 — Robot.cpp
// ----------------------------------------------------------------------------
// Shared sumo-specific behavior — attack, edge recovery, repositioning,
// startup — that both Strategy1 and Strategy2 call into. Nothing in here
// is strategy-specific (no P-controller math, no search-arc speeds); if
// it's identical for both strategies, it lives here instead of being
// duplicated in Strategy1.cpp and Strategy2.cpp.
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
    static SearchDirection nextSearchDirection = SEARCH_LEFT;

    while (true) {
        if (digitalRead(START_BUTTON) != LOW) {
            stopMotors();
            continue;
        }

        bool roundPressed = digitalRead(ROUND_BUTTON) == LOW;

        if (roundPressed) {
            unsigned long buttonDetectedAt = millis();
            bool heldLow = true;

            while (millis() - buttonDetectedAt < START_DEBOUNCE_MS) {
                if (digitalRead(ROUND_BUTTON) != LOW)
                {
                    heldLow = false;
                    break;
                }
            }

            if (heldLow) {
                unsigned long countdownStart = millis();
                inhibitMotionUntil(countdownStart + START_COUNTDOWN_MS);

                // The countdown starts at the first confirmed button
                // detection. Sensors may be read during it, but no motor
                // command can produce movement until the deadline.
                // Keep the mandatory countdown sensor-aware without allowing
                // movement. An edge is intentionally not recovered here:
                // moving before five seconds is a rule violation.
                unsigned long lastEdgeCheck = countdownStart;
                bool stillArmed = true;
                while (millis() - countdownStart < START_COUNTDOWN_MS)
                {
                    if (digitalRead(START_BUTTON) != LOW) {
                        stillArmed = false;
                        stopMotors();
                        break;
                    }

                    unsigned long now = millis();
                    if (now - lastEdgeCheck >= START_EDGE_CHECK_INTERVAL_MS) {
                        lastEdgeCheck = now;
                        readEdgeSensors();
                    }
                }

                if (!stillArmed) {
                    continue;
                }

                // This is the round boundary. Callers may immediately
                // override the direction, but no search state can leak from
                // the previous round.
                beginSearchArc(nextSearchDirection);
                nextSearchDirection = (nextSearchDirection == SEARCH_LEFT)
                    ? SEARCH_RIGHT
                    : SEARCH_LEFT;
                return;
            }
        }
    }
}

void attack() {
    drive(ATTACK_SPEED, ATTACK_SPEED);
}

static bool timeoutRepositionActive = false;

bool edgeRecover(const EdgeReadings &edges) {
    drive(0, 0);
    delay(EDGE_BRAKE_MS);

    unsigned long startTime = millis();
    unsigned long clearedAt = 0;
    EdgeReadings initialEdges = edges;
    bool initialFront = edges.frontLeft || edges.frontRight;

    while (true) {
        EdgeReadings current = readEdgeSensors();
        if (anyEdgeDetected(current)) {
            clearedAt = 0;
        }

        unsigned long elapsed = millis() - startTime;

        if (elapsed > EDGE_RECOVER_MAX_MS) {
            stopMotors();
            timeoutRepositionActive = true;
            bool repositioned = reposition(!initialFront);
            timeoutRepositionActive = false;
            return !repositioned;
        }

        int speed = (elapsed > EDGE_ESCALATE_MS)
                        ? EDGE_RECOVER_MAX_SPEED
                        : EDGE_RECOVER_SPEED;

        bool retreating = elapsed < EDGE_RETREAT_MS;
        // Preserve the original trigger only for the mandatory retreat.
        // After that phase, use live readings so a clear edge can be
        // confirmed instead of pivoting on stale sensor state.
        EdgeReadings activeEdges = retreating ? initialEdges : current;
        bool front = activeEdges.frontLeft || activeEdges.frontRight;
        bool back = activeEdges.backLeft || activeEdges.backRight;

        // Complete a minimum retreat before pivoting. A clear sensor reading
        // must not terminate recovery during either required movement phase.
        if (retreating && front) {
            drive(-speed, -speed);
        }
        else if (retreating && back) {
            drive(speed, speed);
        }
        else if (front && back) {
            drive(-speed, speed);
        }
        else if (front)
        {
            if (activeEdges.frontLeft && activeEdges.frontRight) {
                // Both front sensors are ambiguous; use the established
                // front-left-safe pivot as the deterministic fallback.
                drive(-speed, speed / 2);
            }
            else if (activeEdges.frontLeft) {
                drive(-speed, speed / 2);
            }
            else {
                drive(-speed / 2, speed);
            }
        }
        else if (back) {
            if (activeEdges.backLeft && activeEdges.backRight) {
                // Both back sensors are ambiguous; use the established
                // back-left-safe pivot as the deterministic fallback.
                drive(speed / 2, -speed);
            }
            else if (activeEdges.backLeft) {
                drive(speed / 2, -speed);
            }
            else {
                drive(speed, -speed / 2);
            }
        }
        else {
            stopMotors();

            // Only begin clear confirmation after the minimum maneuver has
            // completed, preventing retreat from cancelling the pivot phase.
            if (!anyEdgeDetected(current) && clearedAt == 0) {
                clearedAt = millis();
            }
            else if (millis() - clearedAt >= EDGE_CONFIRM_CLEAR_MS) {
                stopMotors();
                return false;
            }
        }
    }
}

bool reposition(bool back) {
    unsigned long startTime = millis();
    int speed = back ? -REPOSITION_SPEED : REPOSITION_SPEED;

    while (millis() - startTime < REPOSITION_MS) {
        EdgeReadings edges = readEdgeSensors();
        if (anyEdgeDetected(edges)) {
            if (!timeoutRepositionActive) {
                edgeRecover(edges);
                return false;
            }

            // The fallback is already running from a recovery timeout. Do not
            // ignore a newly detected edge and continue driving off the ring.
            stopMotors();
            return false;
        }
        drive(speed, speed);
    }
    stopMotors();
    return true;
}