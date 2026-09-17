#ifndef SENSORS_H
#define SENSORS_H

// ============================================================================
// SumoX-26 — Sensors.h
// ----------------------------------------------------------------------------
// Same pattern as Motors.h: this is the menu, not the kitchen. Strategy code
// calls these functions and reads these structs without ever touching
// analogRead/digitalRead or a raw pin number directly.
//
// Tunables (DIST_THRESHOLD, EDGE_WHITE_STATE, SENSOR_SAMPLES) live in
// Hardware.h now, not here — this file just uses them.
//
// Two structs, one per sensor family:
//   - OpponentReadings holds a smoothed number per GP2Y0A21. Strategy1 needs
//     the actual numbers (for the proportional steering math), so this
//     struct exposes raw-ish values, not just yes/no.
//   - EdgeReadings holds a true/false per TCRT5000. There's no "how white"
//     concept that matters here, so this one is just booleans.
// ============================================================================

#include "Hardware.h"

// ===================== DATA STRUCTS =====================

// One smoothed (averaged) reading per opponent sensor.
struct OpponentReadings {
  int frontLeft;
  int frontRight;
  int left;
  int right;
};
// basically packages the 4 outputs of the GP2Y0A21 sensors into a single struct for easy passing around

// One true/false per edge sensor. true = white/edge detected at that corner.
struct EdgeReadings {
  bool frontLeft;
  bool frontRight;
  bool backLeft;
  bool backRight;
};
// basically packages the 4 outputs of the edge sensors into a single struct for easy passing around


// ===================== FUNCTIONS =====================

// Set all 8 sensor pins to the correct pinMode. Call once from setup().
void initSensors();

// Reads all 4 GP2Y0A21 pins, pushes each into its own rolling buffer, and
// returns the averaged result for this loop.
OpponentReadings readOpponentSensors(); // no void cause the function is supposed to return something
// returns 4 numbers between 0-1023, one per sensor. Higher = Closer object.

// Reads all 4 TCRT5000 pins and returns which corners currently see white.
EdgeReadings readEdgeSensors();
// returns 4 booleans, one per corner. true = white detected at that corner.

// Convenience check: does this one smoothed reading count as "opponent
// detected"? Strategy code should call this instead of comparing against
// DIST_THRESHOLD directly, so the threshold only ever lives in one place.
bool isOpponentDetected(int reading);
// takes an interger reading (0-1023) and returns true if the reading is above DIST_THRESHOLD, false otherwise

// Convenience check: is ANY corner currently seeing white? This is the
// exact call the shared core's checkEdges() step makes every loop, before
// any drive command is allowed to run.
bool anyEdgeDetected(EdgeReadings edges);
// takes an EdgeReadings struct and returns true if any of the 4 booleans are true, false otherwise

#endif