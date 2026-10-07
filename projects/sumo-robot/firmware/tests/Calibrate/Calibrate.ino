// CALIBRATE: one sketch for every sensor reading you need. Serial Monitor at 115200 baud.
// Setup: make a folder named "Calibrate" containing THIS file plus Hardware.h, Formulas.h, Motors.h, Motors.cpp (copy from SumoX26).
// Run 1: RUN_MOTORS=false. Run 2: RUN_MOTORS=true, robot on a stand, wheels off the ground. Same targets both times.
const bool RUN_MOTORS = false;

#include "Hardware.h"
#include "Motors.h"

void setup()
{
    Serial.begin(115200);
    analogReadResolution(SENSOR_ADC_BITS);
    pinMode(EDGE_FRONT, INPUT);
    pinMode(EDGE_BACK, INPUT);
    pinMode(START_BUTTON_PIN, INPUT);
    if (RUN_MOTORS)
    {
        initMotors();
        drive(255, 255, true);
    }
}

static void report(const char *name, int pin)
{
    const int N = 300;
    (void)analogRead(pin);
    double s = 0, s2 = 0;
    int lo = 100000, hi = -1;
    unsigned long t = micros();
    for (int i = 0; i < N; i++)
    {
        int v = analogRead(pin);
        s += v;
        s2 += (double)v * v;
        if (v < lo) lo = v;
        if (v > hi) hi = v;
    }
    unsigned long us = micros() - t;
    double m = s / N;
    Serial.print(name);
    Serial.print(" mean="); Serial.print(m, 0);
    Serial.print(" sigma="); Serial.print(sqrt(s2 / N - m * m), 1);
    Serial.print(" min="); Serial.print(lo);
    Serial.print(" max="); Serial.print(hi);
    Serial.print(" us/read="); Serial.println((float)us / N, 1);
}

void loop()
{
    report("LEFT   A0", OPPONENT_LEFT);
    report("CENTER A1", OPPONENT_CENTER);
    report("RIGHT  A2", OPPONENT_RIGHT);
    report("ROCKER A4", START_BUTTON_PIN);
    Serial.print("EDGE front D10="); Serial.print(digitalRead(EDGE_FRONT));
    Serial.print("  back D11="); Serial.println(digitalRead(EDGE_BACK));
    Serial.println();
    delay(1000);
}
