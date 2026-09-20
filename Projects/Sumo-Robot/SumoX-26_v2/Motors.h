#ifndef MOTORS_H
#define MOTORS_H

// speed is -255 (full reverse) .. 0 (stop) .. +255 (full forward)

void initMotors();
void stopMotors();
void inhibitMotionUntil(unsigned long deadline);
void setMotorsEnabled(bool enabled);   // false = every drive() call outputs 0 (used by the switch filter)
void drive(int leftSpeed, int rightSpeed);

#endif
