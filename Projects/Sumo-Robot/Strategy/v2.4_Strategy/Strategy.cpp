#include <Arduino.h>
#include <math.h>
#include "Hardware.h"
#include "Sensors.h"
#include "Map.h"
#include "Strategy.h"

static StrategyState state = STATE_OPEN_SWEEP;
static int lastSeenSign = 0; // +1 last seen left, -1 last seen right, 0 unknown

// ALIGN
static bool alignTowardLeft = true;
static unsigned long alignStartMs = 0;
static int lastAlignDir = 0;
static int alignFlipCount = 0;

// COMMIT
static unsigned long commitStartMs = 0;
static unsigned long contactStartMs = 0;
static unsigned long lastDetectMs = 0;

// RETURN
enum ReturnPhase
{
    RETURN_TURNING,
    RETURN_TRANSLATING
};
static ReturnPhase returnPhase = RETURN_TURNING;

// OPEN_SWEEP
enum SweepLeg
{
    SWEEP_LEG_A,
    SWEEP_LEG_B
};
static SweepLeg sweepLeg = SWEEP_LEG_A;
static unsigned long sweepLegStartMs = 0;
static bool sweepDirIsLeftFirst = true;

// STALEMATE_BREAK
static unsigned long stalemateBreakStartMs = 0;

static int stalemateBreakCount = 0;
static int stalemateBreakTrim = 0;

// SEARCH ENTER
static bool searchDirLeft = true;
static float searchSweepDeg = 0.0f;
static bool searchDwelling = false;
static unsigned long searchDwellStartMs = 0;
static int searchLegsCompleted = 0;

static void enterCommit()
{
    state = STATE_COMMIT;
    commitStartMs = millis();
    contactStartMs = 0;
    lastDetectMs = millis(); // lost-target grace always starts from entry, never from a stale timestamp
    alignFlipCount = 0;
    lastAlignDir = 0;
}

static void enterSearch()
{
    alignFlipCount = 0; // a new engagement must not inherit flips from an old one
    lastAlignDir = 0;
    state = STATE_SEARCH;
    searchDirLeft = (lastSeenSign >= 0);
    searchSweepDeg = 0.0f;
    searchDwelling = false;
    searchLegsCompleted = 0; // add this line
}

static int proportionalMag(int raw, int cap)
{
    return (int)constrain((raw - STRONG_THRESHOLD) * ALIGN_PROPORTIONAL_GAIN, 0.0f, (float)cap);
}

// Matches v4's RAM_ALIGN_LEFT/RIGHT wheel signs exactly — same unresolved polarity flag
// carried forward from v4 (bench-verify: does towardLeft=true actually turn toward the
// physical left sensor?). See G0 note at the end.
static MotorCommand spinCommand(bool towardLeft, int pwmMag)
{
    MotorCommand c;
    // towardLeft == CCW turn == right wheel drives forward, left wheel backward.
    // Matches Map's convention (right faster -> CCW), COMMIT's trim sign and RETURN's delta>0 logic.
    if (towardLeft)
    {
        c.leftPwm = -pwmMag;
        c.rightPwm = +pwmMag;
    }
    else
    {
        c.leftPwm = +pwmMag;
        c.rightPwm = -pwmMag;
    }
    return c;
}

static int cmsToPwm(float cms)
{
    return (int)constrain((cms / DRIVE_SPEED_MAX_CMS) * DRIVE_PWM_MAX, 0.0f, (float)DRIVE_PWM_MAX);
}

static void enterAlign(bool towardLeft)
{
    int dir = towardLeft ? +1 : -1;
    if (lastAlignDir != 0 && dir != lastAlignDir)
        alignFlipCount++;
    lastAlignDir = dir;
    if (alignFlipCount >= ALIGN_FLIP_LIMIT)
    {
        enterCommit();
        return;
    }
    state = STATE_ALIGN;
    alignStartMs = millis();
    alignTowardLeft = towardLeft;
}

static void enterFromDetection(const OpponentDetection &d)
{
    if (d.center)
    {
        enterCommit();
    }
    else if (d.left)
    {
        alignFlipCount = 0;
        lastAlignDir = 0;
        enterAlign(true);
    }
    else if (d.right)
    {
        alignFlipCount = 0;
        lastAlignDir = 0;
        enterAlign(false);
    }
    else
        enterSearch();
    ;
}

void resetStrategy(bool seenAtKickoff)
{
    lastSeenSign = 0;
    alignFlipCount = 0;
    lastAlignDir = 0;
    contactStartMs = 0;
    stalemateBreakCount = 0;
    searchLegsCompleted = 0;
    if (seenAtKickoff)
    {
        enterFromDetection(getOpponentDetection());
    }
    else
    {
        state = STATE_OPEN_SWEEP;
        sweepLeg = SWEEP_LEG_A;
        sweepLegStartMs = millis();
        sweepDirIsLeftFirst = true; // arbitrary default — no prior bearing exists at first kickoff
    }
}

void strategyForceCommit()
{
    enterCommit();
}

void strategyForceReturn()
{
    if (!isMapVoid())
    {
        state = STATE_RETURN;
        returnPhase = RETURN_TURNING;
    }
    else
        enterSearch();
    ;
}

void strategyEngage()
{
    enterFromDetection(getOpponentDetection());
}

static bool rearClearForBackoff()
{
    return !isMapVoid() && (getRearMaxRadius() + getUncertainty() + STALEMATE_BACKOFF_CM <= ARENA_RADIUS_CM);
}

StrategyState getStrategyState() { return state; }

MotorCommand updateStrategy(const OpponentDetection &d)
{
    if (d.left)
        lastSeenSign = +1;
    if (d.right)
        lastSeenSign = -1;

    switch (state)
    {

    case STATE_OPEN_SWEEP:
    {
        if (d.center)
        {
            enterCommit();
            return {0, 0};
        }
        if (d.left)
        {
            enterAlign(true);
            return {0, 0};
        }
        if (d.right)
        {
            enterAlign(false);
            return {0, 0};
        }

        unsigned long elapsed = millis() - sweepLegStartMs;
        if (sweepLeg == SWEEP_LEG_A)
        {
            if (elapsed > OPEN_SWEEP_LEG_A_MS)
            {
                sweepLeg = SWEEP_LEG_B;
                sweepLegStartMs = millis();
                return {0, 0};
            }
            return spinCommand(sweepDirIsLeftFirst, SEARCH_SPIN_PWM);
        }
        if (elapsed > OPEN_SWEEP_LEG_B_MS)
        {
            enterSearch();
            ;
            return {0, 0};
        }
        return spinCommand(!sweepDirIsLeftFirst, SEARCH_SPIN_PWM);
    }

    case STATE_SEARCH:
    {
        if (d.center)
        {
            enterCommit();
            return {0, 0};
        }
        if (d.left)
        {
            enterAlign(true);
            return {0, 0};
        }
        if (d.right)
        {
            enterAlign(false);
            return {0, 0};
        }

        if (searchDwelling)
        {
            if (millis() - searchDwellStartMs >= SEARCH_DWELL_MS)
            {
                searchDwelling = false;
                searchSweepDeg = 0.0f;
                searchDirLeft = !searchDirLeft;
                searchLegsCompleted++;
                if (searchLegsCompleted >= 1)
                { // one full local sweep, both directions, nothing found
                    if (!isMapVoid() && shouldReturn())
                    {
                        state = STATE_RETURN;
                        returnPhase = RETURN_TURNING;
                    }
                    else
                        searchLegsCompleted = 0; // already near center, or map unreliable — keep searching locally
                }
            }
            return {0, 0};
        }

        float spinRateDegS = searchDirLeft ? SPIN_RATE_CCW_DEGS : SPIN_RATE_CW_DEGS;
        searchSweepDeg += spinRateDegS * (SEARCH_SPIN_PWM / 255.0f) * (CONTROL_TICK_MS / 1000.0f);

        if (searchSweepDeg >= SEARCH_COVERAGE_SWEEP_DEG)
        {
            searchDwelling = true;
            searchDwellStartMs = millis();
            return {0, 0};
        }
        return spinCommand(searchDirLeft, SEARCH_SPIN_PWM);
    }

    case STATE_ALIGN:
    {
        if (d.center)
        {
            enterCommit();
            return {0, 0};
        }
        if (!d.left && !d.right)
        {
            enterSearch();
            ;
            return {0, 0};
        }

        bool stillLeft = d.left && !d.right;
        bool stillRight = d.right && !d.left;
        if (alignTowardLeft && stillRight)
        {
            enterAlign(false);
            return {0, 0};
        }
        if (!alignTowardLeft && stillLeft)
        {
            enterAlign(true);
            return {0, 0};
        }

        if (millis() - alignStartMs > ALIGN_TIMEOUT_MS)
        {
            enterCommit();
            return {0, 0};
        }

        int raw = alignTowardLeft ? getOpponentReadings().left : getOpponentReadings().right;
        int mag = ALIGN_BASE_SPEED + proportionalMag(raw, ALIGN_PROPORTIONAL_MAX_BIAS);
        return spinCommand(alignTowardLeft, mag);
    }

    case STATE_COMMIT:
    {
        bool seen = anyOpponentDetected(d);
        bool contact = anyContact(d);
        if (seen)
            lastDetectMs = millis();

        // Late-arrival: opponent already in the contact band at first detection, so the
        // near-latch (needs the 600-700 peak first) never set. Only feeds the stalemate
        // timer — never the full-power decision, so anyContact()'s disambiguation elsewhere
        // (push governor, edge-recovery bail, map contact mode) is untouched.
        int centerRaw = getOpponentReadings().center;
        bool centerSustainedBand = d.center && centerRaw >= CONTACT_BAND_LOW && centerRaw <= CONTACT_BAND_HIGH;

        int trim = 0;
        if (!d.center)
        {
            if (d.left && !d.right)
                trim = -proportionalMag(getOpponentReadings().left, COMMIT_TRACK_TRIM_MAX);
            else if (d.right && !d.left)
                trim = proportionalMag(getOpponentReadings().right, COMMIT_TRACK_TRIM_MAX);
        }

        if (contact || centerSustainedBand)
        {
            if (contactStartMs == 0)
                contactStartMs = millis();
            if (millis() - contactStartMs > STALEMATE_TIMEOUT_MS && rearClearForBackoff())
            {
                state = STATE_STALEMATE_BREAK;
                stalemateBreakStartMs = millis();
                stalemateBreakCount++;
                stalemateBreakTrim = (stalemateBreakCount % 2 == 0) ? STALEMATE_BREAK_TRIM : -STALEMATE_BREAK_TRIM;
                return MotorCommand{-EDGE_RECOVER_SPEED + stalemateBreakTrim, -EDGE_RECOVER_SPEED - stalemateBreakTrim};
            }
        }
        else
        {
            contactStartMs = 0;
        }

        if (contact)
        {
            return MotorCommand{DRIVE_PWM_MAX + trim, DRIVE_PWM_MAX - trim};
        }

        if (!seen && (millis() - lastDetectMs > LOST_CONTACT_GRACE_MS))
        {
            enterSearch();
            return {0, 0};
        }

        unsigned long elapsedMs = millis() - commitStartMs;
        float rampFraction = fminf(1.0f, (elapsedMs / 1000.0f) / COMMIT_SOFT_START_S);
        int rampPwm = (int)(rampFraction * DRIVE_PWM_MAX);
        int governedPwm = isMapVoid() ? COMMIT_VOID_PWM : cmsToPwm(getGovernedMaxSpeedCms());
        if (governedPwm < MIN_MOVE_PWM)
            governedPwm = MIN_MOVE_PWM; // governor may slow us, never freeze us
        int basePwm = (rampPwm < governedPwm) ? rampPwm : governedPwm;
        return MotorCommand{basePwm + trim, basePwm - trim};
    }

    case STATE_STALEMATE_BREAK:
    {
        if (millis() - stalemateBreakStartMs > STALEMATE_BACKOFF_MS)
        {
            enterFromDetection(d);
            return {0, 0};
        }
        return MotorCommand{-EDGE_RECOVER_SPEED + stalemateBreakTrim, -EDGE_RECOVER_SPEED - stalemateBreakTrim};
    }

    case STATE_RETURN:
    {
        if (anyOpponentDetected(d) && (d.center || getRadiusFromCenter() + ROBOT_R_SWING_CM <= ARENA_OUT_RADIUS_CM))
        {
            enterFromDetection(d);
            return {0, 0};
        } // non-negotiable abort check

        if (returnPhase == RETURN_TURNING)
        {
            float delta = getReturnTurnDeltaDeg();
            if (fabsf(delta) <= RETURN_HEADING_TOLERANCE_DEG)
            {
                returnPhase = RETURN_TRANSLATING;
                return {0, 0};
            }
            bool towardLeft = delta > 0; // assumes towardLeft=true => CCW/+theta — verify alongside G0
            return spinCommand(towardLeft, SEARCH_SPIN_PWM);
        }

        if (getRadiusFromCenter() <= getUncertainty())
        {
            enterSearch();
            ;
            return {0, 0};
        }
        int pwm = cmsToPwm(getGovernedMaxSpeedCms());
        if (pwm < MIN_MOVE_PWM) pwm = MIN_MOVE_PWM;
        return MotorCommand{pwm, pwm};
    }
    }
    return {0, 0};
}