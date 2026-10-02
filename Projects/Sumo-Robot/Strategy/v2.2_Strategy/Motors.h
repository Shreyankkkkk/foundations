#ifndef MOTORS_H
#define MOTORS_H

void initMotors();          // enables drivers, PWM 0
void disableMotorDrivers(); // EN pins LOW, PWM 0: drivers fully off (pre-power-up state)
void stopMotors();
void drive(int leftSpeed, int rightSpeed); // -255..255

#endif