// ============================================================================
// SumoX-26 - Sensor bench monitor
// ----------------------------------------------------------------------------
// Streams MEDIAN-filtered live readings from all 4 opponent (GP2Y0A21) pins
// at once, continuously. No button presses, no per-sensor re-upload - just
// watch the numbers and write down what you need.
//
// TWO USES:
//
// 1) NO-OBJECT FLOOR (for setting DIST_THRESHOLD):
//    Power it up with nothing in front of any sensor - point the robot at
//    open air, or somewhere nothing is within ~1m. Let it run untouched for
//    10-20s. Whatever each column settles around (note the max, not just
//    the typical value - glitches happen) is that sensor's noise floor.
//    Set DIST_THRESHOLD comfortably above the HIGHEST floor you see across
//    all 4, with margin (e.g. floor maxes out at ~60 -> threshold >= 100).
//
// 2) CALIBRATION:
//    Hold a full A4 sheet, flat and perpendicular, at a known distance in
//    front of ONE sensor at a time (ignore the other columns). Wait about a
//    second for that column's number to settle, then write down
//    (distance_cm, voltage) from its _v column. Repeat at ~6 distances -
//    10, 20, 30, 45, 60, 80 cm is plenty - then move to the next sensor.
//    No re-uploading between sensors, it's all live in one sketch.
//    Feed the (distance,voltage) pairs you collect for each sensor into
//    fit_calibration.py exactly like before, one CSV per sensor.
//
// Wiring matches Hardware.h: A0 FL, A1 FR, A2 L, A3 R.
// When you move to 3 opponent sensors, just delete the pin you no longer
// have and the matching print columns below.
// ============================================================================

#include <Arduino.h>

const int PIN_FL = A0;
const int PIN_FR = A1;
const int PIN_L  = A2;
const int PIN_R  = A3;

const float VREF     = 5.0f;
const int   ADC_MAX   = 1023;

const int MEDIAN_SAMPLES        = 7;   // odd -> true median, no averaging
const unsigned long SAMPLE_GAP_MS   = 3;
const unsigned long PRINT_INTERVAL_MS = 200;

unsigned long lastPrint = 0;

int medianRead(int pin) {
  int buf[MEDIAN_SAMPLES];
  for (int i = 0; i < MEDIAN_SAMPLES; i++) {
    buf[i] = analogRead(pin);
    delay(SAMPLE_GAP_MS);
  }
  for (int i = 1; i < MEDIAN_SAMPLES; i++) {           // insertion sort, tiny array
    int v = buf[i];
    int j = i - 1;
    while (j >= 0 && buf[j] > v) { buf[j + 1] = buf[j]; j--; }
    buf[j + 1] = v;
  }
  return buf[MEDIAN_SAMPLES / 2];
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("millis,FL_raw,FL_v,FR_raw,FR_v,L_raw,L_v,R_raw,R_v");
}

void loop() {
  if (millis() - lastPrint < PRINT_INTERVAL_MS) return;
  lastPrint = millis();

  int fl = medianRead(PIN_FL);
  int fr = medianRead(PIN_FR);
  int l  = medianRead(PIN_L);
  int r  = medianRead(PIN_R);

  Serial.print(millis());                          Serial.print(',');
  Serial.print(fl); Serial.print(','); Serial.print(fl * VREF / ADC_MAX, 3); Serial.print(',');
  Serial.print(fr); Serial.print(','); Serial.print(fr * VREF / ADC_MAX, 3); Serial.print(',');
  Serial.print(l);  Serial.print(','); Serial.print(l  * VREF / ADC_MAX, 3); Serial.print(',');
  Serial.print(r);  Serial.print(','); Serial.println(r * VREF / ADC_MAX, 3);
}
