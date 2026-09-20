#ifndef ROBOT_H
#define ROBOT_H

#include "Hardware.h"

struct EdgeReadings;

enum SearchDirection {
    SEARCH_LEFT,
    SEARCH_RIGHT
};

// ===================== START =====================
const unsigned long START_COUNTDOWN_MS = 5200;   // at least five seconds
const unsigned long START_DEBOUNCE_MS  = 50;     // both switches must read ON this long before the countdown starts

// ===================== SWITCH GLITCH FILTER =====================
// A switch that reads OFF for LESS than this is treated as contact bounce / wire
// vibration: motors are cut for that instant but the round keeps running (no
// reset, no new 5 s countdown). OFF for this long or more = a real OFF: full reset.
// Far shorter than any human flick of a rocker switch. Raise it if your vibration
// test (SENSOR_DEBUG) still shows OFF blips longer than 100 ms.
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

// After the opponent disappears we keep pushing blind for this long.
// (Was 500 ms = a ~25 cm blind lunge at full power; a dodging opponent made you
//  run at the edge. 300 ms is enough to bridge a sensor dropout.)
const unsigned long ATTACK_COMMIT_MS = 300;

// If the last front reading was CLOSE (opponent touching / in the sensor's fold-back
// zone) we keep pushing blind for longer.
//
// SENSOR_PEAK = the highest reading a front sensor gives as an object approaches,
// BEFORE the value starts dropping again (GP2Y0A21 peaks at ~6 cm and folds back
// below that). MEASURE IT: build with SENSOR_DEBUG (see the .ino), slide a flat
// card toward a front sensor from 20 cm to 1 cm, and read the "peak" column.
// 960 is only a placeholder that assumes the sensor goes straight into the ADC
// (about 3.1 V at 3.3 V full scale). With a 10k/10k divider the peak is about half.
const int SENSOR_PEAK = 960;                                   // <<< REPLACE WITH YOUR MEASURED PEAK
const int PUSH_READING = (SENSOR_PEAK * 85) / 100;             // "close" = within 85 % of the peak
// Compile-time guard: PUSH_READING used to be 1024, which the 10-bit ADC can never
// reach, so the long-push branch silently never ran. This makes that impossible.
static_assert(PUSH_READING > DIST_THRESHOLD + 50,
              "PUSH_READING must sit clearly above DIST_THRESHOLD - re-measure SENSOR_PEAK");
static_assert(PUSH_READING <= 1000,
              "PUSH_READING is beyond what the 10-bit ADC can reach - re-measure SENSOR_PEAK");
const unsigned long PUSH_COMMIT_MS = 1000;

// While pushing, steering is limited to this (0-255 scale) so contact stays strong.
const int PUSH_MAX_CORRECTION = 40;

// ===================== SIDE SENSORS =====================
const unsigned long SIDE_TURN_CONFIRM_MS = 50;
// A side sensor can only ever justify turning until the front sensors pick the
// opponent up (well under a full rotation). If one keeps asking for longer than
// this, it is stuck / seeing part of the robot or the arena: ignore it for a while.
const unsigned long SIDE_TURN_MAX_MS = 800;
const unsigned long SIDE_LOCKOUT_MS  = 700;

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
    unsigned long moveMs;       // then drive this long
    bool reverse;               // true = move backward, false = forward
};

const StartRoutine START_PALETTE[] = {
    {200, 300, false},
    {100, 400, false},
    {300, 200, false},
    {0,   300, false},
    {80,  250, true}    // side-step: pivot ~30 deg, back up ~5-10 cm. CALIBRATE both numbers
};

const unsigned long OFFSET_PIVOT_MS = 200;
const unsigned long OFFSET_FORWARD_MS = 300;
const int OFFSET_SPEED = 150;

// ===================== FUNCTIONS =====================
// True while BOTH switches are ON. Glitch-filtered: a raw OFF shorter than
// SWITCH_GLITCH_MS still returns true, but the motors are gated off for that time.
// Poll it from every loop that can run longer than a few ms.
bool switchesOn();
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
