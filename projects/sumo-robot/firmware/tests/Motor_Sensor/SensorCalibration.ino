// ============================================================================
// SumoX-26 — SensorCalibration.ino
// ----------------------------------------------------------------------------
// STANDALONE bench sketch. It does not use any of the SumoX-26 files — copy
// this whole folder somewhere separate and open it on its own.
//
// WHAT IT IS FOR
//   Everything in Hardware.h that says "placeholder" gets its real value from
//   this sketch. It prints RAW, unfiltered readings so you can see exactly
//   what the hardware does, including the things the filtered code hides.
//
// HOW TO USE IT
//   1. Upload. Open Serial Monitor at 115200 baud.
//   2. It prints a line ~4x a second with live values, plus the running
//      minimum and maximum each channel has hit since the last reset.
//   3. Send any character to reset the min/max trackers.
//
// THE FOUR THINGS TO MEASURE
//
//   A) ADC FULL SCALE. Look at the max column. If nothing ever exceeds 1023
//      even with a target right in front of a sensor, the 12-bit setting did
//      not take — set ADC_RESOLUTION_BITS to 10 and ADC_MAX to 1023 in
//      Hardware.h, and divide every threshold in Robot.h by 4.
//
//   B) DIST_THRESHOLD. Two numbers you need:
//        - Point the robot across an EMPTY ring. Note the max. Your threshold
//          must be ABOVE this, or you will chase the far wall and the crowd.
//        - Put a target (a box roughly opponent-sized) at 60 cm. Note the
//          reading. Your threshold must be BELOW this.
//      Pick something in between, closer to the empty-ring number.
//
//   C) THE BLIND ZONE. This is the one to actually watch. Slide a target in
//      from 80 cm toward the sensor face, slowly, watching one channel. The
//      reading climbs... and then somewhere around 10 cm it PEAKS and starts
//      FALLING again. Note the distance where it peaks and the value it
//      falls back to on contact. That falling number is what your robot sees
//      while it is actively pushing an opponent, which is why the attack
//      commit latch in Robot.h exists.
//
//   D) PER-SENSOR TRIM. Put a flat target at exactly 30 cm squarely in front
//      of ONE sensor at a time and note each reading. Whichever reads highest
//      is your reference. For each other sensor:
//          GAIN = 1000 * referenceReading / thisReading
//      Put those four numbers in Hardware.h. Without this, "right minus left"
//      has a permanent lean baked into it.
//
// THE EDGE SENSORS
//   The four columns on the right show the raw HIGH/LOW pin state. Hold the
//   robot over each surface in turn and write down what you see:
//     - over BLACK arena surface
//     - over the WHITE border frame
//     - over the BROWN centre lines  <-- do not skip this one
//   Set EDGE_WHITE_STATE_xx in Hardware.h to whatever state appears over
//   WHITE. Then check brown reads the SAME as black. If brown reads as white
//   on any corner, back that module's trim pot off until it does not, or you
//   will trigger a full edge recovery in the middle of the ring.
//
// THE BUTTONS
//   The last two columns show the switch states. With INPUT_PULLUP, an
//   unpressed button reads HIGH and a pressed one reads LOW. If a button
//   never changes, it is miswired.
// ============================================================================

const int OPP_FL = A0;
const int OPP_FR = A1;
const int OPP_L  = A2;
const int OPP_R  = A3;

const int EDGE_FL = 10;
const int EDGE_FR = 11;
const int EDGE_BL = 12;
const int EDGE_BR = 13;

const int BTN_START = A4;
const int BTN_ROUND = A5;

const int PRINT_INTERVAL_MS = 250;

int minVal[4];
int maxVal[4];
unsigned long lastPrint = 0;

void resetTrackers() {
  for (int i = 0; i < 4; i++) {
    minVal[i] = 32767;
    maxVal[i] = -1;
  }
  Serial.println(F("--- min/max reset ---"));
}

void setup() {
  Serial.begin(115200);
  unsigned long start = millis();
  while (!Serial && (millis() - start) < 3000) {
    ;
  }

#if !defined(ARDUINO_ARCH_AVR)
  analogReadResolution(12);
#endif

  pinMode(OPP_FL, INPUT);
  pinMode(OPP_FR, INPUT);
  pinMode(OPP_L,  INPUT);
  pinMode(OPP_R,  INPUT);

  pinMode(EDGE_FL, INPUT);
  pinMode(EDGE_FR, INPUT);
  pinMode(EDGE_BL, INPUT);
  pinMode(EDGE_BR, INPUT);

  pinMode(BTN_START, INPUT_PULLUP);
  pinMode(BTN_ROUND, INPUT_PULLUP);

  resetTrackers();
  Serial.println(F("SumoX-26 sensor calibration. Send any char to reset min/max."));
  Serial.println(F("FL/FR/L/R = now(min..max) | edges raw | buttons"));
}

void loop() {
  if (Serial.available()) {
    while (Serial.available()) Serial.read();
    resetTrackers();
  }

  int v[4];
  v[0] = analogRead(OPP_FL);
  v[1] = analogRead(OPP_FR);
  v[2] = analogRead(OPP_L);
  v[3] = analogRead(OPP_R);

  for (int i = 0; i < 4; i++) {
    if (v[i] < minVal[i]) minVal[i] = v[i];
    if (v[i] > maxVal[i]) maxVal[i] = v[i];
  }

  if (millis() - lastPrint < PRINT_INTERVAL_MS) {
    return;
  }
  lastPrint = millis();

  const char *names[4] = {"FL", "FR", "L", "R"};
  for (int i = 0; i < 4; i++) {
    Serial.print(names[i]);
    Serial.print('=');
    Serial.print(v[i]);
    Serial.print('(');
    Serial.print(minVal[i]);
    Serial.print("..");
    Serial.print(maxVal[i]);
    Serial.print(") ");
  }

  Serial.print(F("| EDGE FL="));
  Serial.print(digitalRead(EDGE_FL) == HIGH ? F("HIGH") : F("LOW "));
  Serial.print(F(" FR="));
  Serial.print(digitalRead(EDGE_FR) == HIGH ? F("HIGH") : F("LOW "));
  Serial.print(F(" BL="));
  Serial.print(digitalRead(EDGE_BL) == HIGH ? F("HIGH") : F("LOW "));
  Serial.print(F(" BR="));
  Serial.print(digitalRead(EDGE_BR) == HIGH ? F("HIGH") : F("LOW "));

  Serial.print(F(" | START="));
  Serial.print(digitalRead(BTN_START) == LOW ? F("PRESSED") : F("open   "));
  Serial.print(F(" ROUND="));
  Serial.println(digitalRead(BTN_ROUND) == LOW ? F("PRESSED") : F("open"));
}
