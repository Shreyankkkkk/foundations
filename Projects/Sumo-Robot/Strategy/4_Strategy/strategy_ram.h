#ifndef STRATEGY_RAM_H
#define STRATEGY_RAM_H
#include "Sensors.h"

enum RamState { RAM_SEARCH, RAM_ALIGN_LEFT, RAM_ALIGN_RIGHT, RAM_COMMIT, RAM_REACQUIRE };

void resetRamStrategy();
void updateRamStrategy();
void resetStateKeepHeading();
void forceCommit();

RamState getRamState();

float getHeadingEstimate();

#endif