#ifndef HARDWARE_H
#define HARDWARE_H
#include <Arduino.h>
#include <math.h>

// HARDWARE.H = everything YOU type: wiring, rulebook numbers, ruler/stopwatch measurements, tuning knobs.
// FORMULAS.H = everything CALCULATED from these (included at the bottom; only edit if the maths changes).

// ================= WIRING (matches SUMOX-26 wiring plan) =================
const int LEFT_L_EN = 2, LEFT_R_PWM = 3, LEFT_R_EN = 4, LEFT_L_PWM = 5;
const int RIGHT_L_PWM = 6, RIGHT_R_EN = 7, RIGHT_L_EN = 8, RIGHT_R_PWM = 9;
const int EDGE_FRONT = 10, EDGE_BACK = 11;
const int OPPONENT_LEFT = A0, OPPONENT_CENTER = A1, OPPONENT_RIGHT = A2;
const int POWER_BUTTON_PIN = A3, START_BUTTON_PIN = A4;

const bool LEFT_MOTOR_INVERTED = false;  // flip if that wheel spins backward (OR swap M1/M2, never both)
const bool RIGHT_MOTOR_INVERTED = true;
const int EDGE_WHITE_STATE = HIGH;       // FALLBACK only: Sensors.cpp auto-detects polarity at start from the black surface under the robot

const bool POWER_BUTTON_PRESENT = false; // KCD4 cuts battery power, nothing on A3
const bool START_IS_LATCHING = true;     // A4 is a rocker: ON = run, OFF = stop
const bool START_SWITCH_ANALOG = true;   // read A4 as a voltage (3.3V or divided 5V feed)
const bool BUTTON_ACTIVE_LOW = false;
const bool REARM_ENABLED = true;
const unsigned long BUTTON_DEBOUNCE_MS = 30;
const int SENSOR_ADC_BITS = 10;          // VERIFY: NoiseLog max reading tops out near 1023

// ================= RULEBOOK =================
const float ARENA_TOTAL_DIAMETER_CM = 150.0f;    // §5.1
const float ARENA_FRAME_THICKNESS_CM = 3.0f;     // §5.1 white frame
const float START_LINE_CENTER_RADIUS_CM = 10.0f; // §5.2
const float START_LINE_THICKNESS_CM = 2.0f;      // §5.2
const float START_LINE_LENGTH_CM = 20.0f;        // §5.2 max
const float SAFETY_ZONE_MIN_CM = 25.0f;          // §9.3
const unsigned long START_DELAY_MS = 5000UL;     // mandatory stationary delay
const unsigned long START_DELAY_MARGIN_MS = 50;  // errs on the late side only
const unsigned long STALEMATE_HARD_CEILING_MS = 30000UL; // rule 6.6.D

// ================= ROBOT MEASUREMENTS (ruler, wedge ON) =================
const float ROBOT_LENGTH_CM = 20.0f;         // MEASURE: wedge tip to chassis rear
const float REAR_TO_AXLE_CM = 3.6f;          // MEASURE: chassis rear to wheel axle line
const float WEDGE_TO_FRONT_SENSOR_CM = 4.7f; // measured
const float REAR_TO_BACK_SENSOR_CM = 3.6f;   // measured
const float ROBOT_WIDTH_CM = 20.0f;          // MEASURE
const float ROBOT_TRACK_CM = 15.0f;          // MEASURE: spacing of the two driven wheels

// ================= MOTION (placeholders until measured) =================
const float DRIVE_SPEED_MAX_CMS = 45.0f;  // MEASURE: distance / time at PWM 255
const float SPIN_RATE_CW_DEGS = 120.0f;   // MEASURE
const float SPIN_RATE_CCW_DEGS = 120.0f;  // MEASURE
const float SPIN_DRIFT_PER_REV_CM = 5.0f; // MEASURE
const float STOP_DISTANCE_CM = 16.0f;     // MEASURE: slide after cutting power at full speed
const float FRICTION_MU = 0.6f;           // MEASURE: spring-scale pull / weight
const float THETA0_UNCERTAINTY_DEG = 8.0f;
const float U0_POSITION_CM = 5.0f;
const float HEADING_DRIFT_PER_REV_DEG = 3.0f;
const float K_ERR_PATH_FACTOR = 0.15f;
const int MIN_MOVE_PWM = 90;              // MEASURE: lowest PWM that moves the loaded robot

// ================= OPPONENT SENSOR CALIBRATION =================
// Old bench readings were taken WITHOUT the dividers. Through 9.9k/9.9k every reading is halved,
// so safe defaults = old numbers x ratio. Once measured through the dividers: type the 5 MEASURED_ values, set USE_MEASURED_THRESHOLDS = true.
const float SENSOR_DIVIDER_RATIO = 9.9f / (9.9f + 9.9f); // multimeter: both resistors read 9.9k
const int BENCH_NO_OBJECT_MAX = 100;
const int BENCH_CONTACT_LOW = 250, BENCH_CONTACT_HIGH = 350;
const int BENCH_PEAK_LOW = 600, BENCH_PEAK_HIGH = 700;
const bool USE_MEASURED_THRESHOLDS = false;
const int MEASURED_WEAK = 75;
const int MEASURED_CONTACT_LOW = 125, MEASURED_CONTACT_HIGH = 175;
const int MEASURED_PEAK_LOW = 300, MEASURED_PEAK_HIGH = 350;
const float ADC_NOISE_SIGMA = 20.0f;      // pessimistic default until NoiseLog is run (motors ON)
const float DETECT_RANGE_MAX_CM = 80.0f;
const float SENSOR_REFRESH_NOMINAL_MS = 38.3f; // GP2Y0A21 datasheet
const float SENSOR_REFRESH_JITTER_MS = 9.6f;
const int STRONG_CONFIRM_SAMPLES = 2;
const float LOST_CONTACT_GRACE_FLOOR_MS = 60.0f;
const bool PHANTOM_GATE_ENABLED = false;
const bool EDGE_SUPPRESSION_ENABLED = false;

// ================= TUNING =================
const unsigned long CONTROL_TICK_MS = 5UL;
const int DRIVE_PWM_MAX = 255;
const bool MOTOR_SLEW_ENABLED = true;
const int COMMIT_TRACK_TRIM_MAX = 60;
const int EDGE_ESCAPE_TRIM_MAX = 0;
const int COMMIT_VOID_PWM = 150;
const int ALIGN_BASE_SPEED = 170;
const float ALIGN_PROPORTIONAL_GAIN = 0.3f;
const int ALIGN_PROPORTIONAL_MAX_BIAS = 85;
const int ALIGN_FLIP_LIMIT = 3;
const float RETURN_HEADING_TOLERANCE_DEG = 5.0f;
const unsigned long STALEMATE_TIMEOUT_MS = 9000UL;
const unsigned long STALEMATE_BACKOFF_MS = 300UL;
const int STALEMATE_BREAK_TRIM = 40;
const int EDGE_RECOVER_SPEED = 170;
const unsigned long EDGE_CLEAR_CONFIRM_MS = 30;
const unsigned long EDGE_OVERRUN_MS = 80;
const unsigned long EDGE_RECOVER_MAX_MS = 700;
const unsigned long DOUBLE_EDGE_RECOVER_MAX_MS = 150UL;

#include "Formulas.h"
#endif
