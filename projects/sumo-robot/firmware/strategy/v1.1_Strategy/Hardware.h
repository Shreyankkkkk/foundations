#ifndef HARDWARE_H
#define HARDWARE_H

// ============================================================================
// SumoX-26 — Hardware.h
// ----------------------------------------------------------------------------
// Pin assignments AND tunable constants. No logic lives here — just numbers
// every other file needs.
//
// BOARD: Arduino UNO Q (STM32U585 MCU side). This is NOT an UNO R3.
//   - All header GPIO is 3.3 V logic. Absolute max 3.6 V at any pin.
//   - A0 and A1 are ADC-ONLY and are NOT 5 V tolerant. Never feed them more
//     than 3.3 V, and never source/sink DC current through them.
//   - The 5 V header pin is an OUTPUT you can use to power modules. Do not
//     feed 5 V back into any GPIO.
//   - Per-pin current limit is 20 mA. Nothing here drives a load directly.
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

// NOTE: the four *_PWM pins above (3, 5, 6, 9) must all be real PWM outputs.
// On an UNO R3 they are. On the UNO Q the header is UNO-shaped but the MCU
// underneath is different. Run MotorBench.ino before trusting this — it
// verifies each pin produces a variable speed instead of just on/off.

// ===================== EDGE SENSORS (TCRT5000 x4) =====================
// Digital outputs from the comparator on each module.
// The modules must be powered from the 3.3 V rail, NOT 5 V — see the wiring
// notes at the bottom of this file.
const int EDGE_FRONT_LEFT  = 10;
const int EDGE_FRONT_RIGHT = 11;
const int EDGE_BACK_LEFT   = 12;
const int EDGE_BACK_RIGHT  = 13;

// ===================== OPPONENT SENSORS (GP2Y0A21 x4) =====================
// Analog outputs. These MUST go through a voltage divider before reaching
// the pin — see the wiring notes at the bottom of this file. A0 and A1 in
// particular are not 5 V tolerant and will be damaged by a raw sensor output
// if the sensor supply ever glitches high.
const int OPPONENT_FRONT_LEFT  = A0;
const int OPPONENT_FRONT_RIGHT = A1;
const int OPPONENT_LEFT        = A2;
const int OPPONENT_RIGHT       = A3;

// ===================== POWER / ROUND SWITCHES =====================
// START_BUTTON is the power/armed switch's auxiliary signal. The switch also
// controls the battery feed, so flipping it powers the robot but never starts
// the round by itself.
const int START_BUTTON = A4;
// ROUND_BUTTON is pressed after placement to begin the five-second delay.
const int ROUND_BUTTON = A5;

// Select the strategy implementation compiled into the robot.
#define ACTIVE_STRATEGY 1

// ===============================  TUNABLES ===============================

// ===================== ADC SCALE =====================
// Every threshold in this project is expressed in ADC counts, so the whole
// system has to agree on how many counts a full-scale reading is.
//
// The UNO Q's ADC is 14-bit capable. We run it at 12 bits, which gives a
// finer reading than an UNO R3's 10 bits and makes up for the resolution
// lost to the input voltage divider.
//
// If analogReadResolution() will not compile, or SensorCalibration.ino shows
// readings that never exceed ~1023, set BITS to 10 and MAX to 1023 here and
// everything downstream rescales with it.
const int ADC_RESOLUTION_BITS = 12;
const int ADC_MAX             = 4095;

// ===================== MOTOR POLARITY =====================
// Set after running MotorBench.ino with the wheels off the ground.
// false = this motor's wiring already matches "forward PWM = physically
// forward." true = invert it here instead of rewiring or editing Motors.cpp.
const bool LEFT_MOTOR_INVERTED  = false;
const bool RIGHT_MOTOR_INVERTED = false;

// When a motor is told to reverse direction while it is still spinning hard,
// the BTS7960 sees a large current spike and the battery rail dips — which
// can reset the board mid-round. This inserts a brief both-sides-off gap
// before any high-speed direction flip. Set to 0 to disable.
const unsigned int REVERSAL_BRAKE_US    = 400;
// Direction flips below this PWM magnitude are not worth braking for.
const int          REVERSAL_BRAKE_FLOOR = 100;

// ===================== OPPONENT DETECTION =====================
// ADC value at which a GP2Y0A21 reading counts as "opponent detected."
//
// *** THIS VALUE IS A PLACEHOLDER. IT IS NOT CALIBRATED. ***
// Run SensorCalibration.ino and pick a number that satisfies BOTH limits:
//   LOWER limit: above the reading you get from an empty ring, so noise and
//                the far wall do not register.
//   UPPER limit: low enough that you still detect an opponent at ~60 cm, but
//                high enough that you do NOT detect anything past ~70 cm.
//                The ring radius is 75 cm and the GP2Y0A21 reaches 80 cm, so
//                without this ceiling your front sensors will lock onto
//                referees and tables across the ring (rulebook 9.3 makes you
//                responsible for that).
const int DIST_THRESHOLD = 1600;

// Per-sensor trim. Every comparison in the strategy code puts one physical
// sensor's number next to another physical sensor's number (right - left,
// front vs side). Unit-to-unit variation on the GP2Y0A21 is large enough to
// put a permanent lean into that comparison, so each channel gets corrected
// here first.
//
// How to fill these in with SensorCalibration.ino:
//   1. Put a flat target at a fixed distance (30 cm works) squarely in front
//      of ONE sensor at a time and note the reading.
//   2. Pick whichever sensor read highest as the reference.
//   3. For each other sensor, GAIN = 1000 * referenceReading / thisReading.
//   4. Leave OFFSET at 0 unless a sensor reads non-zero with nothing in
//      front of it at all; then set OFFSET to minus that idle reading.
const int OPPONENT_OFFSET_FL    = 0;
const int OPPONENT_OFFSET_FR    = 0;
const int OPPONENT_OFFSET_LEFT  = 0;
const int OPPONENT_OFFSET_RIGHT = 0;
const int OPPONENT_GAIN_FL      = 1000;   // 1000 = x1.000, no change
const int OPPONENT_GAIN_FR      = 1000;
const int OPPONENT_GAIN_LEFT    = 1000;
const int OPPONENT_GAIN_RIGHT   = 1000;

// The GP2Y0A21 refreshes its output roughly every 38 ms. Sampling faster than
// that just re-reads the same held value, which is why the old rolling
// average did nothing. This gates new samples to the sensor's real rate.
const unsigned long SENSOR_SAMPLE_INTERVAL_MS = 40;

// How many samples each opponent sensor's buffer keeps. Must be ODD — the
// filter takes the median, not the mean, because the Sharp's characteristic
// failure is a single large spike that a mean would smear across the window
// instead of discarding. 5 samples x 40 ms = a 200 ms window.
const int SENSOR_SAMPLES = 5;

// ===================== EDGE DETECTION =====================
// TCRT5000 digital state that means "white detected."
//
// Each module has its own trim pot and they are not guaranteed to agree, so
// each corner gets its own constant. SensorCalibration.ino prints all four
// live — hold the robot over black, over white, and over the BROWN centre
// lines, and set each of these to whatever state actually appears over white.
//
// The brown lines matter: the arena has two 2 cm brown lines 10 cm from
// centre. Brown-on-black is a smaller contrast step than white-on-black but
// it is not zero. If a trim pot is set too sensitive you will trigger a full
// edge recovery in the middle of the ring, repeatedly, and lose the round to
// it. Test over brown explicitly.
const int EDGE_WHITE_STATE_FL = HIGH;
const int EDGE_WHITE_STATE_FR = HIGH;
const int EDGE_WHITE_STATE_BL = HIGH;
const int EDGE_WHITE_STATE_BR = HIGH;

// A single noisy read used to be enough to abort an in-progress push. Each
// corner now has to report the same state on two consecutive reads before
// the change is accepted. The loop runs in microseconds so this costs
// essentially no reaction time, but it removes single-sample glitches.
const int EDGE_CONFIRM_READS = 2;

// ============================================================================
// WIRING NOTES — the UNO Q is 3.3 V, your modules are not
// ----------------------------------------------------------------------------
// TCRT5000 edge modules (x4):
//   Power them from the 3.3 V header pin, not 5 V. The LM393 comparator on
//   these boards works fine down to 2 V, and powering the module at 3.3 V
//   means its digital output swings 0–3.3 V, which is directly safe for the
//   pin. The IR LED will be slightly dimmer, so re-adjust the trim pot after
//   the change — do not assume the old setting still works.
//
//   If a module refuses to discriminate black from white at 3.3 V, the
//   fallback is to power it at 5 V and drop its output with a divider:
//   sensor DO -> 10 kOhm -> pin, and 20 kOhm from pin to GND. That gives
//   5 V * 20/30 = 3.33 V. Four of these, one per corner.
//
// GP2Y0A21 opponent sensors (x4):
//   These need a 4.5–5.5 V supply and will NOT run on 3.3 V, so power them
//   from the 5 V header pin. Their output peaks around 3.1 V, which is only
//   just under the 3.3 V limit — and A0/A1 are not 5 V tolerant, so a supply
//   glitch there is not recoverable. Divide every one of the four outputs:
//
//     sensor Vo ---[ 10 kOhm ]---+--- Ax pin
//                                |
//                            [ 22 kOhm ]
//                                |
//                               GND
//
//   That is a x0.688 divider, so 3.1 V becomes 2.13 V — comfortable margin,
//   and the 12-bit ADC setting above more than recovers the lost resolution.
//
//   Also fit a 10 uF capacitor between Vcc and GND at EACH sensor, close to
//   the sensor body. The Sharp datasheet asks for this and the sensors are
//   noticeably noisier without it.
//
// Grounds:
//   The motor battery ground and the UNO Q ground must be joined at ONE
//   point, close to the board. Run the sensor wiring away from the motor
//   leads — the BTS7960 switching noise couples into analog lines easily.
//
// Brownout:
//   If the board resets mid-round it re-enters waitForStart() and sits there
//   for the rest of the match, which is an automatic loss. Fit a large
//   electrolytic (1000 uF or more) across the driver supply and power the
//   board's logic from a separate regulator, not off the same rail the
//   motors are chewing on.
// ============================================================================

#endif
