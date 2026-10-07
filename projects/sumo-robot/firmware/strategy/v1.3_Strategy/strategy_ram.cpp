#include <Arduino.h>
#include <math.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Strategy_Ram.h"

static float headingDeg = 0;
static float sweepBound = SEARCH_MAX_SWEEP_DEG;

static unsigned long lastUpdateMs = 0;

static unsigned long reacquireStart = 0;

static int lastAlignDir = 0;   // +1 left, -1 right, 0 none
static int alignFlipCount = 0;

static void trackHeading(int sign, int pwmMagnitude = 0) {
    unsigned long now = millis();
    unsigned long dt = now - lastUpdateMs;
    lastUpdateMs = now;
    if (sign != 0) headingDeg += sign * (TURN_RATE_DEG_PER_MS * pwmMagnitude / 255.0f) * dt;
}
float getHeadingEstimate() { return headingDeg; }

static bool sweepPositive = true;
static unsigned long lastCreepAt = 0;

static bool creeping = false;
static unsigned long creepStartMs = 0;

static void updateSearch() {
    if (creeping) {
        drive(CREEP_SPEED, CREEP_SPEED); trackHeading(0);
        if (millis() - creepStartMs >= CREEP_PULSE_MS) { creeping = false; lastCreepAt = millis(); }
        return;
    }

    if (sweepPositive && headingDeg > sweepBound)  { sweepPositive = false; sweepBound = SEARCH_MAX_SWEEP_DEG + random(-20, 21); }
    if (!sweepPositive && headingDeg < -sweepBound) { sweepPositive = true;  sweepBound = SEARCH_MAX_SWEEP_DEG + random(-20, 21); }

    bool nearCenter = fabs(headingDeg) < CREEP_ALLOWED_HEADING_BAND_DEG;
    bool creepDue = millis() - lastCreepAt > CREEP_PULSE_MS * 2;

    if (nearCenter && creepDue) {
        creeping = true; creepStartMs = millis();
        drive(CREEP_SPEED, CREEP_SPEED); trackHeading(0);
        return;
    }
    if (sweepPositive) { drive(SEARCH_SPIN_SPEED, -SEARCH_SPIN_SPEED); trackHeading(+1, SEARCH_SPIN_SPEED); }
    else               { drive(-SEARCH_SPIN_SPEED, SEARCH_SPIN_SPEED); trackHeading(-1, SEARCH_SPIN_SPEED); }
}

const int ALIGN_SPEED = 170;
const int RAMP_START_SPEED = 60;
const int RAMP_MAX_SPEED   = 255;
const unsigned long RAMP_TIME_MS = 120;
const unsigned long COMMIT_HOLD_MS = 400;

static RamState state = RAM_SEARCH;
static unsigned long commitStart = 0;
static unsigned long lastDetectTime = 0;
static unsigned long alignStart = 0;
static bool engagedLatched = false;
static unsigned long engagedSinceMs = 0;

static void enterAlign(int dir, unsigned long now) {
    if (lastAlignDir != 0 && dir != lastAlignDir) alignFlipCount++;
    lastAlignDir = dir;
    if (alignFlipCount >= ALIGN_FLIP_LIMIT) {
        state = RAM_COMMIT; commitStart = now;
        alignFlipCount = 0; lastAlignDir = 0;
        return;
    }
    state = (dir > 0) ? RAM_ALIGN_LEFT : RAM_ALIGN_RIGHT;
    alignStart = now;
}

RamState getRamState() { return state; }

void resetRamStrategy() {
    state = RAM_SEARCH;
    headingDeg = 0;
    lastUpdateMs = millis();
    alignFlipCount = 0; lastAlignDir = 0;
    sweepPositive = true;
    engagedLatched = false;
}

void resetStateKeepHeading() {
    state = RAM_SEARCH;
    lastUpdateMs = millis();
    alignFlipCount = 0; lastAlignDir = 0;
    engagedLatched = false;
}

static void goSearch() {
    state = RAM_SEARCH;
    alignFlipCount = 0; lastAlignDir = 0;
}

void forceCommit() { 
    state = RAM_COMMIT; 
    commitStart = millis(); 
    engagedLatched = true; 
    engagedSinceMs = millis();
    alignFlipCount = 0; 
    lastAlignDir = 0; 
}

void updateRamStrategy() {
    OpponentReadings raw = readOpponentSensors();
    OpponentDetection d = detectOpponent(raw);

    switch (state) {

        case RAM_SEARCH:
            if (d.center)      { state = RAM_COMMIT; commitStart = millis(); }
            else if (d.left)   { enterAlign(+1, millis()); }
            else if (d.right)  { enterAlign(-1, millis()); }
            else                updateSearch();
            break;

        case RAM_ALIGN_LEFT:
            if (d.center) {
                state = RAM_COMMIT; commitStart = millis();
            } else if (d.right && !d.left) {
                enterAlign(-1, millis());
            } else if (!d.left && !d.right) {
                goSearch();
            } else if (millis() - alignStart > ALIGN_TIMEOUT_MS) {
                state = RAM_COMMIT; commitStart = millis();
            } else {
                drive(ALIGN_SPEED, -ALIGN_SPEED); trackHeading(+1, ALIGN_SPEED);
            }
            break;

        case RAM_ALIGN_RIGHT:
            if (d.center) {
                state = RAM_COMMIT; commitStart = millis();
            } else if (d.left && !d.right) {
                enterAlign(+1, millis());
            } else if (!d.left && !d.right) {
                goSearch();
            } else if (millis() - alignStart > ALIGN_TIMEOUT_MS) {
                state = RAM_COMMIT; commitStart = millis();
            } else {
                drive(-ALIGN_SPEED, ALIGN_SPEED); trackHeading(-1, ALIGN_SPEED);
            }
            break;

        case RAM_COMMIT: {
            bool stillSeen = d.center || d.left || d.right;
            if (anyEngaged(d)) {
                if (!engagedLatched) engagedSinceMs = millis();  // only stamp on the transition
                engagedLatched = true;
            }
            if (stillSeen) lastDetectTime = millis();

            int leftAdj = 0, rightAdj = 0;
            if (!d.center) {
                if (d.left && !d.right)      { leftAdj = -TRACK_CORRECTION; rightAdj = +TRACK_CORRECTION; }
                else if (d.right && !d.left) { leftAdj = +TRACK_CORRECTION; rightAdj = -TRACK_CORRECTION; }
            }

            if (engagedLatched) {
                if (!anyOpponentDetected(d) && (millis() - lastDetectTime > LOST_CONTACT_GRACE_MS)) {              // lost them completely — don't wait out the full cap blind
                    state = RAM_REACQUIRE; reacquireStart = millis(); engagedLatched = false;
                    break;
                }
                drive(RAMP_MAX_SPEED + leftAdj, RAMP_MAX_SPEED + rightAdj);
                trackHeading(0);
                break;
            }

            if (millis() - lastDetectTime > COMMIT_HOLD_MS) {
                goSearch();
                break;
            }
            unsigned long elapsed = millis() - commitStart;
            int speed = (elapsed >= RAMP_TIME_MS) ? RAMP_MAX_SPEED
                : map(elapsed, 0, RAMP_TIME_MS, RAMP_START_SPEED, RAMP_MAX_SPEED);
            drive(speed + leftAdj, speed + rightAdj);
            trackHeading(0);
            break;
        }

        case RAM_REACQUIRE: 
            if (d.center)      { state = RAM_COMMIT; commitStart = millis(); }
            else if (d.left)   enterAlign(+1, millis());
            else if (d.right)  enterAlign(-1, millis());
            else if (millis() - reacquireStart > RAM_REACQUIRE_MS) goSearch();
            else { drive(REACQUIRE_SPEED, REACQUIRE_SPEED); trackHeading(0); }
            break;
    }
}