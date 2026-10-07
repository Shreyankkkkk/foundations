// ============================================================================
// TCRT5000 bench test - Arduino UNO (bare 4-leg component, no onboard module)
// ----------------------------------------------------------------------------
// Streams live readings so you can compare white paper vs your actual arena
// floor material, at the real close-range gap the sensor will sit at on the
// robot (2-10 mm - MUCH closer than the GP2Y0A21).
//
// Wiring (see chat for how to identify the LED pair vs phototransistor pair):
//   LED anode                 -> 220R -> UNO 5V
//   LED cathode                -> UNO GND
//   Phototransistor collector -> 10k pull-up -> UNO 5V
//                              -> UNO A1
//   Phototransistor emitter   -> UNO GND
//
// Serial Monitor: 115200 baud.
// ============================================================================

#include <Arduino.h>

const int SENSOR_PIN = A1;
const unsigned long SAMPLE_INTERVAL_MS = 100;

void setup() {
  Serial.begin(115200);
  delay(2000);

  pinMode(SENSOR_PIN, INPUT);

  Serial.println("# TCRT5000 bench test");
  Serial.println("# Hold each material 2-10 mm from the sensor face - try a");
  Serial.println("# few distances if you don't know your final mounting gap.");
  Serial.println("# With the wiring above, MORE reflection normally pulls the");
  Serial.println("# reading DOWN (toward 0). Confirm this is true on your");
  Serial.println("# actual circuit before trusting it - swapped legs flip it.");
  Serial.println("#");
  Serial.println("# digitalRead applies Arduino's own ~2.5V logic threshold to");
  Serial.println("# this same analog pin for free. If it reliably flips HIGH/LOW");
  Serial.println("# between white and your floor color, your existing robot code");
  Serial.println("# (which uses digitalRead on the edge pins) can work as-is.");
  Serial.println("# If it does NOT flip cleanly, you'll need to read the analog");
  Serial.println("# value instead and pick your own threshold in software.");
  Serial.println("#");
  Serial.println("ms,adc,volts,digitalRead");
}

void loop() {
  int a = analogRead(SENSOR_PIN);
  int d = digitalRead(SENSOR_PIN);
  float v = a * 5.0f / 1023.0f;

  Serial.print(millis());     Serial.print(',');
  Serial.print(a);            Serial.print(',');
  Serial.print(v, 3);         Serial.print(',');
  Serial.println(d == HIGH ? "HIGH" : "LOW");

  delay(SAMPLE_INTERVAL_MS);
}
