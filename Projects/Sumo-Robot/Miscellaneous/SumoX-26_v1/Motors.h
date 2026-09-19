#ifndef MOTORS_H
#define MOTORS_H
// ============================================================================
// SumoX-26 — Motors.h
// ----------------------------------------------------------------------------
// This is the "menu" — it just lists what motor functions exist. Strategy
// code #includes this and calls these, without knowing or caring that a
// BTS7960 or PWM pins are involved underneath.
//
// speed is -255..+255. Negative is reverse, 0 is a short brake (both
// half-bridges pulled low), positive is forward.
// ============================================================================

void initMotors();
void stopMotors();
void inhibitMotionUntil(unsigned long deadline);

void forward(int speed);
void backward(int speed);
void turnLeft(int speed);
void turnRight(int speed);

void drive(int leftSpeed, int rightSpeed);

#endif
