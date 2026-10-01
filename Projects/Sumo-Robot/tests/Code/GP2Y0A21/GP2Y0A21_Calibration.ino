// ============================================================================
// GP2Y0A21 calibration logger  -  Arduino UNO Q
// ----------------------------------------------------------------------------
// What it does
//   1. Warms the sensor up for a few seconds.
//   2. Walks you through a list of distances (0 cm ... 90 cm). For each one it
//      tells you where to put the target, waits, then records 40 readings
//      and prints ONE summary line (CSV) with mean / min / max / spread.
//   3. Repeats the whole list again as "pass 2", "pass 3", ...
//
// Output is CSV so it pastes straight into Excel. Every line that is NOT data
// starts with '#', so it is easy to delete afterwards.
//
// Wiring (see the guide):
//   sensor Vcc (red)    -> UNO Q 5V pin
//   sensor GND (black)  -> UNO Q GND
//   sensor Vo (yellow)  -> 10k -> [junction] -> 1k -> A2
//                          junction -> 10k -> GND
//                          A2 -> 100 nF -> GND
//
// Serial Monitor: 115200 baud.
// ============================================================================

#include <Arduino.h>

// ============================ SETTINGS YOU EDIT =============================

// 0 = normal Serial output (try this first).
// 1 = older "Monitor" output - only if you see NOTHING in the monitor with 0.
#define USE_MONITOR 0

// 0 = step-by-step calibration table (the main test).
// 1 = live stream of readings (quick "is my wiring OK?" check).
#define LIVE_MODE 0

const int   SENSOR_PIN   = A2;            // analog pin the divider output goes to
const char* SENSOR_LABEL = "S1";          // name of the sensor under test (no commas)
const char* TARGET_LABEL = "white_card";  // what you are pointing it at (no commas)

// Change these ONLY if your circuit is different.
const float VREF_VOLTS    = 3.30f;  // ADC reference (UNO Q 3.3 V rail)
const float DIVIDER_RATIO = 2.0f;   // (R1 + R2) / R2  = (10k + 10k) / 10k = 2.0

// Test timing.
const int SAMPLES_PER_POINT            = 40;   // readings averaged per distance
const unsigned long SAMPLE_INTERVAL_MS = 50;   // sensor refreshes every ~38 ms
const int SETTLE_SECONDS               = 8;    // time you get to place the target
const int WARMUP_SECONDS               = 5;    // sensor warm-up before starting

// Distances to test, in cm, measured from the FRONT FACE of the sensor.
// Dense below 10 cm on purpose: that is where the dead zone is.
const int DISTANCES_CM[] = {
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
  12, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90
};
const int NUM_DISTANCES = sizeof(DISTANCES_CM) / sizeof(DISTANCES_CM[0]);

// ============================================================================

#if USE_MONITOR
  #include <Arduino_RouterBridge.h>
  #define LOG Monitor
#else
  #define LOG Serial
#endif

const int ADC_BITS = 12;
const int ADC_MAX  = 4095;   // 2^12 - 1

int passNumber = 1;

// ADC counts -> voltage at the SENSOR output (undoes the resistor divider).
float countsToSensorVolts(float counts) {
  return counts * VREF_VOLTS / ADC_MAX * DIVIDER_RATIO;
}

// ADC counts -> what your robot code would read with analogReadResolution(10).
float countsToRobot10bit(float counts) {
  return counts * 1023.0f / ADC_MAX;
}

void warmUp() {
  LOG.print("# Warming up sensor for ");
  LOG.print(WARMUP_SECONDS);
  LOG.println(" s ...");
  unsigned long t0 = millis();
  while (millis() - t0 < (unsigned long)WARMUP_SECONDS * 1000UL) {
    analogRead(SENSOR_PIN);
    delay(SAMPLE_INTERVAL_MS);
  }
}

void printHeader() {
  LOG.println("pass,sensor,target,distance_cm,samples,adc12_mean,adc12_min,adc12_max,adc12_std,sensor_V_mean,sensor_V_min,sensor_V_max,robot10bit_equiv");
}

void recordPoint(int distanceCm) {
  int minV = ADC_MAX + 1;
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

  LOG.print(passNumber);                                   LOG.print(',');
  LOG.print(SENSOR_LABEL);                                 LOG.print(',');
  LOG.print(TARGET_LABEL);                                 LOG.print(',');
  LOG.print(distanceCm);                                   LOG.print(',');
  LOG.print(SAMPLES_PER_POINT);                            LOG.print(',');
  LOG.print(mean, 1);                                      LOG.print(',');
  LOG.print(minV);                                         LOG.print(',');
  LOG.print(maxV);                                         LOG.print(',');
  LOG.print(stdDev, 2);                                    LOG.print(',');
  LOG.print(countsToSensorVolts(mean), 3);                 LOG.print(',');
  LOG.print(countsToSensorVolts((float)minV), 3);          LOG.print(',');
  LOG.print(countsToSensorVolts((float)maxV), 3);          LOG.print(',');
  LOG.println(countsToRobot10bit(mean), 1);
}

void runPass() {
  LOG.print("# ---------- PASS ");
  LOG.print(passNumber);
  LOG.println(" ----------");
  printHeader();

  for (int i = 0; i < NUM_DISTANCES; i++) {
    int d = DISTANCES_CM[i];

    LOG.print("# >>> Put the target at ");
    LOG.print(d);
    LOG.print(" cm now. Recording starts in ");
    LOG.print(SETTLE_SECONDS);
    LOG.println(" s.");
    delay((unsigned long)SETTLE_SECONDS * 1000UL);

    LOG.println("#     recording - hold still ...");
    recordPoint(d);
  }

  LOG.print("# ---------- PASS ");
  LOG.print(passNumber);
  LOG.println(" COMPLETE. Copy the data now. Next pass starts in 20 s. ----------");
  passNumber++;
  delay(20000);
}

void setup() {
#if USE_MONITOR
  Monitor.begin();
#else
  Serial.begin(115200);
#endif

  analogReadResolution(ADC_BITS);
  pinMode(SENSOR_PIN, INPUT);

  delay(3000);   // time for you to open the Serial Monitor

  LOG.println("# GP2Y0A21 calibration logger (Arduino UNO Q)");
  LOG.print("# Sensor: ");  LOG.print(SENSOR_LABEL);
  LOG.print("   Target: ");  LOG.println(TARGET_LABEL);

  warmUp();

#if LIVE_MODE
  LOG.println("# LIVE MODE: move your hand / target in front of the sensor.");
  LOG.println("ms,adc12,sensor_V,robot10bit_equiv");
#endif
}

void loop() {
#if LIVE_MODE
  int v = analogRead(SENSOR_PIN);
  LOG.print(millis());                              LOG.print(',');
  LOG.print(v);                                     LOG.print(',');
  LOG.print(countsToSensorVolts((float)v), 3);      LOG.print(',');
  LOG.println(countsToRobot10bit((float)v), 1);
  delay(SAMPLE_INTERVAL_MS);
#else
  runPass();
#endif
}
