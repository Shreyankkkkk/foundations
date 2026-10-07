// ============================================================================
// GP2Y0A21 calibration logger v2 - trimmed-mean, outlier-rejecting
// ----------------------------------------------------------------------------
// Wiring:
//   sensor red (Vcc)    -> UNO 5V   (with 10uF+ cap across Vcc/GND at sensor)
//   sensor black (GND)  -> UNO GND
//   sensor yellow (Vo)  -> UNO A0
//
// Change SENSOR_LABEL below and re-upload for each of your 4 sensors.
// One clean pass is enough - each point takes 100 samples, sorts them, and
// averages only the middle 60% (drops the top/bottom 20% as outliers), so
// the ripple glitches from before get thrown out automatically.
//
// Serial Monitor: 115200 baud, line ending set to "Newline".
// Output is plain CSV (distance_cm,voltage) - copy the data lines straight
// into a .csv file for the Python fitting script.
// ============================================================================

const int SENSOR_PIN = A0;
const char* SENSOR_LABEL = "S1";  // change per sensor

const float VREF   = 5.0f;
const int   ADC_MAX = 1023;

const int DISTANCES_CM[] = {10, 15, 20, 25, 30, 40, 50, 60, 70, 80};
const int NUM_DISTANCES = sizeof(DISTANCES_CM) / sizeof(DISTANCES_CM[0]);

const int SAMPLES_PER_POINT      = 100;
const unsigned long SAMPLE_INTERVAL_MS = 5;
const int TRIM_PERCENT           = 20;   // drop this % total (half off each end)

int samples[SAMPLES_PER_POINT];

int cmpInt(const void* a, const void* b) {
  return (*(int*)a - *(int*)b);
}

void waitForEnter() {
  while (Serial.available()) Serial.read();
  while (true) {
    if (Serial.available()) {
      if (Serial.read() == '\n') break;
    }
  }
}

float readTrimmedVoltage() {
  for (int i = 0; i < SAMPLES_PER_POINT; i++) {
    samples[i] = analogRead(SENSOR_PIN);
    delay(SAMPLE_INTERVAL_MS);
  }
  qsort(samples, SAMPLES_PER_POINT, sizeof(int), cmpInt);

  int trimEach = (SAMPLES_PER_POINT * TRIM_PERCENT) / 100 / 2;
  long sum = 0;
  int count = 0;
  for (int i = trimEach; i < SAMPLES_PER_POINT - trimEach; i++) {
    sum += samples[i];
    count++;
  }
  float avgCounts = (float)sum / count;
  return avgCounts * VREF / ADC_MAX;
}

void setup() {
  Serial.begin(115200);
  delay(1500);
  Serial.print("# Sensor: "); Serial.println(SENSOR_LABEL);
  Serial.println("# Full A4 sheet, held flat and perpendicular to the beam.");
  Serial.println("distance_cm,voltage");
}

void loop() {
  for (int i = 0; i < NUM_DISTANCES; i++) {
    int d = DISTANCES_CM[i];
    Serial.print("# >>> Place the A4 sheet at ");
    Serial.print(d);
    Serial.println(" cm, then press Enter.");
    waitForEnter();
    float v = readTrimmedVoltage();
    Serial.print(d);
    Serial.print(',');
    Serial.println(v, 4);
  }
  Serial.println("# Pass complete. Copy the distance_cm,voltage lines into a CSV file.");
  while (true) delay(1000);  // stop - one clean pass is enough
}
