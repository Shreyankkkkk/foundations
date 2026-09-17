// ============================================================================
// SumoX-26 — Motors.cpp
// ----------------------------------------------------------------------------
// The actual electrical detail lives here. Nothing outside this file should
// ever need to mention LEFT_R_PWM, analogWrite, etc. directly for driving.
//
// DIRECTION WARNING: forward()/turnLeft()/turnRight() below assume both
// motors are mounted facing the same way electrically. If your two motors
// are physically mirrored on the chassis (very common — motor shafts
// pointing outward on both sides), one motor's "forward" wiring may spin
// it backward relative to the robot. Bench-test with one wheel off the
// ground before trusting these — flip the RPWM/LPWM pair for whichever
// side spins the wrong way once you see it happen.
// ============================================================================

#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"

void initMotors() {
  pinMode(LEFT_L_EN, OUTPUT);
  pinMode(LEFT_R_EN, OUTPUT);
  pinMode(LEFT_R_PWM, OUTPUT);
  pinMode(LEFT_L_PWM, OUTPUT);

  pinMode(RIGHT_L_EN, OUTPUT);
  pinMode(RIGHT_R_EN, OUTPUT);
  pinMode(RIGHT_R_PWM, OUTPUT);
  pinMode(RIGHT_L_PWM, OUTPUT);

  // Arm both drivers once. These stay HIGH for the entire match — they are
  // not touched again anywhere else in the code.
  digitalWrite(LEFT_L_EN, HIGH);
  digitalWrite(LEFT_R_EN, HIGH);
  digitalWrite(RIGHT_L_EN, HIGH);
  digitalWrite(RIGHT_R_EN, HIGH);

  stopMotors();
}

void stopMotors() {
  analogWrite(LEFT_R_PWM, 0);
  analogWrite(LEFT_L_PWM, 0);
  analogWrite(RIGHT_R_PWM, 0);
  analogWrite(RIGHT_L_PWM, 0);
}

void forward(int speed) {
  speed = constrain(speed, 0, 255);
  analogWrite(LEFT_R_PWM, speed);
  analogWrite(LEFT_L_PWM, 0);
  analogWrite(RIGHT_R_PWM, speed);
  analogWrite(RIGHT_L_PWM, 0);
}

void backward(int speed) {
  speed = constrain(speed, 0, 255);
  analogWrite(LEFT_R_PWM, 0);
  analogWrite(LEFT_L_PWM, speed);
  analogWrite(RIGHT_R_PWM, 0);
  analogWrite(RIGHT_L_PWM, speed);
}

// Rotate in place: left side reverses, right side goes forward.
void turnLeft(int speed) {
  speed = constrain(speed, 0, 255);
  analogWrite(LEFT_R_PWM, 0);
  analogWrite(LEFT_L_PWM, speed);
  analogWrite(RIGHT_R_PWM, speed);
  analogWrite(RIGHT_L_PWM, 0);
}

// Rotate in place: right side reverses, left side goes forward.
void turnRight(int speed) {
  speed = constrain(speed, 0, 255);
  analogWrite(LEFT_R_PWM, speed);
  analogWrite(LEFT_L_PWM, 0);
  analogWrite(RIGHT_R_PWM, 0);
  analogWrite(RIGHT_L_PWM, speed);
}

// Independent forward-biased speed per side (0-255 each).
void drive(int leftSpeed, int rightSpeed) {
  leftSpeed  = constrain(leftSpeed, 0, 255);
  rightSpeed = constrain(rightSpeed, 0, 255);
  analogWrite(LEFT_R_PWM, leftSpeed);
  analogWrite(LEFT_L_PWM, 0);
  analogWrite(RIGHT_R_PWM, rightSpeed);
  analogWrite(RIGHT_L_PWM, 0);
}