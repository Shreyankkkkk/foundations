// ============================================================================
// GP2Y0A21 calibration logger - Arduino UNO - MANUAL / press-Enter version
// ----------------------------------------------------------------------------
// Wiring (direct, no resistors - Uno is natively 5V):
//   sensor red (Vcc)    -> UNO 5V
//   sensor black (GND)  -> UNO GND
//   sensor yellow (Vo)  -> UNO A0
//
// No timers here. It prints "place target at X cm", then waits until you
// press Enter in the Serial Monitor before recording that distance and
// moving to the next one. Use a FULL A4 sheet (not a scrap piece) as the
// target for every distance, held flat and square to the sensor.
//
// Serial Monitor: 115200 baud. IMPORTANT: set the line-ending dropdown
// (bottom-right of the Serial Monitor) to "Newline" or "Both NL & CR" -
// NOT "No line ending", or your Enter presses won't be detected.
// ============================================================================

#include <Arduino.h>

const int SENSOR_PIN = A0;
const char* SENSOR_LABEL = "S1";  // change to S2/S3/S4 per sensor, re-upload

const int SAMPLES_PER_POINT            = 40;
const unsigned long SAMPLE_INTERVAL_MS = 50;

const int DISTANCES_CM[] = {5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80};
const int NUM_DISTANCES = sizeof(DISTANCES_CM) / sizeof(DISTANCES_CM[0]);

const float UNO_VREF   = 5.0f;
const int   UNO_ADCMAX = 1023;

int passNumber = 1;

float countsToVolts(float counts) {
  return counts * UNO_VREF / UNO_ADCMAX;
}

// What the UNO Q would read for the same physical voltage: halved by a
// 10k/10k divider, then digitized at 3.3V / 1023 counts.
float countsToUnoQEquiv(float counts) {
  float volts = countsToVolts(counts);
  float dividedVolts = volts * 0.5f;
  return dividedVolts / 3.3f * 1023.0f;
}

// Blocks until you press Enter in the Serial Monitor.
void waitForEnter() {
  while (Serial.available()) Serial.read();   // clear any stale input first
  while (true) {
    if (Serial.available()) {
      char c = Serial.read();
      if (c == '\n') break;
    }
  }
}

void printHeader() {
  Serial.println("pass,sensor,distance_cm,samples,adc_mean,adc_min,adc_max,adc_std,sensor_V_mean,unoq_equiv_mean");
}

void recordPoint(int distanceCm) {
  int minV = UNO_ADCMAX + 1;
  int maxV = -1;
  double sum = 0.0;
  double sumSq = 0.0;

  for (int i = 0; i < SAMPLES_PER_POINT; i++) {
    int v = analogRead(SENSOR_PIN);
    sum += v;
    sumSq += (double)v * (double)v;
    if (v < minV) minV = v;
    if (v > maxV) maxV = v;
    delay(SAMPLE_INTERVAL_MS);
  }

  float mean = (float)(sum / SAMPLES_PER_POINT);
  double variance = sumSq / SAMPLES_PER_POINT - (double)mean * (double)mean;
  if (variance < 0.0) variance = 0.0;
  float stdDev = (float)sqrt(variance);

  Serial.print(passNumber);           Serial.print(',');
  Serial.print(SENSOR_LABEL);         Serial.print(',');
  Serial.print(distanceCm);           Serial.print(',');
  Serial.print(SAMPLES_PER_POINT);    Serial.print(',');
  Serial.print(mean, 1);              Serial.print(',');
  Serial.print(minV);                 Serial.print(',');
  Serial.print(maxV);                 Serial.print(',');
  Serial.print(stdDev, 2);            Serial.print(',');
  Serial.print(countsToVolts(mean), 3);      Serial.print(',');
  Serial.println(countsToUnoQEquiv(mean), 1);
}

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("# GP2Y0A21 MANUAL calibration logger (Arduino UNO)");
  Serial.print("# Sensor: "); Serial.println(SENSOR_LABEL);
  Serial.println("# Use a FULL A4 sheet, held flat and square to the sensor.");
  Serial.println("# Press Enter in the Serial Monitor to record each distance.");
}

void loop() {
  Serial.print("# ---------- PASS ");
  Serial.print(passNumber);
  Serial.println(" ----------");
  printHeader();

  for (int i = 0; i < NUM_DISTANCES; i++) {
    int d = DISTANCES_CM[i];
    Serial.print("# >>> Place the A4 sheet at ");
    Serial.print(d);
    Serial.println(" cm, then press Enter.");
    waitForEnter();
    recordPoint(d);
  }

  Serial.print("# ---------- PASS ");
  Serial.print(passNumber);
  Serial.println(" COMPLETE. Copy the data now. Press Enter to start another pass.");
  waitForEnter();
  passNumber++;
}
