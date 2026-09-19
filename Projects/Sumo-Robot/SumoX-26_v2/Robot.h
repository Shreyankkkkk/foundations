#ifndef ROBOT_H
#define ROBOT_H

// Keep this interface independent of the sensor implementation. Source files
// that define these functions include Sensors.h before Robot.h.
struct OpponentReadings;
struct EdgeReadings;

enum TargetSide {
    TARGET_NONE,
    TARGET_LEFT,
    TARGET_RIGHT,
    TARGET_FRONT
};

// Search state declarations
enum SearchDirection {
    SEARCH_LEFT,
    SEARCH_RIGHT
};

// ===================== TUNABLES =====================
const unsigned long START_COUNTDOWN_MS = 5200; // at least five seconds
const unsigned long START_DEBOUNCE_MS = 50;
const unsigned long START_EDGE_CHECK_INTERVAL_MS = 5;

// ===================== SEARCH TUNABLES =====================
const int SEARCH_SLOW_SPEED = 120;
const int SEARCH_FAST_SPEED = 180;

// First arc from border needs to be shorter to turn inward from start position
const unsigned long SEARCH_FIRST_ARC_MS = 600;
// Standard arc time to maintain S-curve across ring
const unsigned long SEARCH_ARC_FLIP_MS = 1100;

const int APPROACH_SPEED = 165;
const int TURN_SPEED = 100;

const int ATTACK_SPEED = 240;

const int EDGE_RECOVER_SPEED = 170;
const int EDGE_RECOVER_MAX_SPEED = 230;

const unsigned long EDGE_BRAKE_MS = 60;
const unsigned long EDGE_RETREAT_MS = 180;      // straight retreat phase
const unsigned long EDGE_ESCALATE_MS = 220;     // still triggered -> max power
const unsigned long EDGE_RECOVER_MAX_MS = 700;  // still triggered -> give up, return
const unsigned long EDGE_CONFIRM_CLEAR_MS = 30; // short confirmation to resume quickly

const int SIDE_TURN_MARGIN = 25;
const int SIDE_TURN_HYSTERESIS = 10;
const unsigned long SIDE_TURN_CONFIRM_MS = 50;
const int STRATEGY2_PUSH_KP = 2;
const int HAMMER_AMPLITUDE = 50;
const unsigned long HAMMER_PERIOD_MS = 100;

struct StartRoutine {
    unsigned long pivotMs;
    unsigned long forwardMs;
};

const StartRoutine START_PALETTE[] = {
    {200, 300}, // Balanced Offset (The Standard)
    {100, 400}, // The Aggressor (Fast forward)
    {300, 200}, // The Flanker (Wider angle)
    {0, 300}    // The Blitz (Pure straight burst)
};

const unsigned long REPOSITION_MS = 300;
const int REPOSITION_SPEED = 150;

const unsigned long OFFSET_PIVOT_MS = 200;
const unsigned long OFFSET_FORWARD_MS = 300;
const int OFFSET_SPEED = 150;

// ===================== FUNCTIONS =====================
void initRobot();
void waitForStart();

void attack(int correction);
void hammerAttack(int correction);

// Returns true when the recovery limit is reached and a fallback reposition is
// required; false means the edge was cleared normally.
bool edgeRecover(const EdgeReadings &edges); // corner-aware: front->reverse+turn, back->forward+turn
bool reposition(bool back);
bool executeManeuver(unsigned long pivotMs, unsigned long forwardMs);
bool executeBalancedOffset();
bool executeRandomStart();

#endif
