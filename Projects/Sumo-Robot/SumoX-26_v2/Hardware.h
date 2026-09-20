#ifndef HARDWARE_H
#define HARDWARE_H

#include <Arduino.h>

// ============================================================================
// SumoX-26 — Hardware.h
// ----------------------------------------------------------------------------
// Pin assignments AND tunable constants. No logic lives here — just numbers
// every other file needs. This is your v3 wiring doc, translated into
// constants that every other file can #include, plus bench-calibrated
// thresholds that strategy/sensor code reads but never hardcodes itself.
// ============================================================================

// ===================== LEFT MOTOR DRIVER (BTS7960) =====================
const int LEFT_L_EN   = 2;
const int LEFT_R_PWM  = 3;
const int LEFT_R_EN   = 4;
const int LEFT_L_PWM  = 5;

// ===================== RIGHT MOTOR DRIVER (BTS7960) =====================
const int RIGHT_L_PWM = 6;
const int RIGHT_R_EN  = 7;
const int RIGHT_L_EN  = 8;
const int RIGHT_R_PWM = 9;

// ===================== EDGE SENSORS (TCRT5000 x4) =====================
const int EDGE_FRONT_LEFT  = 10;
const int EDGE_FRONT_RIGHT = 11;
const int EDGE_BACK_LEFT   = 12;
const int EDGE_BACK_RIGHT  = 13;

// ===================== OPPONENT SENSORS (GP2Y0A21 x4) =====================
const int OPPONENT_FRONT_LEFT  = A0;
const int OPPONENT_FRONT_RIGHT = A1;
const int OPPONENT_LEFT        = A2;
const int OPPONENT_RIGHT       = A3;

// ===================== POWER / ROUND SWITCHES =====================
const int START_BUTTON = A4;
const int ROUND_BUTTON = A5;

// ===============================  TUNABLES ===============================

// ===================== MOTOR POLARITY =====================
const bool LEFT_MOTOR_INVERTED  = false;
const bool RIGHT_MOTOR_INVERTED = false;

// Raw analog value (0-1023) at which a GP2Y0A21 reading counts as "opponent
// detected." Closer objects = higher voltage = higher ADC value on this
// sensor, so DETECTED means "reading is above this number."
const int DIST_THRESHOLD = 400;
const int OPPONENT_OFFSET_FL = 0;
const int OPPONENT_OFFSET_FR = 0;
const int OPPONENT_OFFSET_LEFT = 0;
const int OPPONENT_OFFSET_RIGHT = 0;
const int OPPONENT_GAIN_FL = 1000;
const int OPPONENT_GAIN_FR = 1000;
const int OPPONENT_GAIN_LEFT = 1000;
const int OPPONENT_GAIN_RIGHT = 1000;
const int SENSOR_SAMPLE_INTERVAL_MS = 40;
const int STRATEGY1_KP_NUMERATOR = 1;
const int STRATEGY1_KP_DENOMINATOR = 2;
const int STRATEGY1_ERROR_DEADBAND = 20;
const int STRATEGY1_BASE_SPEED = 165;
const int STRATEGY1_MAX_CORRECTION = 255;

// TCRT5000 digital state that means "white detected."
const int EDGE_WHITE_STATE = HIGH;
const int EDGE_WHITE_STATE_FL = EDGE_WHITE_STATE;
const int EDGE_WHITE_STATE_FR = EDGE_WHITE_STATE;
const int EDGE_WHITE_STATE_BL = EDGE_WHITE_STATE;
const int EDGE_WHITE_STATE_BR = EDGE_WHITE_STATE;

// How many samples each opponent sensor's rolling buffer keeps.
const int SENSOR_SAMPLES = 3;

#endif