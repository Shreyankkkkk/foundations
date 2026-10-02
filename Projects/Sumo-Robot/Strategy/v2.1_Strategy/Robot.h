#ifndef ROBOT_H
#define ROBOT_H
#include "Hardware.h"
#include "Sensors.h"
#include "Map.h"
#include "Strategy.h" // must define: struct MotorCommand{int leftPwm,rightPwm;};
                      // MotorCommand updateStrategy(const OpponentDetection&);
                      // void resetStrategy(bool seenAtKickoff);
                      // void strategyForceCommit();
                      // void strategyForceReturn();

void initRobot();
void robotLoop();

#endif