// ============================================================================
// TCRT5000 (Besomi module) height-sweep test - Arduino UNO
// ----------------------------------------------------------------------------
// This module's OUT pin is already a clean digital signal (comparator built
// in) - no resistors needed. Wire: VCC -> UNO 5V, GND -> UNO GND, OUT -> pin 2.
//
// Only prints when the state CHANGES, with a timestamp. Procedure:
//   1. Hold your test material touching the sensor. Confirm it prints HIGH.
//   2. Slowly pull the material away using known-thickness shims (coins,
//      stacked cardstock, etc).
//   3. Note the millis() timestamp the moment it flips to LOW, and what
//      shim height you were at - that's this sensor's trigger distance
//      for this material.
//   4. Repeat per material (white / black / brown) and per sensor (move
//      the OUT wire to test each of your 4 units).
// ============================================================================

#include <Arduino.h>

const int SENSOR_PIN = 2;

int lastState = -1;

void setup() {
  Serial.begin(115200);
  delay(1000);
  pinMode(SENSOR_PIN, INPUT);
  Serial.println("# TCRT5000 sweep test - only prints on state change");
  Serial.println("# Write down the shim height you were at when a line prints");
  Serial.println("ms,state");
}

void loop() {
  int state = digitalRead(SENSOR_PIN);
  if (state != lastState) {
    Serial.print(millis());
    Serial.print(',');
    Serial.println(state == HIGH ? "HIGH" : "LOW");
    lastState = state;
  }
}
