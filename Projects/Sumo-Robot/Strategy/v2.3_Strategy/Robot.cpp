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
    int speed = anyContact(getOpponentDetection()) ? DRIVE_PWM_MAX : EDGE_RECOVER_SPEED; // in contact: full effort, 170 loses the push
    int baseSpeed = edgeFrontTriggered ? -speed : speed;
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
    drive(leftPwm, rightPwm, true);
    mapUpdateMotion(leftPwm, rightPwm, dtMs);
}

static bool buttonDown(int pin) { return (digitalRead(pin) == HIGH) != BUTTON_ACTIVE_LOW; }

// Blocks until `pin` has been RELEASED for a stable window and then PRESSED for a stable window.
// Requiring release first means a held/stuck/shorted button can never trigger anything, and a
// button still held from the previous step must be let go and pressed again.
// Motors are forced to 0 the whole time; sensors are polled if they are already powered.
static void waitForPress(int pin, bool pollSensors)
{
    unsigned long t = millis();
    while (millis() - t < BUTTON_DEBOUNCE_MS)
    {
        stopMotors();
        if (pollSensors) updateOpponentSensors();
        if (buttonDown(pin)) t = millis();
        delay(1);
    }
    t = millis();
    while (millis() - t < BUTTON_DEBOUNCE_MS)
    {
        stopMotors();
        if (pollSensors) updateOpponentSensors();
        if (!buttonDown(pin)) t = millis();
        delay(1);
    }
}

static bool constantsValid()
{
    return DRIVE_SPEED_MAX_CMS > 0 && SPIN_RATE_CW_DEGS > 0 && SPIN_RATE_CCW_DEGS > 0 &&
           STOP_DISTANCE_CM > 0 && FRICTION_MU > 0 && DETECT_RANGE_MAX_CM > 0 &&
           isfinite(DRIVE_DECEL_CMS2) && isfinite(COMMIT_SOFT_START_S) && isfinite(SEARCH_SPIN_CAP_DEGS) &&
           isfinite(ALIGN_ACTUAL_SPIN_DEGS) && ALIGN_ACTUAL_SPIN_DEGS > 0 &&
           SEARCH_SPIN_PWM > 0 && OPEN_SWEEP_LEG_A_MS > 0 && ALIGN_TIMEOUT_MS > 0 &&
           ADC_OVERSAMPLE_N >= 1 && ADC_OVERSAMPLE_N <= ADC_OVERSAMPLE_MAX &&
           WEAK_THRESHOLD < STRONG_THRESHOLD && STRONG_THRESHOLD < NEAR_THRESHOLD;
}

// STAGES 2-4: idle until BUTTON 2, mandatory 5 s stationary delay, then hand over to the strategy.
static void armAndStart()
{
    stopMotors();
    initMap();
    primeOpponentSensors();
    waitForPress(START_BUTTON_PIN, true); // STAGE 2

    unsigned long holdStart = millis(); // STAGE 3
    while (millis() - holdStart < START_COUNTDOWN_MS)
    {
        stopMotors();
        updateOpponentSensors();
    }

    resetStrategy(anyOpponentDetected(getOpponentDetection())); // STAGE 4
    edgePhase = EDGE_RECOVERY_IDLE;
    doubleEdgeActive = false;
    lastTickMs = millis();
}

void initRobot()
{
    // STAGE 0 - boot: everything off. Drivers disabled, no sensor reads, no logic.
    disableMotorDrivers();
    if (!constantsValid())
        while (true) delay(1000); // bad/zero/NaN constant: stay dead at the bench instead of driving on garbage
    pinMode(POWER_BUTTON_PIN, BUTTON_ACTIVE_LOW ? INPUT_PULLUP : INPUT);
    pinMode(START_BUTTON_PIN, BUTTON_ACTIVE_LOW ? INPUT_PULLUP : INPUT);

    // STAGE 1 - BUTTON 1 (A3): power up. Drivers enabled (PWM 0), sensors live. NO logic, no timers.
    waitForPress(POWER_BUTTON_PIN, false);
    initMotors();
    initSensors();
    armAndStart();
}

static void handleDoubleEdgeTick(const EdgeReadings &e, unsigned long dtMs)
{
    if (!e.front || !e.back) { stopMotors(); doubleEdgeActive = false; return; }
    if (millis() - doubleEdgeStartMs > DOUBLE_EDGE_RECOVER_MAX_MS) { stopMotors(); doubleEdgeActive = false; return; }

    int speed = doubleEdgeDriveForward ? EDGE_RECOVER_SPEED : -EDGE_RECOVER_SPEED;
    drive(speed, speed, true);
    mapUpdateMotion(speed, speed, dtMs);
}

void robotLoop()
{
    unsigned long now = millis();
    if (now - lastTickMs < CONTROL_TICK_MS)
        return;
    unsigned long dtMs = now - lastTickMs;
    lastTickMs = now;

    if (REARM_ENABLED)
    { // hold BUTTON 2 for REARM_HOLD_MS: stop and re-arm (round 2, referee reset) without a power cycle
        static unsigned long heldSince = 0;
        if (buttonDown(START_BUTTON_PIN))
        {
            if (heldSince == 0) heldSince = now;
            if (now - heldSince >= REARM_HOLD_MS)
            {
                heldSince = 0;
                armAndStart();
                return;
            }
        }
        else
            heldSince = 0;
    }

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