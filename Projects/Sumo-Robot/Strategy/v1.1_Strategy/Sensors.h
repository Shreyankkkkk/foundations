#ifndef SENSORS_H
#define SENSORS_H

// ============================================================================
// SumoX-26 — Sensors.h
// ----------------------------------------------------------------------------
// Same pattern as Motors.h: this is the menu, not the kitchen. Strategy code
// calls these functions and reads these structs without ever touching
// analogRead/digitalRead or a raw pin number directly.
//
// All tunables live in Hardware.h — this file only uses them.
// ============================================================================

#include "Hardware.h"

// ===================== DATA STRUCTS =====================

// One filtered, trimmed reading per opponent sensor, in ADC counts
// (0..ADC_MAX). Higher = closer, but ONLY down to about 10 cm — see the
// warning on readOpponentSensors() below.
struct OpponentReadings {
  int frontLeft;
  int frontRight;
  int left;
  int right;
};

// One true/false per edge sensor. true = white/edge detected at that corner.
struct EdgeReadings {
  bool frontLeft;
  bool frontRight;
  bool backLeft;
  bool backRight;
};

// ===================== FUNCTIONS =====================

// Set all sensor pins to the correct pinMode and prime the filters.
// Call once from setup(), before anything reads a sensor.
void initSensors();

// Opens the USB serial link for bench work and waits briefly for a terminal
// to attach. Call this from setup() BEFORE printSensorDebug() will do
// anything at all — without it every print is silently discarded.
// Safe to leave in for a match: it gives up waiting after a second.
void initSensorDebug();

// Prints every current sensor value over serial, one line, for bench
// calibration and continuity testing. Does nothing if serial is not open.
void printSensorDebug(OpponentReadings readings, EdgeReadings edges);

// Samples the GP2Y0A21 sensors at their real ~40 ms update rate, keeps a
// rolling history, and returns the per-channel MEDIAN with each channel's
// Hardware.h trim applied. Cheap to call every loop — it only recomputes
// when a genuinely new sample has arrived.
//
// BLIND ZONE WARNING: the GP2Y0A21 is specified from 10 cm to 80 cm. Below
// about 10 cm its output voltage FALLS again as the target gets closer, so a
// robot pressed against your wedge reads the same as one 30 cm away. Never
// treat a falling front reading as "the opponent left" — that is exactly
// when it is touching you. Robot.cpp's attack commit latch exists to cover
// this; see attack()/attackCommitted() in Robot.h.
OpponentReadings readOpponentSensors();

// Reads all 4 TCRT5000 pins and returns which corners currently see white.
// A corner has to report the same state on EDGE_CONFIRM_READS consecutive
// calls before the change is accepted, which removes single-sample glitches
// without adding meaningful latency.
EdgeReadings readEdgeSensors();

// Bypasses the confirmation filter and returns the instantaneous pin states.
// Only useful for bench diagnostics.
EdgeReadings readEdgeSensorsRaw();

// Does this one filtered reading count as "opponent detected"? Strategy code
// calls this instead of comparing against DIST_THRESHOLD directly, so the
// threshold only ever lives in one place.
bool isOpponentDetected(int reading);

// Is ANY corner currently seeing white? This is the exact call the main
// loop's edge check makes every iteration, before any drive command.
bool anyEdgeDetected(EdgeReadings edges);

#endif
