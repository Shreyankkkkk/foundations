#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"

void initMotors()
{
    analogWriteResolution(8);

    pinMode(LEFT_L_EN, OUTPUT);
    pinMode(LEFT_R_EN, OUTPUT);
    pinMode(RIGHT_L_EN, OUTPUT);
    pinMode(RIGHT_R_EN, OUTPUT);

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

void stopMotors() { drive(0, 0); }

static void setSide(int rPwmPin, int lPwmPin, int speed)
{
    if (speed >= 0)
    {
        analogWrite(lPwmPin, 0);
        analogWrite(rPwmPin, speed);
    }
    else
    {
        analogWrite(rPwmPin, 0);
        analogWrite(lPwmPin, -speed);
    }
}

void drive(int leftSpeed, int rightSpeed)
{
    leftSpeed = constrain(leftSpeed, -255, 255);
    rightSpeed = constrain(rightSpeed, -255, 255);

    if (LEFT_MOTOR_INVERTED)
        leftSpeed = -leftSpeed;
    if (RIGHT_MOTOR_INVERTED)
        rightSpeed = -rightSpeed;

    setSide(LEFT_R_PWM, LEFT_L_PWM, leftSpeed);
    setSide(RIGHT_R_PWM, RIGHT_L_PWM, rightSpeed);
}