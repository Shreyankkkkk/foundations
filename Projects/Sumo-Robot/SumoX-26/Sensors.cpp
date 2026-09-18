// ============================================================================
// SumoX-26 — Sensors.cpp
// ----------------------------------------------------------------------------
// The actual sensor-reading detail lives here. Nothing outside this file
// should ever call analogRead/digitalRead on a sensor pin directly.
//
// The 4 static buffers below are how the rolling-average smoothing works:
// each opponent sensor gets its own small array, we overwrite one slot per
// loop, and average whatever's currently in the array. `static` here means
// "only visible inside this file" — Strategy code never needs to touch
// these buffers directly, only the functions below.
// ============================================================================

#include <Arduino.h>
#include "Hardware.h"
#include "Sensors.h"

static int frontLeftBuffer[SENSOR_SAMPLES];
static int frontRightBuffer[SENSOR_SAMPLES];
static int leftBuffer[SENSOR_SAMPLES];
static int rightBuffer[SENSOR_SAMPLES];
static int bufferIndex = 0;

// Averages whatever is currently sitting in one buffer. Only used inside
// this file, hence static — no other file needs to average a raw array.
static int averageBuffer(int *buffer) {
    long sum = 0;
    for (int i = 0; i < SENSOR_SAMPLES; i++) {
        sum += buffer[i];
    }
    return sum / SENSOR_SAMPLES;
}

void initSensors() {

  analogReadResolution(10);
  
  bufferIndex = 0;

  pinMode(OPPONENT_FRONT_LEFT, INPUT);
  pinMode(OPPONENT_FRONT_RIGHT, INPUT);
  pinMode(OPPONENT_LEFT, INPUT);
  pinMode(OPPONENT_RIGHT, INPUT);

  pinMode(EDGE_FRONT_LEFT, INPUT);
  pinMode(EDGE_FRONT_RIGHT, INPUT);
  pinMode(EDGE_BACK_LEFT, INPUT);
  pinMode(EDGE_BACK_RIGHT, INPUT);

  // Pre-fill every buffer with a real reading, so the very first average
  // returned isn't skewed toward zero before enough loops have run to
  // naturally fill the buffer.
  for (int i = 0; i < SENSOR_SAMPLES; i++) {
    frontLeftBuffer[i]  = analogRead(OPPONENT_FRONT_LEFT);
    frontRightBuffer[i] = analogRead(OPPONENT_FRONT_RIGHT);
    leftBuffer[i]       = analogRead(OPPONENT_LEFT);
    rightBuffer[i]      = analogRead(OPPONENT_RIGHT);
  }
}

void printSensorDebug(OpponentReadings readings, EdgeReadings edges) {
  Serial.print("OPP [FL FR L R]: ");
  Serial.print(readings.frontLeft);  Serial.print(" ");
  Serial.print(readings.frontRight); Serial.print(" ");
  Serial.print(readings.left);       Serial.print(" ");
  Serial.print(readings.right);

  Serial.print(" | EDGE [FL FR BL BR]: ");
  Serial.print(edges.frontLeft  ? "WHITE" : "black"); Serial.print(" ");
  Serial.print(edges.frontRight ? "WHITE" : "black"); Serial.print(" ");
  Serial.print(edges.backLeft   ? "WHITE" : "black"); Serial.print(" ");
  Serial.println(edges.backRight ? "WHITE" : "black");
}

OpponentReadings readOpponentSensors() {
  frontLeftBuffer[bufferIndex]  = analogRead(OPPONENT_FRONT_LEFT);
  frontRightBuffer[bufferIndex] = analogRead(OPPONENT_FRONT_RIGHT);
  leftBuffer[bufferIndex]       = analogRead(OPPONENT_LEFT);
  rightBuffer[bufferIndex]      = analogRead(OPPONENT_RIGHT);

  bufferIndex = (bufferIndex + 1) % SENSOR_SAMPLES;

  OpponentReadings readings;
  readings.frontLeft  = averageBuffer(frontLeftBuffer);
  readings.frontRight = averageBuffer(frontRightBuffer);
  readings.left       = averageBuffer(leftBuffer);
  readings.right      = averageBuffer(rightBuffer);
  return readings;
}

EdgeReadings readEdgeSensors() {
  EdgeReadings edges;
  edges.frontLeft  = (digitalRead(EDGE_FRONT_LEFT)  == EDGE_WHITE_STATE);
  edges.frontRight = (digitalRead(EDGE_FRONT_RIGHT) == EDGE_WHITE_STATE);
  edges.backLeft   = (digitalRead(EDGE_BACK_LEFT)   == EDGE_WHITE_STATE);
  edges.backRight  = (digitalRead(EDGE_BACK_RIGHT)  == EDGE_WHITE_STATE);
  return edges;
}

bool isOpponentDetected(int reading) {
  return reading > DIST_THRESHOLD;
}

bool anyEdgeDetected(EdgeReadings edges) {
  return edges.frontLeft || edges.frontRight || edges.backLeft || edges.backRight;
}