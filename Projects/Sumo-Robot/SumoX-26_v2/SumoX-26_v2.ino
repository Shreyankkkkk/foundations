#include <Arduino.h>
#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"
#include "Robot.h"
#include "Strategy_Hybrid.h"

// ---------------------------------------------------------------------------
// BENCH MODE. Uncomment the next line, upload, open the serial monitor.
// The robot does NOT move in this mode. Use it to:
//   1. measure SENSOR_PEAK (Robot.h): slide a flat card toward each FRONT sensor
//      from 20 cm to 1 cm and read the "peak" column,
//   2. check DIST_THRESHOLD against real distances (calibrated readings),
//   3. check the edge sensors (E: FL FR BL BR, 1 = sees white),
//   4. tap / shake the chassis while watching "OFFblips": every count is a switch
//      glitch. "longest" is the longest one in ms; it must stay well below
//      SWITCH_GLITCH_MS (Robot.h),
//   5. spot brown-outs: a second "BOOT" line appearing mid-test = the MCU reset.
// Comment it out again for the competition build.
// ---------------------------------------------------------------------------
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

  // ---- Any switch OFF (for real, not a blip): stop and reset everything ----
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
#endif

void loop() {
#ifdef SENSOR_DEBUG
  sensorDebug();
#else
  robotLoop();
#endif
}
