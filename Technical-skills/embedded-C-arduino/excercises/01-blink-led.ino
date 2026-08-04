/*
  Exercise 01 - Blink LED
  Goal: Understand setup()/loop(), pinMode(), digitalWrite(), delay()

  Hardware: Arduino Uno on Wokwi (built-in LED on pin 13, no wiring needed)

  What I learned:
  - setup() runs once, loop() runs forever automatically
  - pinMode() must be called before using a pin
  - digitalWrite(pin, HIGH/LOW) turns a pin on/off
  - delay(ms) pauses everything for that many milliseconds
  - Changing both delay values together speeds up / slows down the blink evenly.
    Changing them to different values (e.g. delay(100) then delay(200)) makes
    the on-time and off-time uneven — I could visualize this as a graph in my
    head before running it, and the board matched what I predicted.
*/

void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
