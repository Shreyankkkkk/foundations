#ifndef MOTORS_H
#define MOTORS_H
// ============================================================================
// SumoX-26 — Motors.h
// ----------------------------------------------------------------------------
// This is the "menu" — it just lists what motor functions exist. Strategy
// code will #include this and call these, without knowing or caring that
// a BTS7960 or PWM pins are involved underneath. That's the whole point
// of splitting .h (interface) from .cpp (implementation).
//
// speed is 0-255 (PWM duty), same range analogWrite() itself takes.
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