/*
  TCRT5000 - SINGLE SENSOR Diagnostic Sketch
  --------------------------------------------
  Test one sensor at a time before wiring up all 4.

  WIRING (3-pin module: VCC, GND, OUT):
    VCC -> Arduino 5V
    GND -> Arduino GND
    OUT -> Arduino A0   (A0 can do both analogRead AND digitalRead,
                          so this one sketch tells us everything)

  WHAT THIS TEST TELLS YOU:
    Watch the "RAW" column as you move a surface toward/away from the sensor.

    - If RAW moves smoothly through a wide range of numbers (e.g. 40, 180,
      420, 900...) as you change distance or color -> you have TRUE analog
      output. Great, per-sensor threshold calibration (as planned) will work.

    - If RAW only ever jumps between ~0 and ~1023 with NOTHING in between,
      no matter the distance or color -> your module's OUT pin is already
      passed through an onboard comparator (a small blue trimmer pot on the
      board is the tell). It is a digital signal already, being read with
      analogRead just fine, but there's no raw reflectivity data available
      at this pin. In that case, tell me and we'll switch strategy (tune the
      onboard pot precisely, or tap the phototransistor leg directly).

  HOW TO USE:
    1. Open Serial Monitor, 9600 baud.
    2. Hold a WHITE surface at various distances (touching, 3mm, 5mm, 10mm, 20mm)
       and note the RAW value + DIGITAL column at each distance.
    3. Repeat with BLACK, then BROWN.
    4. Write down the numbers -- we'll use them for the threshold in the next step.
*/

const uint8_t SENSOR_PIN = A0;

const unsigned long SAMPLE_INTERVAL_MS = 150;
unsigned long lastSampleTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(SENSOR_PIN, INPUT);

  Serial.println(F("TCRT5000 single-sensor diagnostic started."));
  Serial.println(F("Move a test surface slowly toward/away from the sensor."));
  Serial.println();
  Serial.println(F("millis,RAW_analog(0-1023),DIGITAL(threshold@512),volts"));
}

void loop() {
  unsigned long now = millis();
  if (now - lastSampleTime < SAMPLE_INTERVAL_MS) return;
  lastSampleTime = now;

  int raw = analogRead(SENSOR_PIN);
  int digitalEquivalent = (raw > 512) ? HIGH : LOW; // just for reference, not a real threshold yet
  float volts = raw * (5.0 / 1023.0);

  Serial.print(now);
  Serial.print(',');
  Serial.print(raw);
  Serial.print(',');
  Serial.print(digitalEquivalent == HIGH ? "HIGH" : "LOW");
  Serial.print(',');
  Serial.print(volts, 2);
  Serial.println('V');
}
