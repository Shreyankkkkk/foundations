#ifndef HARDWARE_H
#define HARDWARE_H

// ============================================================================
// SumoX-26 — Hardware.h
// ----------------------------------------------------------------------------
// Pin assignments AND tunable constants. No logic lives here — just numbers
// every other file needs. This is your v3 wiring doc, translated into
// constants that every other file can #include, plus bench-calibrated
// thresholds that strategy/sensor code reads but never hardcodes itself.
//
// `#ifndef HARDWARE_H / #define HARDWARE_H / #endif` at the top/bottom is
// an "include guard" — it stops this file from being pasted in twice if
// two other files both #include it. You'll see this pattern in every .h
// file we write; just copy it, no need to memorize why yet.
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
// Corners confirmed from chassis render. Pin-to-physical-sensor mapping
// still needs a continuity test.
const int EDGE_FRONT_LEFT  = 10;
const int EDGE_FRONT_RIGHT = 11;
const int EDGE_BACK_LEFT   = 12;
const int EDGE_BACK_RIGHT  = 13;

// ===================== OPPONENT SENSORS (GP2Y0A21 x4) =====================
// 2 front + 1 each side, confirmed from chassis render. Same continuity
// caveat as the edge sensors.
const int OPPONENT_FRONT_LEFT  = A0;
const int OPPONENT_FRONT_RIGHT = A1;
const int OPPONENT_LEFT        = A2;
const int OPPONENT_RIGHT       = A3;

// ===================== START BUTTON =====================
// Not in the v3 wiring table — placeholder on a free pin, confirm or change.
const int START_BUTTON = A4;

// =========================-=== SENSOR TUNABLES =============================

// Raw analog value (0-1023) at which a GP2Y0A21 reading counts as "opponent
// detected." Closer objects = higher voltage = higher ADC value on this
// sensor, so DETECTED means "reading is above this number."
const int DIST_THRESHOLD = 400;

// TCRT5000 digital state that means "white detected." Confirm this with a
// multimeter test on your actual sensors before trusting it — modules vary
// on whether HIGH or LOW means white vs black.
const int EDGE_WHITE_STATE = HIGH;

// How many samples each opponent sensor's rolling buffer keeps, to smooth
// out single-reading noise before comparing against DIST_THRESHOLD.
const int SENSOR_SAMPLES = 4;

#endif
