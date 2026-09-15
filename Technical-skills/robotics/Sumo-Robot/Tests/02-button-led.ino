/*
  Exercise 02 - Button Controls LED
  Goal: Understand INPUT_PULLUP, digitalRead(), variables, if/else, Serial

  Hardware: Arduino Uno + 1 pushbutton (Wokwi wokwi-pushbutton part)

  Wiring (this took two tries to get right):
  - WRONG (first attempt): connected 1.l -> pin 2, 1.r -> GND.
    This didn't work because 1.l and 1.r are the SAME contact — they're
    always connected to each other whether the button is pressed or not.
    Wiring both legs of one contact just makes a permanent short.
  - CORRECT: connected 1.r -> pin 2, 2.l -> GND (one leg from EACH of the
    two different contacts). Now the button pressing is what completes
    the circuit between them.

  Behavior note: this is a MOMENTARY button, not a toggle switch. The LED
  is only ON while the button is physically held down, and turns OFF the
  instant it's released. That's correct expected behavior, not a bug.

  What I learned:
  - pinMode(pin, INPUT_PULLUP) means the pin defaults to reading HIGH,
    so a pressed button reads LOW (this feels backwards until you know why)
  - digitalRead(pin) returns the current state and can be stored in a variable
  - int buttonState = digitalRead(2);  <- variables need a declared type
  - == compares (is this equal to?), = assigns (set this to)
  - Serial.begin() + Serial.println() let me see what the code is doing
    in real time on the computer screen, not just on the board
*/

void setup() {
  pinMode(13, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int buttonState = digitalRead(2);

  if (buttonState == LOW) {
    digitalWrite(13, HIGH);
    Serial.println("Button pressed - LED ON");
  } else {
    digitalWrite(13, LOW);
    Serial.println("Button not pressed - LED OFF");
  }
}
