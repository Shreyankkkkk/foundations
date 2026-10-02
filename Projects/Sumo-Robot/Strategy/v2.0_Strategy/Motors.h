#ifndef MOTORS_H
#define MOTORS_H

void initMotors();
void stopMotors();
void drive(int leftSpeed, int rightSpeed); // -255..255

#endif