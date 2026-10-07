/*
  TCRT5000 Calibration / Diagnostic Sketch
  -----------------------------------------
  Purpose: log raw analogRead() values from all 4 edge sensors so you can
  find (a) the mounting height where white/brown/black separate cleanly,
  and (b) a per-sensor threshold to hardcode into the final sketch.

  WIRING: connect each sensor's AO (analog out) pin only.
  Do NOT use the onboard digital/comparator output for this — it's unreliable
  across identical-looking modules due to LED/phototransistor gain variance.

    Sensor 1 (Front Left)  -> A0
    Sensor 2 (Front Right) -> A1
    Sensor 3 (Back Left)   -> A2
    Sensor 4 (Back Right)  -> A3

  HOW TO USE:
    1. Mount all 4 sensors at the same fixed height above the surface.
    2. Open Serial Monitor at 9600 baud.
    3. Hold the chassis stationary over BLACK arena for ~3 seconds, note the values.
    4. Move to BROWN start line, note the values.
    5. Move to WHITE border, note the values.
    6. Repeat at 2-3 different heights if black/white values are too close.
    7. Write down, per sensor: min/max over black, brown, white.

  Output format (CSV, easy to paste into a spreadsheet):
    millis, S1, S2, S3, S4
*/

const uint8_t SENSOR_PINS[4] = {A0, A1, A2, A3};
const char* SENSOR_NAMES[4]  = {"S1_FL", "S2_FR", "S3_BL", "S4_BR"};

const unsigned long SAMPLE_INTERVAL_MS = 200; // 5 samples/sec, readable in Serial Monitor
unsigned long lastSampleTime = 0;

// Simple rolling min/max tracker per sensor, resettable via Serial ('r' + Enter)
int sensorMin[4];
int sensorMax[4];

void resetMinMax() {
  for (uint8_t i = 0; i < 4; i++) {
    sensorMin[i] = 1023;
    sensorMax[i] = 0;
  }
  Serial.println(F("--- min/max reset ---"));
}

void setup() {
  Serial.begin(9600);
  for (uint8_t i = 0; i < 4; i++) {
    pinMode(SENSOR_PINS[i], INPUT);
  }
  resetMinMax();

  Serial.println(F("TCRT5000 calibration logger started."));
  Serial.println(F("Type 'r' + Enter at any time to reset min/max tracking"));
  Serial.println(F("(do this when you move to a new surface)."));
  Serial.println();
  Serial.println(F("millis,S1_FL,S2_FR,S3_BL,S4_BR,  S1min,S1max,S2min,S2max,S3min,S3max,S4min,S4max"));
}

void loop() {
  // Allow resetting min/max between surface tests without re-flashing
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'r' || c == 'R') {
      resetMinMax();
    }
  }

  unsigned long now = millis();
  if (now - lastSampleTime < SAMPLE_INTERVAL_MS) return;
  lastSampleTime = now;

  int readings[4];
  for (uint8_t i = 0; i < 4; i++) {
    readings[i] = analogRead(SENSOR_PINS[i]);
    if (readings[i] < sensorMin[i]) sensorMin[i] = readings[i];
    if (readings[i] > sensorMax[i]) sensorMax[i] = readings[i];
  }

  Serial.print(now);
  Serial.print(',');
  for (uint8_t i = 0; i < 4; i++) {
    Serial.print(readings[i]);
    Serial.print(',');
  }
  Serial.print("  ");
  for (uint8_t i = 0; i < 4; i++) {
    Serial.print(sensorMin[i]);
    Serial.print(',');
    Serial.print(sensorMax[i]);
    if (i < 3) Serial.print(',');
  }
  Serial.println();
}
