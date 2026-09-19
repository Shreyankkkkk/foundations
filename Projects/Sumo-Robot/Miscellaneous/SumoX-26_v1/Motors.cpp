// ============================================================================
// SumoX-26 — Motors.cpp
// ----------------------------------------------------------------------------
// The actual electrical detail lives here. Nothing outside this file should
// ever mention LEFT_R_PWM, analogWrite, etc. directly.
//
// drive(0, 0) is a real brake, not a coast: with EN high and both PWM pins
// at 0, both BTS7960 half-bridges pull the motor terminals to ground, which
// shorts the motor and stops it hard. That is deliberate — do not "fix" it
// by disabling the drivers instead.
//
// DIRECTION WARNING: run MotorBench.ino with the wheels off the ground before
// trusting any of this. If a side spins the wrong way, set its *_INVERTED
// flag in Hardware.h rather than rewiring or editing this file.
// ============================================================================

#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"

static unsigned long motionInhibitUntil = 0;

// Last values actually written to the hardware, used to detect a high-speed
// direction flip so we can insert a brake gap before it.
static int lastAppliedLeft  = 0;
static int lastAppliedRight = 0;

void initMotors() {
  pinMode(LEFT_L_EN, OUTPUT);
  pinMode(LEFT_R_EN, OUTPUT);
  pinMode(LEFT_R_PWM, OUTPUT);
  pinMode(LEFT_L_PWM, OUTPUT);

  pinMode(RIGHT_L_EN, OUTPUT);
  pinMode(RIGHT_R_EN, OUTPUT);
  pinMode(RIGHT_R_PWM, OUTPUT);
  pinMode(RIGHT_L_PWM, OUTPUT);

  // Zero PWM outputs before the drivers are armed, so there is no window
  // where EN is HIGH and the PWM pins are in an unknown state.
  analogWrite(LEFT_R_PWM, 0);
  analogWrite(LEFT_L_PWM, 0);
  analogWrite(RIGHT_R_PWM, 0);
  analogWrite(RIGHT_L_PWM, 0);

  // Arm both drivers once. These stay HIGH for the entire match.
  digitalWrite(LEFT_L_EN, HIGH);
  digitalWrite(LEFT_R_EN, HIGH);
  digitalWrite(RIGHT_L_EN, HIGH);
  digitalWrite(RIGHT_R_EN, HIGH);

  lastAppliedLeft  = 0;
  lastAppliedRight = 0;

  stopMotors();
}

void inhibitMotionUntil(unsigned long deadline) {
  motionInhibitUntil = deadline;
  stopMotors();
}

void stopMotors() {
  drive(0, 0);
}

// Writes one side's PWM pair. Kept private to this file.
static void applySide(int speed, int rPwmPin, int lPwmPin) {
  if (speed >= 0) {
    analogWrite(lPwmPin, 0);
    analogWrite(rPwmPin, speed);
  } else {
    analogWrite(rPwmPin, 0);
    analogWrite(lPwmPin, -speed);
  }
}

// Returns true if going from `from` to `to` is a direction reversal that is
// fast enough to be worth braking through first.
static bool needsReversalBrake(int from, int to) {
  if (REVERSAL_BRAKE_US == 0) return false;
  if (from > 0 && to < 0) return (from >= REVERSAL_BRAKE_FLOOR || -to >= REVERSAL_BRAKE_FLOOR);
  if (from < 0 && to > 0) return (-from >= REVERSAL_BRAKE_FLOOR || to >= REVERSAL_BRAKE_FLOOR);
  return false;
}

void drive(int leftSpeed, int rightSpeed) {
  // Nothing may move until the mandatory five-second start window is over.
  // The subtraction-then-compare form is rollover safe.
  if (leftSpeed != 0 || rightSpeed != 0) {
    if ((long)(millis() - motionInhibitUntil) < 0) {
      leftSpeed  = 0;
      rightSpeed = 0;
    }
  }

  leftSpeed  = constrain(leftSpeed,  -255, 255);
  rightSpeed = constrain(rightSpeed, -255, 255);

  if (LEFT_MOTOR_INVERTED)  leftSpeed  = -leftSpeed;
  if (RIGHT_MOTOR_INVERTED) rightSpeed = -rightSpeed;

  // Slam-reversing a loaded gearmotor spikes the current hard enough to dip
  // the battery rail and reset the board. Cross through zero first.
  if (needsReversalBrake(lastAppliedLeft, leftSpeed) ||
      needsReversalBrake(lastAppliedRight, rightSpeed)) {
    analogWrite(LEFT_R_PWM, 0);
    analogWrite(LEFT_L_PWM, 0);
    analogWrite(RIGHT_R_PWM, 0);
    analogWrite(RIGHT_L_PWM, 0);
    delayMicroseconds(REVERSAL_BRAKE_US);
  }

  applySide(leftSpeed,  LEFT_R_PWM,  LEFT_L_PWM);
  applySide(rightSpeed, RIGHT_R_PWM, RIGHT_L_PWM);

  lastAppliedLeft  = leftSpeed;
  lastAppliedRight = rightSpeed;
}

void forward(int speed) {
  speed = constrain(speed, 0, 255);
  drive(speed, speed);
}

void backward(int speed) {
  speed = constrain(speed, 0, 255);
  drive(-speed, -speed);
}

// Rotate in place counter-clockwise (nose swings left).
void turnLeft(int speed) {
  speed = constrain(speed, 0, 255);
  drive(-speed, speed);
}

// Rotate in place clockwise (nose swings right).
void turnRight(int speed) {
  speed = constrain(speed, 0, 255);
  drive(speed, -speed);
}
