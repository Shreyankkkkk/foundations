#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Strategy_Ram.h"
#include "Robot.h"

void initRobot() {
    randomSeed(micros());
    
    initMotors();
    initSensors();

    unsigned long start = millis();
    while (millis() - start < START_COUNTDOWN_MS) {
        stopMotors();   // mandatory stationary period before round logic runs
    }

    primeOpponentSensors();
    resetRamStrategy();
}

// Blocking edge-recovery: straight-line only, no rotation, so heading
// estimate in Strategy_Ram is unaffected by this call.
static void recoverFromEdge(bool frontTriggered) {
    int speed = frontTriggered ? -EDGE_RECOVER_SPEED : EDGE_RECOVER_SPEED;
    unsigned long start = millis();
    unsigned long clearedAt = 0;
    bool bailToCommit = false;

    while (millis() - start < EDGE_RECOVER_MAX_MS) {
        if (anyOpponentDetected(detectOpponent(readOpponentSensors()))) { bailToCommit = true; break; }

        EdgeReadings e = readEdgeSensors();
        bool oppositeTriggered = frontTriggered ? e.back : e.front;
        if (oppositeTriggered) break;

        bool stillOnEdge = frontTriggered ? e.front : e.back;
        if (stillOnEdge) {
            clearedAt = 0;
        } else if (clearedAt == 0) {
            clearedAt = millis();
        } else if (millis() - clearedAt > EDGE_CLEAR_CONFIRM_MS + EDGE_OVERRUN_MS) {
            break;
        }
        drive(speed, speed);
    }
    stopMotors(); primeOpponentSensors();
    if (bailToCommit) forceCommit(); else resetStateKeepHeading();
}

void robotLoop() {
    EdgeReadings e = readEdgeSensors();
    
    if (e.front && e.back) {
        stopMotors();
        primeOpponentSensors();
        resetStateKeepHeading();
        return;
}

    if (e.front) { recoverFromEdge(true); return; }
    if (e.back) { recoverFromEdge(false); return; }

    updateRamStrategy();
}