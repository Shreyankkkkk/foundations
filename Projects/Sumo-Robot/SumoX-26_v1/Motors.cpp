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

static unsigned long motionInhibitUntil = 0;

void initMotors() {
  pinMode(LEFT_L_EN, OUTPUT);
  pinMode(LEFT_R_EN, OUTPUT);
  pinMode(LEFT_R_PWM, OUTPUT);
  pinMode(LEFT_L_PWM, OUTPUT);

  pinMode(RIGHT_L_EN, OUTPUT);
  pinMode(RIGHT_R_EN, OUTPUT);
  pinMode(RIGHT_R_PWM, OUTPUT);
  pinMode(RIGHT_L_PWM, OUTPUT);

  // Zero PWM outputs before the drivers are armed, so there's no window
  // where EN is HIGH and the PWM pins are in an unknown state.
  analogWrite(LEFT_R_PWM, 0);
  analogWrite(LEFT_L_PWM, 0);
  analogWrite(RIGHT_R_PWM, 0);
  analogWrite(RIGHT_L_PWM, 0);

  // Arm both drivers once. These stay HIGH for the entire match — they are
  // not touched again anywhere else in the code.
  digitalWrite(LEFT_L_EN, HIGH);
  digitalWrite(LEFT_R_EN, HIGH);
  digitalWrite(RIGHT_L_EN, HIGH);
  digitalWrite(RIGHT_R_EN, HIGH);

  stopMotors();
}

void inhibitMotionUntil(unsigned long deadline) {
  motionInhibitUntil = deadline;
  stopMotors();
}

void stopMotors() {
  drive(0, 0);
}

// -255 = full reverse, 0 = stop, +255 = full forward.

void drive(int leftSpeed, int rightSpeed) {
  if (leftSpeed != 0 || rightSpeed != 0) {
    if ((long)(millis() - motionInhibitUntil) < 0) {
      leftSpeed = 0;
      rightSpeed = 0;
    }
  }

  leftSpeed  = constrain(leftSpeed, -255, 255);
  rightSpeed = constrain(rightSpeed, -255, 255);

  if (LEFT_MOTOR_INVERTED) leftSpeed = -leftSpeed;
  if (RIGHT_MOTOR_INVERTED) rightSpeed = -rightSpeed;
  
  if (leftSpeed >= 0){
    analogWrite(LEFT_R_PWM, leftSpeed);
    analogWrite(LEFT_L_PWM, 0);
  } else {
    analogWrite(LEFT_R_PWM, 0);
    analogWrite(LEFT_L_PWM, -leftSpeed);
  }  

  if (rightSpeed >= 0){
    analogWrite(RIGHT_R_PWM, rightSpeed);
    analogWrite(RIGHT_L_PWM, 0);
  } else {
    analogWrite(RIGHT_R_PWM, 0);
    analogWrite(RIGHT_L_PWM, -rightSpeed);
  } 
}

void forward(int speed) {
  speed = constrain(speed, 0, 255);
  drive(speed, speed);
}

void backward(int speed) {
  speed = constrain(speed, 0, 255);
  drive(-speed, -speed);
}

// Rotate in place: left side reverses, right side goes forward.
void turnLeft(int speed) {
  speed = constrain(speed, 0, 255);
  drive(-speed, speed);
}

// Rotate in place: right side reverses, left side goes forward.
void turnRight(int speed) {
  speed = constrain(speed, 0, 255);
  drive(speed, -speed);
}
