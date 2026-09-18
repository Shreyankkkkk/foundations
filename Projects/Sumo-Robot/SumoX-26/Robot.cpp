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

void initRobot()
{
    initMotors();
    initSensors();

    pinMode(START_BUTTON, INPUT_PULLUP);
    pinMode(ROUND_BUTTON, INPUT_PULLUP);
}

void waitForStart()
{
    stopMotors();

    while (true)
    {
        bool startPressed = digitalRead(START_BUTTON) == LOW;
        bool roundPressed = digitalRead(ROUND_BUTTON) == LOW;

        if (startPressed || roundPressed)
        {
            unsigned long startTime = millis();

            while (millis() - startTime < START_DEBOUNCE_MS)
            {
                if (digitalRead(START_BUTTON) != LOW &&
                    digitalRead(ROUND_BUTTON) != LOW)
                {
                    break;
                }
            }

            if (digitalRead(START_BUTTON) == LOW ||
                digitalRead(ROUND_BUTTON) == LOW)
            {
                break;
            }
        }
    }

    delay(START_COUNTDOWN_MS);
}

void attack()
{
    drive(ATTACK_SPEED, ATTACK_SPEED);
}

bool anyOpponentDetected(const OpponentReadings &readings)
{
    return isOpponentDetected(readings.frontLeft) ||
           isOpponentDetected(readings.frontRight) ||
           isOpponentDetected(readings.left) ||
           isOpponentDetected(readings.right);
}

TargetSide getTargetSide(const OpponentReadings &readings)
{
    int frontLeft = readings.frontLeft;
    int frontRight = readings.frontRight;
    int left = readings.left;
    int right = readings.right;

    int strongest = max(max(frontLeft, frontRight), max(left, right));

    if (strongest < DIST_THRESHOLD)
    {
        return TARGET_NONE;
    }

    // front sensors win if they are the strongest
    if (frontLeft >= frontRight && frontLeft >= left && frontLeft >= right)
        return TARGET_FRONT;
    if (frontRight >= frontLeft && frontRight >= left && frontRight >= right)
        return TARGET_FRONT;

    if (left >= right && left >= DIST_THRESHOLD)
        return TARGET_LEFT;
    if (right >= left && right >= DIST_THRESHOLD)
        return TARGET_RIGHT;

    return TARGET_NONE;
}

static SearchDirection currentDir = SEARCH_LEFT;
static unsigned long lastArcSwitchTime = 0;
static bool firstArcCompleted = false;

void beginSearchArc(SearchDirection initialDir)
{
    currentDir = initialDir;
    lastArcSwitchTime = millis();
    firstArcCompleted = false;
}

void updateSearchArc()
{
    unsigned long now = millis();
    unsigned long targetInterval = firstArcCompleted ? SEARCH_ARC_FLIP_MS : SEARCH_FIRST_ARC_MS;

    if (now - lastArcSwitchTime >= targetInterval)
    {
        currentDir = (currentDir == SEARCH_LEFT) ? SEARCH_RIGHT : SEARCH_LEFT;
        lastArcSwitchTime = now;
        firstArcCompleted = true;
    }

    if (currentDir == SEARCH_LEFT)
    {
        drive(SEARCH_SLOW_SPEED, SEARCH_FAST_SPEED);
    }
    else
    {
        drive(SEARCH_FAST_SPEED, SEARCH_SLOW_SPEED);
    }
}

void approachTarget(const OpponentReadings &readings)
{
    int left = readings.left;
    int right = readings.right;
    int front = max(readings.frontLeft, readings.frontRight);
    int side = max(left, right);

    // Commit when a front sensor sees the opponent at least as strongly as the
    // strongest side sensor. Side reflections must not reduce push power.
    if (front >= DIST_THRESHOLD && front >= side)
    {
        attack();
        return;
    }

    // Turn toward the stronger side while keeping forward motion
    if (right > left + SIDE_TURN_MARGIN)
    {
        drive(APPROACH_SPEED, TURN_SPEED);
        return;
    }

    if (left > right + SIDE_TURN_MARGIN)
    {
        drive(TURN_SPEED, APPROACH_SPEED);
        return;
    }

    // No meaningful steering error: drive straight rather than introducing
    // a permanent turn bias.
    drive(APPROACH_SPEED, APPROACH_SPEED);
}

void edgeRecover(EdgeReadings edges)
{
    drive(0, 0);
    delay(EDGE_BRAKE_MS);

    unsigned long startTime = millis();
    unsigned long clearedAt = 0;
    EdgeReadings activeEdges = edges;

    while (true)
    {
        EdgeReadings current = readEdgeSensors();
        if (anyEdgeDetected(current))
        {
            activeEdges = current;
            clearedAt = 0;
        }

        unsigned long elapsed = millis() - startTime;

        if (elapsed > EDGE_RECOVER_MAX_MS)
        {
            stopMotors();
            return;
        }

        int speed = (elapsed > EDGE_ESCALATE_MS)
                        ? EDGE_RECOVER_MAX_SPEED
                        : EDGE_RECOVER_SPEED;

        bool front = activeEdges.frontLeft || activeEdges.frontRight;
        bool back = activeEdges.backLeft || activeEdges.backRight;
        bool retreating = elapsed < EDGE_RETREAT_MS;
        bool pivoting = elapsed < EDGE_RETREAT_MS + EDGE_PIVOT_MS;

        // Complete a minimum retreat before pivoting. A clear sensor reading
        // must not terminate recovery during either required movement phase.
        if (retreating && front)
        {
            drive(-speed, -speed);
        }
        else if (retreating && back)
        {
            drive(speed, speed);
        }
        else if (pivoting && front && back)
        {
            drive(speed, -speed);
        }
        else if (pivoting && front)
        {
            if (activeEdges.frontLeft && activeEdges.frontRight)
            {
                drive(speed, -speed);
            }
            else if (activeEdges.frontLeft)
            {
                drive(speed, -speed);
            }
            else
            {
                drive(-speed, speed);
            }
        }
        else if (pivoting && back)
        {
            if (activeEdges.backLeft && activeEdges.backRight)
            {
                drive(speed, -speed);
            }
            else if (activeEdges.backLeft)
            {
                drive(-speed, speed);
            }
            else
            {
                drive(speed, -speed);
            }
        }
        else
        {
            stopMotors();

            // Only begin clear confirmation after the minimum maneuver has
            // completed, preventing retreat from cancelling the pivot phase.
            if (clearedAt == 0)
            {
                clearedAt = millis();
            }
            else if (millis() - clearedAt >= EDGE_CONFIRM_CLEAR_MS)
            {
                stopMotors();
                return;
            }
        }
    }
}

void reposition(bool back)
{
    unsigned long startTime = millis();
    int speed = back ? -REPOSITION_SPEED : REPOSITION_SPEED;

    while (millis() - startTime < REPOSITION_MS)
    {
        EdgeReadings edges = readEdgeSensors();
        if (anyEdgeDetected(edges))
        {
            edgeRecover(edges);
            return;
        }

        drive(speed, speed);
    }

    stopMotors();
}