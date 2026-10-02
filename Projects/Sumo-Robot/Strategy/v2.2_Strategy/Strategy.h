#ifndef STRATEGY_H
#define STRATEGY_H
#include "Sensors.h"

struct MotorCommand
{
    int leftPwm;
    int rightPwm;
};

enum StrategyState
{
    STATE_OPEN_SWEEP,
    STATE_SEARCH,
    STATE_ALIGN,
    STATE_COMMIT,
    STATE_RETURN,
    STATE_STALEMATE_BREAK
};

void resetStrategy(bool seenAtKickoff);
MotorCommand updateStrategy(const OpponentDetection &d);

void strategyForceCommit();
void strategyForceReturn();
void strategyEngage();

StrategyState getStrategyState();

#endif