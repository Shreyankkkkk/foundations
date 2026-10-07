// ============================================================================
// GP2Y0A21 calibration logger - Arduino UNO (bench test board)
// ----------------------------------------------------------------------------
// Runs on a plain Arduino UNO, not the UNO Q. The UNO is natively 5V, so the
// sensor plugs in directly - no resistors, no divider. The "unoq_equiv"
// column tells you what your UNO Q robot (3.3V, 10k/10k divider,
// analogReadResolution(10)) would actually see, so this data carries
// straight into Hardware.h. Still worth a final sanity check on the real
// UNO Q wiring before competition.
//
// Wiring (direct, NO resistors):
//   sensor red (Vcc)    -> UNO 5V
//   sensor black (GND)  -> UNO GND
//   sensor yellow (Vo)  -> UNO A0   (edit SENSOR_PIN below for other sensors)
//
// Serial Monitor: 115200 baud. Test ONE sensor at a time - edit
// SENSOR_LABEL/SENSOR_PIN and re-upload for each of your 4 units.
// ============================================================================

#include <Arduino.h>

// 0 = step-by-step calibration table (the main test)
// 1 = live stream of raw readings (quick "is my wiring OK?" check)
#define LIVE_MODE 0

const int   SENSOR_PIN   = A0;
const char* SENSOR_LABEL = "S1";          // S1, S2, S3, S4 - change per sensor
const char* TARGET_LABEL = "white_card";  // change per material you test

const int SAMPLES_PER_POINT            = 40;   // readings averaged per distance
const unsigned long SAMPLE_INTERVAL_MS = 50;   // sensor refreshes every ~38 ms
const int SETTLE_SECONDS               = 8;    // time you get to place the target
const int WARMUP_SECONDS               = 5;    // sensor warm-up before starting

// Distances to test, in cm, from the sensor's FRONT FACE. Dense below 10 cm
// on purpose - that is where the dead zone is.
const int DISTANCES_CM[] = {
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
  12, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90
};
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

void warmUp() {
  Serial.print("# Warming up sensor for ");
  Serial.print(WARMUP_SECONDS);
  Serial.println(" s ...");
  unsigned long t0 = millis();
  while (millis() - t0 < (unsigned long)WARMUP_SECONDS * 1000UL) {
    analogRead(SENSOR_PIN);
    delay(SAMPLE_INTERVAL_MS);
  }
}

void printHeader() {
  Serial.println("pass,sensor,target,distance_cm,samples,adc_mean,adc_min,adc_max,adc_std,sensor_V_mean,unoq_equiv_mean");
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
  Serial.print(TARGET_LABEL);         Serial.print(',');
  Serial.print(distanceCm);           Serial.print(',');
  Serial.print(SAMPLES_PER_POINT);    Serial.print(',');
  Serial.print(mean, 1);              Serial.print(',');
  Serial.print(minV);                 Serial.print(',');
  Serial.print(maxV);                 Serial.print(',');
  Serial.print(stdDev, 2);            Serial.print(',');
  Serial.print(countsToVolts(mean), 3);      Serial.print(',');
  Serial.println(countsToUnoQEquiv(mean), 1);
}

void runPass() {
  Serial.print("# ---------- PASS ");
  Serial.print(passNumber);
  Serial.println(" ----------");
  printHeader();

  for (int i = 0; i < NUM_DISTANCES; i++) {
    int d = DISTANCES_CM[i];
    Serial.print("# >>> Put the target at ");
    Serial.print(d);
    Serial.print(" cm now. Recording starts in ");
    Serial.print(SETTLE_SECONDS);
    Serial.println(" s.");
    delay((unsigned long)SETTLE_SECONDS * 1000UL);

    Serial.println("#     recording - hold still ...");
    recordPoint(d);
  }

  Serial.print("# ---------- PASS ");
  Serial.print(passNumber);
  Serial.println(" COMPLETE. Copy the data now. Next pass starts in 20 s. ----------");
  passNumber++;
  delay(20000);
}

void setup() {
  Serial.begin(115200);
  delay(2000);   // time for you to open the Serial Monitor

  Serial.println("# GP2Y0A21 calibration logger (Arduino UNO)");
  Serial.print("# Sensor: ");  Serial.print(SENSOR_LABEL);
  Serial.print("   Target: "); Serial.println(TARGET_LABEL);

  warmUp();

#if LIVE_MODE
  Serial.println("# LIVE MODE: move your hand / target in front of the sensor.");
  Serial.println("ms,adc,sensor_V,unoq_equiv");
#endif
}

void loop() {
#if LIVE_MODE
  int v = analogRead(SENSOR_PIN);
  Serial.print(millis());                      Serial.print(',');
  Serial.print(v);                              Serial.print(',');
  Serial.print(countsToVolts((float)v), 3);     Serial.print(',');
  Serial.println(countsToUnoQEquiv((float)v), 1);
  delay(SAMPLE_INTERVAL_MS);
#else
  runPass();
#endif
}
