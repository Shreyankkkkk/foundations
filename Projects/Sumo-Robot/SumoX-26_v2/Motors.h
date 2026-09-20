#ifndef MOTORS_H
#define MOTORS_H

// speed is -255 (full reverse) .. 0 (stop) .. +255 (full forward)

void initMotors();
void stopMotors();
void inhibitMotionUntil(unsigned long deadline);
void drive(int leftSpeed, int rightSpeed);

#endif