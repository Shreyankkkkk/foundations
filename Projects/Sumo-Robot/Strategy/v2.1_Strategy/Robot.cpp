#include <Arduino.h>
#include <math.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Map.h"
#include "Strategy.h"
#include "Robot.h"

enum EdgeRecoveryPhase
{
    EDGE_RECOVERY_IDLE,
    EDGE_RECOVERY_ACTIVE
};
static EdgeRecoveryPhase edgePhase = EDGE_RECOVERY_IDLE;
static bool edgeFrontTriggered = false;
static unsigned long edgeRecoverStartMs = 0;
static unsigned long edgeClearedAtMs = 0;
static unsigned long lastTickMs = 0;

static bool doubleEdgeActive = false;
static unsigned long doubleEdgeStartMs = 0;
static bool doubleEdgeDriveForward = true;

static float normalizeDeg180Local(float deg)
{
    while (deg > 180.0f)
        deg -= 360.0f;
    while (deg < -180.0f)
        deg += 360.0f;
    return deg;
}

static void computeEdgeEscapeDrive(int &leftPwm, int &rightPwm)
{
    int baseSpeed = edgeFrontTriggered ? -EDGE_RECOVER_SPEED : EDGE_RECOVER_SPEED;
    int trim = 0;

    if (!isMapVoid())
    { // rarely true right after a snap — U resets to ~U0 on every snap
        float travelHeadingDeg = normalizeDeg180Local(getPose().thetaDeg + (edgeFrontTriggered ? 180.0f : 0.0f));
        float turnDeltaDeg = normalizeDeg180Local(getReturnHeadingDeg() - travelHeadingDeg);
        trim = (int)(EDGE_ESCAPE_TRIM_MAX * sinf(turnDeltaDeg * DEG_TO_RAD)); // sign unverified — bench check, see ALIGN_LEFT precedent
    }

    leftPwm = baseSpeed - trim;
    rightPwm = baseSpeed + trim;
}

static void handleEdgeRecoveryTick(const EdgeReadings &e, unsigned long dtMs)
{
    unsigned long now = millis();
    OpponentDetection d = getOpponentDetection();

    bool oppositeTriggered = edgeFrontTriggered ? e.back : e.front;
    bool stillOnEdge = edgeFrontTriggered ? e.front : e.back;
    bool clearedLongEnough = false;
    bool swingClear = getRadiusFromCenter() + ROBOT_R_SWING_CM <= ARENA_OUT_RADIUS_CM;

    if (stillOnEdge)
    {
        edgeClearedAtMs = 0;
    }
    else if (edgeClearedAtMs == 0)
    {
        edgeClearedAtMs = now;
    }
    else if (now - edgeClearedAtMs > EDGE_CLEAR_CONFIRM_MS + EDGE_OVERRUN_MS && swingClear)
    {
        clearedLongEnough = true;
    }

    bool timedOut = (now - edgeRecoverStartMs) > EDGE_RECOVER_MAX_MS;

    if (oppositeTriggered || clearedLongEnough || timedOut)
    {
        stopMotors();
        edgePhase = EDGE_RECOVERY_IDLE;
        if (anyOpponentDetected(d) && !oppositeTriggered && swingClear)
            strategyEngage();      // left/right -> ALIGN, center -> COMMIT
        else
            strategyForceReturn();
        return;
    }

    int leftPwm, rightPwm;
    computeEdgeEscapeDrive(leftPwm, rightPwm);
    drive(leftPwm, rightPwm);
    mapUpdateMotion(leftPwm, rightPwm, dtMs);
}

static bool startButtonPressed() { return digitalRead(START_BUTTON_PIN) == LOW; }

// Blocks until the start button has been pressed (debounced). The button must first be seen
// RELEASED for a stable window, so a stuck/held/shorted button can never auto-start the robot.
// Motors stay stopped the whole time.
static void waitForStartButton()
{
    unsigned long t = millis();
    while (millis() - t < START_BUTTON_DEBOUNCE_MS)
    {
        stopMotors();
        if (startButtonPressed())
            t = millis(); // still pressed (or bouncing) -> restart the released-window
        delay(1);
    }
    t = millis();
    while (millis() - t < START_BUTTON_DEBOUNCE_MS)
    {
        stopMotors();
        if (!startButtonPressed())
            t = millis(); // released/bounced -> restart the pressed-window
        delay(1);
    }
}

void initRobot()
{
    initMotors(); // motors stopped
    pinMode(START_BUTTON_PIN, INPUT_PULLUP);
    initSensors();
    initMap();

    // 1) Robot is powered (switch #1) and idle. Wait for the start button (button #2).
    waitForStartButton();

    // 2) Mandatory 5 s stationary delay, counted from the debounced press. Motors held at 0.
    unsigned long holdStart = millis();
    while (millis() - holdStart < START_COUNTDOWN_MS)
    {
        stopMotors();
        updateOpponentSensors(); // keep confirm-counters settling so kickoff detection is valid
    }

    // 3) Delay over -> strategy begins.
    bool seenAtKickoff = anyOpponentDetected(getOpponentDetection());
    resetStrategy(seenAtKickoff);

    edgePhase = EDGE_RECOVERY_IDLE;
    doubleEdgeActive = false;
    lastTickMs = millis();
}

static void handleDoubleEdgeTick(const EdgeReadings &e, unsigned long dtMs)
{
    if (!e.front || !e.back) { stopMotors(); doubleEdgeActive = false; return; }
    if (millis() - doubleEdgeStartMs > DOUBLE_EDGE_RECOVER_MAX_MS) { stopMotors(); doubleEdgeActive = false; return; }

    int speed = doubleEdgeDriveForward ? EDGE_RECOVER_SPEED : -EDGE_RECOVER_SPEED;
    drive(speed, speed);
    mapUpdateMotion(speed, speed, dtMs);
}

void robotLoop()
{
    unsigned long now = millis();
    if (now - lastTickMs < CONTROL_TICK_MS)
        return;
    unsigned long dtMs = now - lastTickMs;
    lastTickMs = now;

    updateOpponentSensors();
    EdgeReadings e = readEdgeSensors();

    if (e.front && e.back && edgePhase == EDGE_RECOVERY_IDLE)
    {
        if (!doubleEdgeActive)
        {
            doubleEdgeActive = true;
            doubleEdgeStartMs = now;
            Pose p = getPose();
            float thetaRad = p.thetaDeg * DEG_TO_RAD;
            float frontR = hypotf(p.x + ROBOT_L_F_CM * cosf(thetaRad), p.y + ROBOT_L_F_CM * sinf(thetaRad));
            float backR  = hypotf(p.x - ROBOT_L_B_CM * cosf(thetaRad), p.y - ROBOT_L_B_CM * sinf(thetaRad));
            doubleEdgeDriveForward = isMapVoid() ? false : (frontR <= backR);
        }
        handleDoubleEdgeTick(e, dtMs);
        return;
    }

    if ((e.front || e.back) && edgePhase == EDGE_RECOVERY_IDLE)
    {
        OpponentDetection dCheck = getOpponentDetection();
        bool implausible = EDGE_SUPPRESSION_ENABLED && isEdgeReadingImplausible() && !anyContact(dCheck);
        if (!implausible)
        {
            edgeFrontTriggered = e.front;
            edgeRecoverStartMs = now;
            edgeClearedAtMs = 0;
            mapSnapEdge(edgeFrontTriggered);
            edgePhase = EDGE_RECOVERY_ACTIVE;
        }
        // else: worn-patch false positive — no map snap, no state change, falls through to strategy below
    }

    if (edgePhase == EDGE_RECOVERY_ACTIVE)
    {
        handleEdgeRecoveryTick(e, dtMs);
        return;
    }

    OpponentDetection d = getOpponentDetection();
    MotorCommand cmd = updateStrategy(d);
    drive(cmd.leftPwm, cmd.rightPwm);

    if (anyContact(d))
        mapUpdateContact(dtMs);
    else
        mapUpdateMotion(cmd.leftPwm, cmd.rightPwm, dtMs);
}