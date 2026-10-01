// T0: boot time. Start a stopwatch the instant you switch the robot ON.
// Stop it when the LED turns on. That time = switch-on -> first line of setup().
// Write it down: it becomes BOOT_DELAY_ESTIMATE_MS (in ms).

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.begin(115200);
}

void loop()
{
    Serial.println(millis());
    delay(500);
}
