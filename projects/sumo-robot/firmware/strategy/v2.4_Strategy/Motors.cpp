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

void disableMotorDrivers()
{
    pinMode(LEFT_L_EN, OUTPUT);
    pinMode(LEFT_R_EN, OUTPUT);
    pinMode(RIGHT_L_EN, OUTPUT);
    pinMode(RIGHT_R_EN, OUTPUT);
    digitalWrite(LEFT_L_EN, LOW);
    digitalWrite(LEFT_R_EN, LOW);
    digitalWrite(RIGHT_L_EN, LOW);
    digitalWrite(RIGHT_R_EN, LOW);
    analogWrite(LEFT_R_PWM, 0);
    analogWrite(LEFT_L_PWM, 0);
    analogWrite(RIGHT_R_PWM, 0);
    analogWrite(RIGHT_L_PWM, 0);
}

void stopMotors() { drive(0, 0, true); }

static int curL = 0, curR = 0;
static unsigned long lastDriveMs = 0;

static int slewToward(int cur, int target, int maxStep)
{
    if (cur != 0 && target != 0 && ((cur > 0) != (target > 0)))
        return 0; // reversal: pass through zero (brake) first
    int curMag = cur < 0 ? -cur : cur;
    int tgtMag = target < 0 ? -target : target;
    if (tgtMag <= curMag)
        return target; // slowing down is never delayed
    int mag = curMag + (((tgtMag - curMag) < maxStep) ? (tgtMag - curMag) : maxStep);
    return (target < 0) ? -mag : mag;
}

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

void drive(int leftSpeed, int rightSpeed, bool immediate)
{
    leftSpeed = constrain(leftSpeed, -255, 255);
    rightSpeed = constrain(rightSpeed, -255, 255);

    unsigned long now = millis();
    if (MOTOR_SLEW_ENABLED && !immediate)
    {
        int maxStep = (int)ceilf(MOTOR_SLEW_PWM_PER_MS * (float)(now - lastDriveMs));
        leftSpeed = slewToward(curL, leftSpeed, maxStep);
        rightSpeed = slewToward(curR, rightSpeed, maxStep);
    }
    curL = leftSpeed;
    curR = rightSpeed;
    lastDriveMs = now;

    if (LEFT_MOTOR_INVERTED)
        leftSpeed = -leftSpeed;
    if (RIGHT_MOTOR_INVERTED)
        rightSpeed = -rightSpeed;

    setSide(LEFT_R_PWM, LEFT_L_PWM, leftSpeed);
    setSide(RIGHT_R_PWM, RIGHT_L_PWM, rightSpeed);
}

int getAppliedLeft() { return curL; }
int getAppliedRight() { return curR; }