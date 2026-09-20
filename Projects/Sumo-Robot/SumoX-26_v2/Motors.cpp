// ============================================================================
// SumoX-26 — Motors.cpp
// Electrical details of the two BTS7960 drivers live here.
// ============================================================================

#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"

static unsigned long motionInhibitUntil = 0;

void initMotors() {
  analogWriteResolution(8);   // drive() assumes 0-255. If the compiler rejects this line, delete it (8-bit is the default).

  pinMode(LEFT_L_EN, OUTPUT);
  pinMode(LEFT_R_EN, OUTPUT);
  pinMode(LEFT_R_PWM, OUTPUT);
  pinMode(LEFT_L_PWM, OUTPUT);

  pinMode(RIGHT_L_EN, OUTPUT);
  pinMode(RIGHT_R_EN, OUTPUT);
  pinMode(RIGHT_R_PWM, OUTPUT);
  pinMode(RIGHT_L_PWM, OUTPUT);

  // PWM to zero BEFORE the drivers are enabled.
  analogWrite(LEFT_R_PWM, 0);
  analogWrite(LEFT_L_PWM, 0);
  analogWrite(RIGHT_R_PWM, 0);
  analogWrite(RIGHT_L_PWM, 0);

  digitalWrite(LEFT_L_EN, HIGH);
  digitalWrite(LEFT_R_EN, HIGH);
  digitalWrite(RIGHT_L_EN, HIGH);
  digitalWrite(RIGHT_R_EN, HIGH);

  stopMotors();
}

// No motion is allowed until millis() reaches this deadline (used for the 5 s rule).
void inhibitMotionUntil(unsigned long deadline) {
  motionInhibitUntil = deadline;
  stopMotors();
}

void stopMotors() {
  drive(0, 0);
}

// One side of the robot. The direction being left is switched off FIRST, so
// the two half-bridges are never both driven during a reversal.
static void setSide(int rPwmPin, int lPwmPin, int speed) {
  if (speed >= 0) {
    analogWrite(lPwmPin, 0);
    analogWrite(rPwmPin, speed);
  } else {
    analogWrite(rPwmPin, 0);
    analogWrite(lPwmPin, -speed);
  }
}

// -255 = full reverse, 0 = stop, +255 = full forward.
void drive(int leftSpeed, int rightSpeed) {
  if (leftSpeed != 0 || rightSpeed != 0) {
    if (millis() < motionInhibitUntil) {
      leftSpeed = 0;
      rightSpeed = 0;
    }
  }

  leftSpeed  = constrain(leftSpeed, -255, 255);
  rightSpeed = constrain(rightSpeed, -255, 255);

  if (LEFT_MOTOR_INVERTED)  leftSpeed  = -leftSpeed;
  if (RIGHT_MOTOR_INVERTED) rightSpeed = -rightSpeed;

  setSide(LEFT_R_PWM,  LEFT_L_PWM,  leftSpeed);
  setSide(RIGHT_R_PWM, RIGHT_L_PWM, rightSpeed);
}