#ifndef ROBOT_H
#define ROBOT_H

#include "Hardware.h"

struct EdgeReadings;

enum SearchDirection {
    SEARCH_LEFT,
    SEARCH_RIGHT
};

// ===================== START =====================
const unsigned long START_COUNTDOWN_MS = 5200;
const unsigned long START_DEBOUNCE_MS  = 50;

// ===================== SWITCH GLITCH FILTER =====================
const unsigned long SWITCH_GLITCH_MS = 100;

// ===================== SEARCH =====================
const int SEARCH_SLOW_SPEED = 120;
const int SEARCH_FAST_SPEED = 180;
const unsigned long SEARCH_FIRST_ARC_MS = 600;
const unsigned long SEARCH_ARC_FLIP_MS  = 1100;

// ===================== ATTACK / PUSH =====================
const int ATTACK_SPEED = 240;
const int HAMMER_AMPLITUDE = 50;
const unsigned long HAMMER_PERIOD_MS = 100;

const unsigned long ATTACK_COMMIT_MS = 300;

const int SENSOR_PEAK = 220;                                   // <<< REPLACE WITH YOUR MEASURED PEAK
const int PUSH_READING = (SENSOR_PEAK * 85) / 100;
static_assert(PUSH_READING > DIST_THRESHOLD + 50,
              "PUSH_READING must sit clearly above DIST_THRESHOLD - re-measure SENSOR_PEAK");
static_assert(PUSH_READING <= 1000,
              "PUSH_READING is beyond what the 10-bit ADC can reach - re-measure SENSOR_PEAK");
const unsigned long PUSH_COMMIT_MS = 1000;

const int PUSH_MAX_CORRECTION = 40;

// ===================== SIDE SENSORS =====================
const unsigned long SIDE_TURN_CONFIRM_MS = 50;
const unsigned long SIDE_TURN_MAX_MS = 800;
const unsigned long SIDE_LOCKOUT_MS  = 700;

// ===================== LOST TARGET =====================
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
const int EDGE_TURN_SPEED = 170;
const unsigned long EDGE_TURN_MS = 300;

const unsigned long REPOSITION_MS = 300;
const int REPOSITION_SPEED = 150;

// ===================== OFFSET / START MANEUVERS =====================
struct StartRoutine {
    unsigned long pivotMs;
    unsigned long moveMs;
    bool reverse;
};

// No longer used by waitForStart() (see executeDiagonalStart() below) — left
// in place in case you want to fall back to it. Safe to delete later.
const StartRoutine START_PALETTE[] = {
    {200, 300, false},
    {100, 400, false},
    {300, 200, false},
    {0,   300, false},
    {80,  250, true}
};

const unsigned long OFFSET_PIVOT_MS = 200;
const unsigned long OFFSET_FORWARD_MS = 300;
const int OFFSET_SPEED = 150;

// ===================== DIAGONAL OPENING STEP =====================
// "Turn one way, drive, turn back the other way 45°" opening move.
// PLACEHOLDER — extrapolated from EDGE_TURN_MS, not measured on the new
// chassis. TUNE ON THE RING.
const unsigned long DIAGONAL_TURN_MS = 100;    // ~45° at DIAGONAL_TURN_SPEED
const int DIAGONAL_TURN_SPEED = 170;
const unsigned long DIAGONAL_DRIVE_MS = 300;   // the "step" between the two turns
const int DIAGONAL_DRIVE_SPEED = 150;

// ===================== FUNCTIONS =====================
// True while START_BUTTON alone is held (or was, within SWITCH_GLITCH_MS) —
// standby: sensors sampling, motors idle, no round logic running.
bool startOn();

// True while BOTH switches are ON. Glitch-filtered.
bool switchesOn();
void abortAttack();
void initRobot();
void waitForStart();

extern unsigned long attackDeadline;

void commitAttack(int correction, int frontReading);
void hammerDrive(int correction);
void resetHammerState();

void edgeRecover(const EdgeReadings &edges);
bool executeBalancedOffset();
bool executeDiagonalStart();

#endif