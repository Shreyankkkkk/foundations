#ifndef ROBOT_H
#define ROBOT_H

// Keep this interface independent of the sensor implementation.  The source
// file that defines these functions should include Sensors.h before Robot.h.
struct OpponentReadings;
struct EdgeReadings;

enum TargetSide
{
    TARGET_NONE,
    TARGET_LEFT,
    TARGET_RIGHT,
    TARGET_FRONT
};

// Search state declarations
enum SearchDirection
{
    SEARCH_LEFT,
    SEARCH_RIGHT
};

// ===================== TUNABLES =====================
const unsigned long START_COUNTDOWN_MS = 5000; // rulebook-mandated
const unsigned long START_DEBOUNCE_MS = 50;

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
const unsigned long EDGE_PIVOT_MS = 150;        // initial pivot; tune on the dohyo
const unsigned long EDGE_ESCALATE_MS = 220;     // still triggered -> max power
const unsigned long EDGE_RECOVER_MAX_MS = 700;  // still triggered -> give up, return
const unsigned long EDGE_CONFIRM_CLEAR_MS = 30; // short confirmation to resume quickly

const int SIDE_TURN_MARGIN = 25;

const unsigned long REPOSITION_MS = 300;
const int REPOSITION_SPEED = 150;

// ===================== FUNCTIONS =====================
void initRobot();
void waitForStart();

// Explicit state initialization and non-blocking updater
void beginSearchArc(SearchDirection initialDir);
void updateSearchArc();

bool anyOpponentDetected(const OpponentReadings &readings);
TargetSide getTargetSide(const OpponentReadings &readings);

void approachTarget(const OpponentReadings &readings);
void attack();

void edgeRecover(EdgeReadings edges); // corner-aware: front->reverse+turn, back->forward+turn
void reposition(bool back);

#endif
