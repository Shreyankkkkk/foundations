// Standalone GP2Y0A21 x3 test — breadboard + Uno R3
// Wiring: sensor Vo -> voltage divider -> A0/A1/A2. GND common with Arduino.
// Open Serial Monitor at 9600 baud.

const int PIN_LEFT   = A0;
const int PIN_CENTER = A1;
const int PIN_RIGHT  = A2;

// Set this after you see the raw numbers below — start guessing from your
// TCRT5000-style test (near vs far object) and adjust until the L/C/R
// triplet matches reality for detect range.
int DETECT_THRESHOLD = 150;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int l = analogRead(PIN_LEFT);
  int c = analogRead(PIN_CENTER);
  int r = analogRead(PIN_RIGHT);

  bool dl = l > DETECT_THRESHOLD;
  bool dc = c > DETECT_THRESHOLD;
  bool dr = r > DETECT_THRESHOLD;

  Serial.print("raw  L:"); Serial.print(l);
  Serial.print("  C:");    Serial.print(c);
  Serial.print("  R:");    Serial.print(r);

  Serial.print("   triplet(L C R): ");
  Serial.print(dl); Serial.print(dc); Serial.println(dr);

  delay(150);
}
