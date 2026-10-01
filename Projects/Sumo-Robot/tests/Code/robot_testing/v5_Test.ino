// Copy Hardware.h, Motors.h/.cpp, Sensors.h/.cpp into this sketch's folder too
// testing raw hardware behavior
// Serial Monitor at 115200 baud

#include "Hardware.h"
#include "Motors.h"
#include "Sensors.h"

const int BOOT_MARKER_PIN = 12; // free pin, unused in match build — wire an LED here for t0 slow-mo video
const int TEST_PWM = 200;
const unsigned long DRIVE_TEST_MS = 2000;
const unsigned long STOP_TEST_MS = 2000;
const unsigned long STREAM_INTERVAL_MS = 100;

void setup()
{
    pinMode(BOOT_MARKER_PIN, OUTPUT);
    digitalWrite(BOOT_MARKER_PIN, HIGH); // fires the instant code starts — film this + the power LED together for t0

    Serial.begin(115200);
    initMotors();
    initSensors();

    Serial.println(F("v5_test ready. Commands:"));
    Serial.println(F("  f/b = drive fwd/back 2s @ test PWM (measure distance -> DRIVE_SPEED_MAX_CMS)"));
    Serial.println(F("  l/r = spin left/right, any key stops (time it -> deg/s = 360/seconds for one full turn)"));
    Serial.println(F("  w   = 300ms 'toward left' pulse -> confirm which way it turned (G0 polarity check)"));
    Serial.println(F("  e   = stop-distance test: 2s full speed then cut power (measure slide -> STOP_DISTANCE_CM)"));
    Serial.println(F("  o   = stream raw opponent sensor values (L,C,R) -> noise log / R_det / distance table"));
    Serial.println(F("  g   = stream raw edge sensor states (front,back) -> polarity + height-band checks"));
    Serial.println(F("  a   = ADC saturation check (put finger on center sensor, ~0cm) -> should read near 1023"));
    Serial.println(F("  x   = stop everything"));
}

static void driveTimed(int left, int right, unsigned long ms)
{
    drive(left, right);
    unsigned long start = millis();
    while (millis() - start < ms)
    {
        if (Serial.available())
        {
            Serial.read();
            break;
        } // abort early on any keypress
    }
    stopMotors();
}

static void spinUntilKey(bool towardLeft)
{
    Serial.println(F("Spinning... press any key the instant it completes exactly one full turn."));
    unsigned long start = millis();
    int mag = TEST_PWM;
    if (towardLeft)
        drive(+mag, -mag);
    else
        drive(-mag, +mag);
    while (!Serial.available())
    { /* wait */
    }
    Serial.read();
    stopMotors();
    unsigned long elapsed = millis() - start;
    Serial.print(F("Elapsed ms for that rotation: "));
    Serial.println(elapsed);
    Serial.println(F("deg/s = 360000 / elapsed_ms"));
}

static void streamOpponent()
{
    Serial.println(F("Streaming L,C,R raw ADC. Press any key to stop."));
    while (!Serial.available())
    {
        updateOpponentSensors();
        OpponentReadings r = getOpponentReadings();
        Serial.print(r.left);
        Serial.print(',');
        Serial.print(r.center);
        Serial.print(',');
        Serial.println(r.right);
        delay(STREAM_INTERVAL_MS);
    }
    Serial.read();
}

static void streamEdge()
{
    Serial.println(F("Streaming front,back edge state. Press any key to stop."));
    while (!Serial.available())
    {
        EdgeReadings e = readEdgeSensors();
        Serial.print(e.front);
        Serial.print(',');
        Serial.println(e.back);
        delay(STREAM_INTERVAL_MS);
    }
    Serial.read();
}

void loop()
{
    if (!Serial.available())
        return;
    char cmd = Serial.read();

    switch (cmd)
    {
    case 'f':
        Serial.println(F("Driving forward 2s. Mark start/end position, measure distance."));
        driveTimed(TEST_PWM, TEST_PWM, DRIVE_TEST_MS);
        Serial.println(F("Done. cm/s = distance_cm / 2.0"));
        break;
    case 'b':
        Serial.println(F("Driving backward 2s. Mark start/end position, measure distance."));
        driveTimed(-TEST_PWM, -TEST_PWM, DRIVE_TEST_MS);
        Serial.println(F("Done. cm/s = distance_cm / 2.0"));
        break;
    case 'l':
        spinUntilKey(true);
        break;
    case 'r':
        spinUntilKey(false);
        break;
    case 'w':
        Serial.println(F("Pulsing 'toward left' for 300ms. Watch which way it turns."));
        driveTimed(+TEST_PWM, -TEST_PWM, 300);
        Serial.println(F("If it turned toward the LEFT sensor's side: polarity is correct as-is."));
        Serial.println(F("If it turned right instead: flip the sign in spinCommand() in Strategy.cpp."));
        break;
    case 'e':
        Serial.println(F("Full speed 2s, then power cut. Measure slide distance from cutoff point to rest."));
        drive(255, 255);
        delay(STOP_TEST_MS);
        stopMotors();
        Serial.println(F("Power cut now. Measure the slide."));
        break;
    case 'o':
        streamOpponent();
        break;
    case 'g':
        streamEdge();
        break;
    case 'a':
    {
        updateOpponentSensors();
        OpponentReadings r = getOpponentReadings();
        Serial.print(F("Center raw: "));
        Serial.println(r.center);
        Serial.println(F("Should approach ~1023 with an object nearly touching the sensor, not ~4095."));
        break;
    }
    case 'x':
    default:
        stopMotors();
        break;
    }
}