// ============================================================================
// SumoX-26 — MotorBench.ino
// ----------------------------------------------------------------------------
// STANDALONE bench sketch. Copy this folder somewhere separate and open it
// on its own. It does not use any of the SumoX-26 files.
//
// *** WHEELS OFF THE GROUND. Chassis clamped or held. Every time. ***
//
// WHAT IT IS FOR — two things you cannot answer from a datasheet:
//
//   1. IS PWM REAL ON THESE PINS?
//      Your motor PWM pins are D3, D5, D6, D9. On an UNO R3 all four are PWM
//      outputs. The UNO Q uses the same header shape but a completely
//      different microcontroller underneath, so this has to be verified, not
//      assumed. The ramp test below sweeps each side 0 -> 255 -> 0 over a few
//      seconds. Watch the wheel:
//        - speed changes smoothly  => PWM works on that pin. Good.
//        - wheel is either stopped or full speed, nothing in between
//          => that pin is NOT a PWM output. Move it to one that is and
//             update Hardware.h. The speed constants are meaningless until
//             this passes.
//
//   2. WHICH WAY IS FORWARD?
//      The polarity test drives each side at a gentle speed in the direction
//      the code calls "forward". Watch which way each wheel actually turns.
//      For any side that spins BACKWARDS relative to the robot, set its
//      LEFT_MOTOR_INVERTED / RIGHT_MOTOR_INVERTED flag to true in Hardware.h.
//      Do not rewire and do not edit Motors.cpp — that is what the flags
//      are for.
//
// HOW TO USE IT
//   Upload, open Serial Monitor at 115200, and follow the prompts. Send any
//   character to advance to the next test. Motors stop between tests.
// ============================================================================

const int LEFT_L_EN   = 2;
const int LEFT_R_PWM  = 3;
const int LEFT_R_EN   = 4;
const int LEFT_L_PWM  = 5;

const int RIGHT_L_PWM = 6;
const int RIGHT_R_EN  = 7;
const int RIGHT_L_EN  = 8;
const int RIGHT_R_PWM = 9;

// Gentle. Do not raise this for a bench test.
const int POLARITY_SPEED = 80;

void allOff() {
  analogWrite(LEFT_R_PWM, 0);
  analogWrite(LEFT_L_PWM, 0);
  analogWrite(RIGHT_R_PWM, 0);
  analogWrite(RIGHT_L_PWM, 0);
}

// speed: -255..255. Positive is what the main code calls forward.
void driveLeft(int speed) {
  if (speed >= 0) { analogWrite(LEFT_L_PWM, 0); analogWrite(LEFT_R_PWM, speed); }
  else            { analogWrite(LEFT_R_PWM, 0); analogWrite(LEFT_L_PWM, -speed); }
}

void driveRight(int speed) {
  if (speed >= 0) { analogWrite(RIGHT_L_PWM, 0); analogWrite(RIGHT_R_PWM, speed); }
  else            { analogWrite(RIGHT_R_PWM, 0); analogWrite(RIGHT_L_PWM, -speed); }
}

void waitForKey(const __FlashStringHelper *prompt) {
  allOff();
  Serial.println();
  Serial.println(prompt);
  Serial.println(F("   (send any character to continue)"));
  while (Serial.available()) Serial.read();
  while (!Serial.available()) {
    ;
  }
  while (Serial.available()) Serial.read();
}

void rampSide(bool leftSide) {
  Serial.println(F("   ramping up..."));
  for (int s = 0; s <= 255; s += 5) {
    if (leftSide) driveLeft(s); else driveRight(s);
    delay(25);
  }
  Serial.println(F("   ramping down..."));
  for (int s = 255; s >= 0; s -= 5) {
    if (leftSide) driveLeft(s); else driveRight(s);
    delay(25);
  }
  allOff();
}

void setup() {
  Serial.begin(115200);
  unsigned long start = millis();
  while (!Serial && (millis() - start) < 3000) {
    ;
  }

  pinMode(LEFT_L_EN,  OUTPUT);
  pinMode(LEFT_R_EN,  OUTPUT);
  pinMode(LEFT_R_PWM, OUTPUT);
  pinMode(LEFT_L_PWM, OUTPUT);

  pinMode(RIGHT_L_EN,  OUTPUT);
  pinMode(RIGHT_R_EN,  OUTPUT);
  pinMode(RIGHT_R_PWM, OUTPUT);
  pinMode(RIGHT_L_PWM, OUTPUT);

  // Zero the PWM pins BEFORE arming the drivers, so there is never a moment
  // where the bridges are enabled with the inputs in an unknown state.
  allOff();
  digitalWrite(LEFT_L_EN,  HIGH);
  digitalWrite(LEFT_R_EN,  HIGH);
  digitalWrite(RIGHT_L_EN, HIGH);
  digitalWrite(RIGHT_R_EN, HIGH);

  Serial.println(F("=== SumoX-26 motor bench ==="));
  Serial.println(F("WHEELS OFF THE GROUND."));
}

void loop() {
  waitForKey(F("TEST 1/4 - LEFT side PWM ramp. Watch for SMOOTH speed change."));
  rampSide(true);

  waitForKey(F("TEST 2/4 - RIGHT side PWM ramp. Watch for SMOOTH speed change."));
  rampSide(false);

  waitForKey(F("TEST 3/4 - LEFT side polarity. Should turn the robot FORWARD."));
  driveLeft(POLARITY_SPEED);
  delay(2500);
  allOff();
  Serial.println(F("   Wrong way? Set LEFT_MOTOR_INVERTED = true in Hardware.h"));

  waitForKey(F("TEST 4/4 - RIGHT side polarity. Should turn the robot FORWARD."));
  driveRight(POLARITY_SPEED);
  delay(2500);
  allOff();
  Serial.println(F("   Wrong way? Set RIGHT_MOTOR_INVERTED = true in Hardware.h"));

  waitForKey(F("Done. Continue to loop back to TEST 1."));
}
