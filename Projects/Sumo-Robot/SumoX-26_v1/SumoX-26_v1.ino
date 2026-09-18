#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Robot.h"
#if ACTIVE_STRATEGY == 1
#include "Strategy_1.h"
#else
#include "Strategy_2.h"
#endif

void setup() {
  Serial.begin(115200);
  initRobot();
  waitForStart();
}

void loop() {
  static bool trackingTarget = false;
  static unsigned int lostTargetLoops = 0;

  if (digitalRead(START_BUTTON) != LOW) {
    stopMotors();
    trackingTarget = false;
    lostTargetLoops = 0;
    waitForStart();
    return;
  }

  EdgeReadings edges = readEdgeSensors();
  if (anyEdgeDetected(edges)) {
    edgeRecover(edges);
    beginSearchArc(SEARCH_RIGHT);
    return;
  }

  OpponentReadings readings = readOpponentSensors();
  if (anyOpponentDetected(readings)) {
    trackingTarget = true;
    lostTargetLoops = 0;
    approachTarget(readings);
  } else {
    if (trackingTarget) {
      lostTargetLoops++;
      if (lostTargetLoops >= LOST_TARGET_LOOPS) {
        reposition(false);
        trackingTarget = false;
        lostTargetLoops = 0;
        beginSearchArc(SEARCH_RIGHT);
        return;
      }
    }
    updateSearchArc();
  }
}