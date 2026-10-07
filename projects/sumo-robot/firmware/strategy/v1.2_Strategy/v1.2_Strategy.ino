#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Robot.h"
#include "Strategy_Hybrid.h"

// #define SENSOR_DEBUG

#ifdef SENSOR_DEBUG
static void sensorDebug() {
  static unsigned long lastPrint = 0;
  static int peak[4] = {0, 0, 0, 0};
  static bool wasOn = true;
  static unsigned long offSince = 0, longestOff = 0, blips = 0;

  const bool rawOn = (digitalRead(START_BUTTON) == LOW && digitalRead(ROUND_BUTTON) == LOW);
  const unsigned long now = millis();
  if (!rawOn && wasOn) { offSince = now; }
  if (rawOn && !wasOn) {
    blips++;
    if (now - offSince > longestOff) longestOff = now - offSince;
  }
  wasOn = rawOn;

  OpponentReadings r = readOpponentSensors();
  const int v[4] = {r.frontLeft, r.frontRight, r.left, r.right};
  for (int i = 0; i < 4; i++) if (v[i] > peak[i]) peak[i] = v[i];

  if (now - lastPrint < 100) return;
  lastPrint = now;

  EdgeReadings e = readEdgeSensors();
  Serial.print("FL "); Serial.print(v[0]);
  Serial.print(" FR "); Serial.print(v[1]);
  Serial.print(" L ");  Serial.print(v[2]);
  Serial.print(" R ");  Serial.print(v[3]);
  Serial.print(" | peak FL "); Serial.print(peak[0]);
  Serial.print(" FR "); Serial.print(peak[1]);
  Serial.print(" L ");  Serial.print(peak[2]);
  Serial.print(" R ");  Serial.print(peak[3]);
  Serial.print(" | E: ");
  Serial.print(e.frontLeft); Serial.print(e.frontRight);
  Serial.print(e.backLeft);  Serial.print(e.backRight);
  Serial.print(" | sw ");   Serial.print(rawOn ? "ON" : "OFF");
  Serial.print(" OFFblips "); Serial.print(blips);
  Serial.print(" longest ");  Serial.println(longestOff);
}
#endif

void setup() {
#ifdef SENSOR_DEBUG
  Serial.begin(115200);
  Serial.println("BOOT");
#endif
  initRobot();
}

#ifndef SENSOR_DEBUG
static void robotLoop() {
  static bool trackingTarget = false;
  static int lastKnownCorrection = 0;
  static bool wasReady = false;
  static unsigned long lostTurnStart = 0;
  static bool wasStarted = false;

  bool started = startOn();
  bool active  = switchesOn();

  // ---- Fully off: neither switch ----
  if (!started) {
    stopMotors();
    trackingTarget = false;
    lastKnownCorrection = 0;
    lostTurnStart = 0;
    wasReady = false;
    wasStarted = false;
    beginSearchArc(SEARCH_RIGHT);
    return;
  }

  // ---- Standby: START_BUTTON held, ROUND_BUTTON not yet pressed ----
  if (!active) {
    if (!wasStarted) {
      wasStarted = true;
      primeOpponentSensors();
    }
    stopMotors();
    readOpponentSensors();
    readEdgeSensors();
    trackingTarget = false;
    lastKnownCorrection = 0;
    lostTurnStart = 0;
    wasReady = false;
    return;
  }

  // ---- Round active: unchanged ----
  wasStarted = true;

  if (!wasReady) {
    wasReady = true;
    stopMotors();
    waitForStart();
    return;
  }

  EdgeReadings edges = readEdgeSensors();
  if (anyEdgeDetected(edges)) {
    edgeRecover(edges);
    primeOpponentSensors();
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
    hammerDrive(constrain(lastKnownCorrection, -PUSH_MAX_CORRECTION, PUSH_MAX_CORRECTION));

  } else if (trackingTarget) {
    int dir = getLastSeenDirection();
    if (dir != 0) {
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
#endif

void loop() {
#ifdef SENSOR_DEBUG
  sensorDebug();
#else
  robotLoop();
#endif
}