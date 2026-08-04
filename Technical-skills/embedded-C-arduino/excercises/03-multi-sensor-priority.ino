/*
  Exercise 03 - Multi-Sensor Priority Logic
  Goal: Understand else-if chains with multiple inputs, and WHY order matters.

  This is a stand-in for the real sumo robot's decision logic:
  - Button on pin 2  = stand-in for "opponent detected" sensor
  - Button on pin 3   = stand-in for "edge detected" sensor

  Hardware: Arduino Uno + 2 pushbuttons (same wiring pattern as Exercise 02 -
  one leg from EACH contact, not both legs of the same contact)

  Why edge-check is checked FIRST:
  if/else-if chains are checked top to bottom, and the FIRST true condition
  wins - the rest are skipped, even if they'd also be true. If "opponent
  detected" were checked before "edge detected", the robot could attack its
  way straight over the edge whenever both were true at once. Putting the
  safety check (edge) first guarantees it always overrides everything else,
  every single loop cycle, no matter what else is happening.

  This structure is IDENTICAL to the real Besomi kit's loop() - just with
  buttons standing in for the actual IR/line sensors.
*/

void setup() {
  pinMode(13, OUTPUT);
  pinMode(2, INPUT_PULLUP);  // pretend: opponent detected sensor
  pinMode(3, INPUT_PULLUP);  // pretend: edge detected sensor
  Serial.begin(9600);
}

void loop() {
  int opponentDetected = digitalRead(2);
  int edgeDetected = digitalRead(3);

  if (edgeDetected == LOW) {
    // Safety check - always checked FIRST, always wins
    Serial.println("ACTION: EDGE ESCAPE");
    digitalWrite(13, LOW);
  }
  else if (opponentDetected == LOW) {
    Serial.println("ACTION: ATTACK");
    digitalWrite(13, HIGH);
  }
  else {
    Serial.println("ACTION: SEARCH");
    digitalWrite(13, LOW);
  }
}
