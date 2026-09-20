#ifndef ROBOT_H
#define ROBOT_H

struct OpponentReadings;
struct EdgeReadings;

enum SearchDirection {
    SEARCH_LEFT,
    SEARCH_RIGHT
};

// ===================== START =====================
const unsigned long START_COUNTDOWN_MS = 5200;   // at least five seconds
const unsigned long START_DEBOUNCE_MS  = 50;

// ===================== SEARCH =====================
const int SEARCH_SLOW_SPEED = 120;
const int SEARCH_FAST_SPEED = 180;
const unsigned long SEARCH_FIRST_ARC_MS = 600;
const unsigned long SEARCH_ARC_FLIP_MS  = 1100;

// ===================== ATTACK / PUSH =====================
const int ATTACK_SPEED = 240;
const int HAMMER_AMPLITUDE = 50;
const unsigned long HAMMER_PERIOD_MS = 100;

// After the opponent disappears we keep pushing blind for this long.
const unsigned long ATTACK_COMMIT_MS = 500;
// If the last front reading was at least PUSH_READING (opponent very close,
// sensor may be in its "fold-back" zone) we keep pushing blind for longer.
// TUNE PUSH_READING from your sensor sweep: the highest reading you see
// before the value starts dropping as the opponent gets closer.
const int PUSH_READING = 1024;
const unsigned long PUSH_COMMIT_MS = 1000;
// While pushing, steering is limited to this (0-255 scale) so contact stays strong.
const int PUSH_MAX_CORRECTION = 40;
const unsigned long SIDE_TURN_CONFIRM_MS = 50;

// ===================== LOST TARGET =====================
// Opponent slipped away to a side: turn toward where it was last seen.
const unsigned long LOST_TURN_MS = 300;
const int LOST_TURN_SPEED = 150;

// ===================== EDGE RECOVERY =====================
const int EDGE_RECOVER_SPEED = 170;
const int EDGE_RECOVER_MAX_SPEED = 230;
const unsigned long EDGE_BRAKE_MS = 60;
const unsigned long EDGE_RETREAT_MS = 180;
const unsigned long EDGE_ESCALATE_MS = 220;
const unsigned long EDGE_RECOVER_MAX_MS = 900;
const unsigned long EDGE_CONFIRM_CLEAR_MS = 30;
// After backing off a FRONT edge, turn away so we don't drive straight back at it.
// TUNE EDGE_TURN_MS on the ring until the robot turns roughly 120-150 degrees.
const int EDGE_TURN_SPEED = 170;
const unsigned long EDGE_TURN_MS = 300;

const unsigned long REPOSITION_MS = 300;
const int REPOSITION_SPEED = 150;

// ===================== OFFSET / START MANEUVERS =====================
struct StartRoutine {
    unsigned long pivotMs;      // turn in place first (0 = none)
    unsigned long moveMs;    // then drive this long
    bool reverse;               // true = move backward, false = forward
};

const StartRoutine START_PALETTE[] = {
    {200, 300, false},  
    {100, 400, false},
    {300, 200, false},
    {0,   300, false},
    {80,  250, true}    // side-step: pivot ~30 deg, back up ~5-10 cm. CALIBRATE both numbers (see section 4)
};

const unsigned long OFFSET_PIVOT_MS = 200;
const unsigned long OFFSET_FORWARD_MS = 300;
const int OFFSET_SPEED = 150;

// ===================== FUNCTIONS =====================
bool switchesOn();          // true only while BOTH switches are ON
void abortAttack();
void initRobot();
void waitForStart();        // 5.2 s countdown + opening move, then returns

extern unsigned long attackDeadline;

// Opponent squarely in front right now: push, and (re)open the blind-push window.
void commitAttack(int correction, int frontReading);
// Opponent not visible but the blind-push window is still open.
void hammerDrive(int correction);
void resetHammerState();

void edgeRecover(const EdgeReadings &edges);
bool executeBalancedOffset();

#endif