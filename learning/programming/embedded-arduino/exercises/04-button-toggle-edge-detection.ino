/*
  Exercise 04 - Button Toggle LED (Edge Detection)

  Purpose:
  - Pressing the button toggles the LED ON/OFF.
  - The LED keeps its state after the button is released
    (unlike Exercise 02, where the LED only stayed on while HELD).

  Hardware:
  - Built-in LED on Arduino UNO -> Pin 13
  - Push button -> Pin 2 and GND

  INPUT_PULLUP logic:
  - Button released -> HIGH
  - Button pressed  -> LOW

  This works because the Arduino internally pulls the pin HIGH.
  When the button is pressed, it connects the pin to GND, causing LOW.

  This is a step up from Exercise 02: instead of just checking the
  CURRENT button state every loop, this compares the current reading
  to the PREVIOUS reading to detect the exact moment the button goes
  from released to pressed (a "falling edge": HIGH -> LOW). See notes
  file for why this matters.
*/

// Stores the current LED state
// false = OFF
// true  = ON
bool ledState = false;

// Stores the previous button reading
// Used to detect when the button changes from HIGH -> LOW
bool previousButtonState = HIGH;

// Pin definitions
const int LED = 13;
const int BUTTON = 2;

void setup() {
  // Configure LED pin as an output
  pinMode(LED, OUTPUT);

  // Configure button pin as an input using internal pull-up resistor
  pinMode(BUTTON, INPUT_PULLUP);

  // Start serial communication for debugging
  Serial.begin(9600);
}

void loop() {

  // Read the current state of the button
  // Returns:
  // HIGH -> button released
  // LOW  -> button pressed
  bool buttonState = digitalRead(BUTTON);

  /*
    Detect a button press.

    We are looking for the transition:

    HIGH -> LOW

    Meaning:
    Previous loop: button was released
    Current loop: button is now pressed

    This prevents the LED from toggling repeatedly
    while the button is being held down.
  */
  if (previousButtonState == HIGH && buttonState == LOW) {

    // Toggle LED state:
    // false becomes true
    // true becomes false
    ledState = !ledState;

    // Apply the new LED state
    digitalWrite(LED, ledState);

    Serial.println("Button Pressed");
  }

  // Save current button state for the next loop
  previousButtonState = buttonState;

  // Small delay to prevent accidental multiple readings
  delay(50);
}
