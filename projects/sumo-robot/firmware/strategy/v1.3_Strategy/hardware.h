#ifndef HARDWARE_H
#define HARDWARE_H

#include <Arduino.h>

// ================== === LEFT MOTOR DRIVER (BTS7960) =====================
const int LEFT_L_EN = 2;
const int LEFT_R_PWM = 3;
const int LEFT_R_EN = 4;
const int LEFT_L_PWM = 5;

// ===================== RIGHT MOTOR DRIVER (BTS7960) =====================
const int RIGHT_L_PWM = 6;
const int RIGHT_R_EN = 7;
const int RIGHT_L_EN = 8;
const int RIGHT_R_PWM = 9;

// ===================== EDGE SENSORS (TCRT5000 x2, onboard comparator) ======
const int EDGE_FRONT = 10;
const int EDGE_BACK = 11;

// ===================== OPPONENT SENSORS (GP2Y0A21 x3) =====================
const int OPPONENT_LEFT = A0;
const int OPPONENT_CENTER = A1;
const int OPPONENT_RIGHT = A2;

// ===================== MOTOR POLARITY =====================
const bool LEFT_MOTOR_INVERTED = false;
const bool RIGHT_MOTOR_INVERTED = true;

// ===================== EDGE SENSOR STATE =====================
const int EDGE_WHITE_STATE = HIGH;

// ===================== OPPONENT SENSOR THRESHOLDS =====================
const int DETECT_THRESHOLD_L = 100;
const int DETECT_THRESHOLD_C = 100; // without any object, value ranges between 80-90
const int DETECT_THRESHOLD_R = 100;

const int ENGAGE_THRESHOLD_L = 465;
const int ENGAGE_THRESHOLD_C = 465; // at 10 cm, the value ranges from 600-700, since there is a median filter, getting one 600 reading may not be enough to trigger the engage state, so we set it to 450 to be safe
const int ENGAGE_THRESHOLD_R = 465;

// ===================== SENSOR SAMPLE INTERVAL =====================
const int SENSOR_SAMPLE_INTERVAL_MS = 40;

// ===================== SENSOR SAMPLE COUNT =====================
const int SENSOR_SAMPLE = 3;

// ===================== HEADING ESTIMATE (dead-reckoned, no gyro) =========
const float TURN_RATE_DEG_PER_MS = 0.312f;

// ===================== SEARCH (bounded oscillation, no free arc) =========
const int SEARCH_SPIN_SPEED = 150;
const float SEARCH_MAX_SWEEP_DEG = 180.0f;

// ===================== BOUNDED CREEP =====================
const int CREEP_SPEED = 140;
const unsigned long CREEP_PULSE_MS = 120;
const float CREEP_ALLOWED_HEADING_BAND_DEG = 25.0f;

const unsigned long START_COUNTDOWN_MS = 5000; // confirm against ruleset

const int EDGE_RECOVER_SPEED = 170;

const unsigned long EDGE_CLEAR_CONFIRM_MS = 30;
const unsigned long EDGE_OVERRUN_MS = 80;
const unsigned long EDGE_RECOVER_MAX_MS = 700;

const unsigned long ALIGN_TIMEOUT_MS = 600;
const int ALIGN_FLIP_LIMIT = 3;

const unsigned long RAM_REACQUIRE_MS = 1500;
const int REACQUIRE_SPEED = 130;

const int TRACK_CORRECTION = 60;

// ===================== LOST CONTACT PERIOD for GP2Y0A21=====================
const unsigned long LOST_CONTACT_GRACE_MS = 150;

#endif