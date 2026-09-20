#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Robot.h"
#include "Strategy_Hybrid.h"

void setup() {
  Serial.begin(115200);
  initRobot();
}

void loop() {
  static bool trackingTarget = false;
  static int lastKnownCorrection = 0;
  static bool wasReady = false;
  static unsigned long lostTurnStart = 0;

  // ---- Any switch OFF: stop and reset everything ----
  if (!switchesOn()) {
    stopMotors();
    trackingTarget = false;
    lastKnownCorrection = 0;
    lostTurnStart = 0;
    wasReady = false;
    beginSearchArc(SEARCH_RIGHT);
    return;
  }

  // ---- Switches just turned ON: 5.2 s countdown + opening move ----
  if (!wasReady) {
    wasReady = true;
    stopMotors();
    waitForStart();
    return;
  }

  // ---- Edges always come first ----
  EdgeReadings edges = readEdgeSensors();
  if (anyEdgeDetected(edges)) {
    edgeRecover(edges);
    primeOpponentSensors();      // recovery blocked the loop: drop stale readings
    trackingTarget = false;
    lostTurnStart = 0;
    beginSearchArc(SEARCH_RIGHT);
    return;
  }

  OpponentReadings readings = readOpponentSensors();

  if (anyOpponentDetected(readings)) {
    trackingTarget = true;
    lostTurnStart = 0;
    approachTarget(readings);
    lastKnownCorrection = getLastCorrection();

  } else if (trackingTarget && millis() < attackDeadline) {
    // Just lost it while pushing: keep pushing blind for a moment.
    hammerDrive(constrain(lastKnownCorrection, -PUSH_MAX_CORRECTION, PUSH_MAX_CORRECTION));

  } else if (trackingTarget) {
    int dir = getLastSeenDirection();
    if (dir != 0) {
      // It slipped away to one side: turn toward where it was, then search that way.
      if (lostTurnStart == 0) lostTurnStart = millis();
      if (millis() - lostTurnStart < LOST_TURN_MS) {
        if (dir > 0) drive(LOST_TURN_SPEED, -LOST_TURN_SPEED);
        else         drive(-LOST_TURN_SPEED, LOST_TURN_SPEED);
      } else {
        trackingTarget = false;
        lostTurnStart = 0;
        beginSearchArc(dir > 0 ? SEARCH_RIGHT : SEARCH_LEFT);
      }
    } else {
      // Lost it dead ahead after a push: your original offset maneuver.
      abortAttack();
      trackingTarget = false;
      lostTurnStart = 0;
      executeBalancedOffset();
      primeOpponentSensors();
      beginSearchArc(SEARCH_RIGHT);
    }

  } else {
    updateSearchArc();
  }
}