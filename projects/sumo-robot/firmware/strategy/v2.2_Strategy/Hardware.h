#ifndef HARDWARE_H
#define HARDWARE_H

#include <Arduino.h>
#include <math.h>

// ============================================================
// PIN MAP — unchanged wiring from v4
// ============================================================
const int LEFT_L_EN = 2;
const int LEFT_R_PWM = 3;
const int LEFT_R_EN = 4;
const int LEFT_L_PWM = 5;

const int RIGHT_L_PWM = 6;
const int RIGHT_R_EN = 7;
const int RIGHT_L_EN = 8;
const int RIGHT_R_PWM = 9;

const int EDGE_FRONT = 10;
const int EDGE_BACK = 11;

const int OPPONENT_LEFT = A0;
const int OPPONENT_CENTER = A1;
const int OPPONENT_RIGHT = A2;

const bool LEFT_MOTOR_INVERTED = false;
const bool RIGHT_MOTOR_INVERTED = true;

const int EDGE_WHITE_STATE = HIGH;

const float THETA0_UNCERTAINTY_DEG = 8.0f; // MEASURE: spread of ~10 manual aim attempts

// ============================================================
// ARENA GEOMETRY — rulebook §5.1/5.2, no measurement needed
// ============================================================
const float ARENA_TOTAL_DIAMETER_CM = 150.0f; // §5.1
const float ARENA_FRAME_THICKNESS_CM = 3.0f;  // §5.1, white frame
const float ARENA_RADIUS_CM =
    (ARENA_TOTAL_DIAMETER_CM - 2.0f * ARENA_FRAME_THICKNESS_CM) / 2.0f; // = 72.0, black surface
const float ARENA_OUT_RADIUS_CM = ARENA_TOTAL_DIAMETER_CM / 2.0f;       // = 75.0, true disqualifying radius

const float START_LINE_CENTER_RADIUS_CM = 10.0f; // §5.2
const float START_LINE_THICKNESS_CM = 2.0f;      // §5.2
const float START_LINE_FAR_EDGE_RADIUS_CM =
    START_LINE_CENTER_RADIUS_CM + START_LINE_THICKNESS_CM / 2.0f; // = 11.0, nearest our nose can legally be
const float START_LINE_LENGTH_CM = 20.0f;                         // §5.2, max
const float START_LATERAL_SPREAD_MAX_CM = START_LINE_LENGTH_CM;   // worst case: us + opponent each offset ±10cm along their own line = 20cm total

// ============================================================
// ROBOT GEOMETRY — MEASURE with ruler, from pivot M (midpoint of driven wheel contacts)
// ============================================================
const float ROBOT_L_F_CM = 10.5f;               // MEASURE: M to wedge tip
const float ROBOT_L_B_CM = 9.5f;                // MEASURE: M to rear edge
const float ROBOT_WIDTH_CM = 20.0f;             // MEASURE: full width
const float ROBOT_TRACK_CM = 15.0f;             // MEASURE: sideways spacing of the two DRIVEN wheels
const float EDGE_SENSOR_FRONT_OFFSET_CM = 8.0f; // MEASURE: M to front edge sensor
const float EDGE_SENSOR_BACK_OFFSET_CM = 8.0f;  // MEASURE: M to back edge sensor

// Derived: farthest footprint corner from M (worst-case swing radius)
const float ROBOT_R_SWING_CM =
    fmaxf(hypotf(ROBOT_WIDTH_CM / 2.0f, ROBOT_L_F_CM),
          hypotf(ROBOT_WIDTH_CM / 2.0f, ROBOT_L_B_CM));

// Derived: whether the front edge sensor can actually protect the tip
// (only true if it sits within ARENA_OUT_RADIUS_CM - ARENA_RADIUS_CM of it)
const float EDGE_SENSOR_REACH_MARGIN_CM = ARENA_OUT_RADIUS_CM - ARENA_RADIUS_CM; // = 3.0

// Derived: start pose radius and opening sweep half-angle
// Worst case for sweep width: assume opponent's nose is right at ITS line (its own L_f unknown -> treat as 0)
const float START_POSE_RADIUS_CM = START_LINE_FAR_EDGE_RADIUS_CM + ROBOT_L_F_CM;
const float START_OPPONENT_WORST_CASE_LONG_CM =
    START_LINE_FAR_EDGE_RADIUS_CM + START_LINE_FAR_EDGE_RADIUS_CM + ROBOT_L_F_CM; // = 22 + L_f
const float OPEN_SWEEP_HALF_ANGLE_DEG =
    atanf(START_LATERAL_SPREAD_MAX_CM / START_OPPONENT_WORST_CASE_LONG_CM) * RAD_TO_DEG + THETA0_UNCERTAINTY_DEG;

// ============================================================
// MOTION MODEL — MEASURE in v5_test, all placeholders below
// ============================================================
const float DRIVE_SPEED_MAX_CMS = 45.0f;  // MEASURE: loaded top speed at RAMP_MAX_SPEED PWM (ceiling is 54.5-57.2, real is lower)
const float SPIN_RATE_CW_DEGS = 120.0f;   // MEASURE
const float SPIN_RATE_CCW_DEGS = 120.0f;  // MEASURE
const float SPIN_DRIFT_PER_REV_CM = 5.0f; // MEASURE: eps_spin
const float STOP_DISTANCE_CM = 16.0f;     // MEASURE: d_stop at DRIVE_SPEED_MAX_CMS
const float FRICTION_MU = 0.6f;           // MEASURE: spring-scale pull test

// Derived: deceleration from the measured stopping distance (v^2 = 2*a*d)
const float DRIVE_DECEL_CMS2 =
    (DRIVE_SPEED_MAX_CMS * DRIVE_SPEED_MAX_CMS) / (2.0f * STOP_DISTANCE_CM);

const float COMMIT_SOFT_START_S = DRIVE_SPEED_MAX_CMS / (FRICTION_MU * 981.0f); // t = v/(mu*g), g in cm/s^2

const int COMMIT_TRACK_TRIM_MAX = 60; // same role as v4's TRACK_CORRECTION — simple, already-proven pattern, no gate needed
const int EDGE_ESCAPE_TRIM_MAX = 0;   // 0 until G5 passes — a different, map-derived calculation, genuinely untested

// ============================================================
// SENSOR ADC CONFIG
// ============================================================
const int SENSOR_ADC_BITS = 10; // forced 10-bit to match bench calibration; VERIFY with Serial.print of a saturated reading

// ============================================================
// SENSOR THRESHOLDS — from bench data (250-350 @0-10cm, 600-700 @~10cm, <100 no-object/>80cm)
// ============================================================
const int CONTACT_BAND_LOW = 250;
const int CONTACT_BAND_HIGH = 350;
const int PEAK_BAND_LOW = 600;
const int PEAK_BAND_HIGH = 700;

const int STRONG_THRESHOLD = CONTACT_BAND_LOW;                      // = 250
const int NEAR_THRESHOLD = (CONTACT_BAND_HIGH + PEAK_BAND_LOW) / 2; // = 475
const int WEAK_THRESHOLD = 100;                                     // MEASURE: replace with venue no-object log max + spread

const float U0_POSITION_CM = 5.0f;            // MEASURE: spread of ~10 real placements (position only)
const float HEADING_DRIFT_PER_REV_DEG = 3.0f; // MEASURE: extra heading error per 360° of commanded turning
const float K_ERR_PATH_FACTOR = 0.15f;        // MEASURE: run-to-run speed/spin spread as a fraction of path traveled
const float SAFETY_ZONE_MIN_CM = 25.0f;       // §9.3, using the minimum stated width (conservative)
const float DETECT_RANGE_MAX_CM = 80.0f;      // MEASURE: R_det on a black target, sensor's rated max

// ============================================================
// SENSOR TIMING — derived from GP2Y0A21 refresh spec (datasheet: 38.3ms +/- 9.6ms, VERIFY)
// ============================================================
const float SENSOR_REFRESH_NOMINAL_MS = 38.3f;
const float SENSOR_REFRESH_JITTER_MS = 9.6f;
const unsigned long SENSOR_SAMPLE_INTERVAL_MS =
    (unsigned long)ceilf((SENSOR_REFRESH_NOMINAL_MS - SENSOR_REFRESH_JITTER_MS) / 2.0f); // = 15

const int WEAK_CONFIRM_SAMPLES =
    (int)ceilf((SENSOR_REFRESH_NOMINAL_MS + SENSOR_REFRESH_JITTER_MS) / (float)SENSOR_SAMPLE_INTERVAL_MS); // = 4
const int STRONG_CONFIRM_SAMPLES = 2;                                                                      // MEASURE: drop to 1 once 60s no-object log confirms no outliers above STRONG_THRESHOLD

const unsigned long LOST_CONTACT_GRACE_MS =
    (unsigned long)fmaxf(WEAK_CONFIRM_SAMPLES * (float)SENSOR_SAMPLE_INTERVAL_MS, 60.0f); // MEASURE: replace 60 with longest dropout seen in push tests

// ============================================================
// STATE TIMING
// ============================================================
// TWO PHYSICAL BUTTONS (wired to GND, internal pull-up -> pressed = LOW)
//   BUTTON 1 (A3): "power up"  -> enables motor drivers + sensors, NO logic runs
//   BUTTON 2 (A4): "start"     -> 5 s stationary delay, then the strategy runs
const int POWER_BUTTON_PIN = A3;
const int START_BUTTON_PIN = A4;
const bool BUTTON_ACTIVE_LOW = true; // false if wired to 3.3V with an external pull-down
const unsigned long BUTTON_DEBOUNCE_MS = 30;
const unsigned long START_DELAY_MS = 5000UL;       // rulebook: mandatory stationary delay
const unsigned long START_DELAY_MARGIN_MS = 50;    // only ever errs on the late side
const unsigned long START_COUNTDOWN_MS = START_DELAY_MS + START_DELAY_MARGIN_MS;

const unsigned long CONTROL_TICK_MS = 5UL; // fixed loop tick; well under SENSOR_SAMPLE_INTERVAL_MS (15ms)

const int DRIVE_PWM_MAX = 255;

const float SEARCH_SPIN_CAP_DEGS =
    (2.0f * atanf((ROBOT_WIDTH_CM / 2.0f) / DETECT_RANGE_MAX_CM) * RAD_TO_DEG) / ((SENSOR_REFRESH_NOMINAL_MS + WEAK_CONFIRM_SAMPLES * (float)SENSOR_SAMPLE_INTERVAL_MS) / 1000.0f);
const int SEARCH_SPIN_PWM =
    (int)constrain(255.0f * (SEARCH_SPIN_CAP_DEGS / fminf(SPIN_RATE_CW_DEGS, SPIN_RATE_CCW_DEGS)), 0.0f, 255.0f);

const float SEARCH_ACTUAL_SPIN_DEGS = fminf(SEARCH_SPIN_CAP_DEGS, fminf(SPIN_RATE_CW_DEGS, SPIN_RATE_CCW_DEGS));
const unsigned long OPEN_SWEEP_LEG_A_MS = (unsigned long)((OPEN_SWEEP_HALF_ANGLE_DEG / SEARCH_ACTUAL_SPIN_DEGS) * 1000.0f);
const unsigned long OPEN_SWEEP_LEG_B_MS = 2UL * OPEN_SWEEP_LEG_A_MS;

const int ALIGN_BASE_SPEED = 170; // TUNE (empirical): reused v4's ALIGN_SPEED as a starting point
const float ALIGN_ACTUAL_SPIN_DEGS = fminf(SPIN_RATE_CW_DEGS, SPIN_RATE_CCW_DEGS) * (ALIGN_BASE_SPEED / 255.0f);
const unsigned long ALIGN_TIMEOUT_MS =
    (unsigned long)(45.0f / ALIGN_ACTUAL_SPIN_DEGS * 1000.0f); // fixed: uses ALIGN's actual rate, not full-scale
const int ALIGN_FLIP_LIMIT = 3;

const float ALIGN_PROPORTIONAL_GAIN = 0.3f;      // TUNE (empirical)
const int ALIGN_PROPORTIONAL_MAX_BIAS = 85;      // TUNE (empirical)
const float RETURN_HEADING_TOLERANCE_DEG = 5.0f; // TUNE (empirical)

const unsigned long STALEMATE_HARD_CEILING_MS = 30000UL; // rule 6.6.D
const unsigned long STALEMATE_TIMEOUT_MS = 9000UL;       // MEASURE: 90th-percentile winning-push time; must stay < ceiling
const unsigned long STALEMATE_BACKOFF_MS = 300UL;        // TUNE (empirical)
const int STALEMATE_BREAK_TRIM = 40;                     // TUNE: alternates escape angle so a holding opponent can't predict our retreat line

static_assert(STALEMATE_TIMEOUT_MS + STALEMATE_BACKOFF_MS < STALEMATE_HARD_CEILING_MS,
              "Stalemate cycle must stay under rule 6.6.D's 30s ceiling");

// ============================================================
// EDGE RECOVERY — reused v4 constants as starting point, MEASURE for v5 chassis
// ============================================================
const int EDGE_RECOVER_SPEED = 170; // MEASURE
const unsigned long EDGE_CLEAR_CONFIRM_MS = 30;
const unsigned long EDGE_OVERRUN_MS = 80;
const unsigned long EDGE_RECOVER_MAX_MS = 700; // MEASURE

const unsigned long DOUBLE_EDGE_RECOVER_MAX_MS = 150UL; // caps the both-edges escape before re-reading sensors
const bool EDGE_SUPPRESSION_ENABLED = false; // map constants unmeasured: edge sensor always wins

// ============================================================
// STEERING
// ============================================================
const float SEARCH_COVERAGE_SWEEP_DEG = 360.0f - 90.0f; // full coverage: rotation + 90° sensor cone ≥ 360°
const unsigned long SEARCH_DWELL_MS = (unsigned long)(WEAK_CONFIRM_SAMPLES * SENSOR_SAMPLE_INTERVAL_MS);

const int COMMIT_VOID_PWM = 150; // map untrusted: moderate speed, edge sensors are the safety net

#endif