#include <Arduino.h>
#include <math.h>
#include "Hardware.h"
#include "Sensors.h"
#include "Map.h"

static float x, y, thetaDeg;
static float U;
static float pathSinceAnchor;    // cm, for k_err-scaled uncertainty
static float turnSinceAnchor;    // deg, for eps_spin-scaled uncertainty
static float contactUncertainty; // cm, raw worst-case additive during contact

static float normalizeDeg180(float deg)
{
    while (deg > 180.0f)
        deg -= 360.0f;
    while (deg < -180.0f)
        deg += 360.0f;
    return deg;
}

static float headingUncertaintyDeg;

static void recomputeU()
{
    float headingInducedDriftCm = pathSinceAnchor * sinf(headingUncertaintyDeg * DEG_TO_RAD);
    U = U0_POSITION_CM + K_ERR_PATH_FACTOR * pathSinceAnchor + SPIN_DRIFT_PER_REV_CM * (turnSinceAnchor / 360.0f) + headingInducedDriftCm + contactUncertainty;
}

void initMap()
{
    x = -START_POSE_RADIUS_CM;
    y = 0.0f;
    thetaDeg = 0.0f;
    pathSinceAnchor = 0.0f;
    turnSinceAnchor = 0.0f;
    contactUncertainty = 0.0f;
    headingUncertaintyDeg = THETA0_UNCERTAINTY_DEG; // only ever set here — nothing mid-round corrects heading
    recomputeU();
}

void mapUpdateMotion(int leftPwm, int rightPwm, unsigned long dtMs)
{
    float dtSec = dtMs / 1000.0f;

    float commonPwm = (leftPwm + rightPwm) / 2.0f;
    float diffPwm = (rightPwm - leftPwm) / 2.0f; // >0 -> right faster -> CCW turn (matches omega=(vR-vL)/T convention)

    float v = (commonPwm / 255.0f) * DRIVE_SPEED_MAX_CMS;
    float spinRate = (diffPwm >= 0) ? SPIN_RATE_CCW_DEGS : SPIN_RATE_CW_DEGS;
    float omega = (diffPwm / 255.0f) * spinRate; // approximation: assumes turning dynamics scale the same in blended motion as in pure spin

    thetaDeg = normalizeDeg180(thetaDeg + omega * dtSec);
    float thetaRad = thetaDeg * DEG_TO_RAD;
    x += v * dtSec * cosf(thetaRad);
    y += v * dtSec * sinf(thetaRad);

    pathSinceAnchor += fabsf(v) * dtSec;
    turnSinceAnchor += fabsf(omega) * dtSec;
    headingUncertaintyDeg += HEADING_DRIFT_PER_REV_DEG * (fabsf(omega) * dtSec / 360.0f);
    recomputeU();
}

void mapUpdateContact(unsigned long dtMs)
{
    // Winning vs. losing a push is unknowable without force/current sensing, which we don't
    // have. Rather than assume forward progress (confidently wrong whenever we're the one
    // being pushed back), leave x,y unmoved and let uncertainty grow to reflect that we could
    // have shifted this far in either direction. A real edge touch is still caught independently,
    // regardless of this estimate.
    float dtSec = dtMs / 1000.0f;
    contactUncertainty += DRIVE_SPEED_MAX_CMS * dtSec;
    recomputeU();
}

void mapSnapEdge(bool frontTriggered)
{
    float offset = frontTriggered ? EDGE_SENSOR_FRONT_OFFSET_CM : -EDGE_SENSOR_BACK_OFFSET_CM;
    float thetaRad = thetaDeg * DEG_TO_RAD;
    float sensorX = x + offset * cosf(thetaRad);
    float sensorY = y + offset * sinf(thetaRad);

    float sensorAngle = atan2f(sensorY, sensorX);
    float newSensorX = ARENA_RADIUS_CM * cosf(sensorAngle);
    float newSensorY = ARENA_RADIUS_CM * sinf(sensorAngle);

    x = newSensorX - offset * cosf(thetaRad);
    y = newSensorY - offset * sinf(thetaRad);

    pathSinceAnchor = 0.0f;
    turnSinceAnchor = 0.0f;
    contactUncertainty = 0.0f;
    // headingUncertaintyDeg intentionally NOT reset — an edge touch confirms position, not facing direction
    recomputeU();
}

Pose getPose()
{
    Pose p;
    p.x = x;
    p.y = y;
    p.thetaDeg = thetaDeg;
    return p;
}

float getRadiusFromCenter() { return hypotf(x, y); }
float getUncertainty() { return U; }

static float cornerRadius(float localX, float localY)
{
    float thetaRad = thetaDeg * DEG_TO_RAD;
    float wx = x + localX * cosf(thetaRad) - localY * sinf(thetaRad);
    float wy = y + localX * sinf(thetaRad) + localY * cosf(thetaRad);
    return hypotf(wx, wy);
}

float getFootprintMaxRadius()
{
    float halfW = ROBOT_WIDTH_CM / 2.0f;
    float r1 = cornerRadius(ROBOT_L_F_CM, halfW);
    float r2 = cornerRadius(ROBOT_L_F_CM, -halfW);
    float r3 = cornerRadius(-ROBOT_L_B_CM, halfW);
    float r4 = cornerRadius(-ROBOT_L_B_CM, -halfW);
    return fmaxf(fmaxf(r1, r2), fmaxf(r3, r4));
}

bool isMapVoid()
{
    return U >= (ARENA_RADIUS_CM - ROBOT_R_SWING_CM - STOP_DISTANCE_CM);
}

bool isEdgeReadingImplausible()
{
    if (isMapVoid())
        return false; // never suppress when position isn't trustworthy
    float margin = ARENA_RADIUS_CM - (getFootprintMaxRadius() + getUncertainty());
    return margin >= ROBOT_R_SWING_CM; // must be at least one full swing-radius of slack
}

float getReturnHeadingDeg()
{
    return atan2f(-y, -x) * RAD_TO_DEG;
}

float getReturnTurnDeltaDeg()
{
    return normalizeDeg180(getReturnHeadingDeg() - thetaDeg);
}

bool shouldReturn()
{
    return getRadiusFromCenter() > (U + ROBOT_WIDTH_CM / 2.0f);
}

float getGovernedMaxSpeedCms()
{
    float rMax = getFootprintMaxRadius();
    float margin = ARENA_RADIUS_CM - U - rMax;
    if (margin <= 0.0f)
        return 0.0f;
    return sqrtf(2.0f * DRIVE_DECEL_CMS2 * margin);
}

bool isPhantomDetection(int whichSensor, int rawAdc)
{
    if (isMapVoid()) return false; // never suppress when position isn't trustworthy — same rule as isEdgeReadingImplausible()

    float r = getRadiusFromCenter();
    float phantomRiskRadius = (ARENA_OUT_RADIUS_CM + SAFETY_ZONE_MIN_CM) - DETECT_RANGE_MAX_CM;
    if (r <= phantomRiskRadius)
        return false; // too close to center for a phantom to be geometrically possible

    float range = estimateFarRangeCm(rawAdc);
    float angleOffsetDeg = (whichSensor < 0) ? 45.0f : (whichSensor > 0) ? -45.0f
                                                                         : 0.0f;
    float beamRad = (thetaDeg + angleOffsetDeg) * DEG_TO_RAD;

    float impliedX = x + range * cosf(beamRad);
    float impliedY = y + range * sinf(beamRad);
    float impliedRadius = hypotf(impliedX, impliedY);

    return impliedRadius > ARENA_RADIUS_CM;
}