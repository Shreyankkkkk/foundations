// Copy Hardware.h, Motors.h, Motors.cpp, Map.h, Map.cpp, Sensors.h, Sensors.cpp into this folder first.
// Robot on a stand (wheels off the ground). Opponent sensor aimed at a FIXED target.
// Run 1: RUN_MOTORS=false. Run 2: RUN_MOTORS=true. Compare sigma/pp: the difference is the UBEC/motor-load noise.
// Put the larger sigma into ADC_NOISE_SIGMA in Hardware.h. us/read must satisfy 3*(ADC_OVERSAMPLE_N+1)*us < SENSOR_SAMPLE_INTERVAL_MS*1000.
#include "Hardware.h"
#include "Motors.h"

const bool RUN_MOTORS = true;

void setup()
{
    Serial.begin(115200);
    analogReadResolution(SENSOR_ADC_BITS);
    if (RUN_MOTORS)
    {
        initMotors();
        drive(255, 255, true);
    }
}

void loop()
{
    const int pins[3] = {OPPONENT_LEFT, OPPONENT_CENTER, OPPONENT_RIGHT};
    const int N = 500;
    for (int c = 0; c < 3; c++)
    {
        (void)analogRead(pins[c]);
        double s = 0, s2 = 0;
        int lo = 100000, hi = -1;
        unsigned long t = micros();
        for (int i = 0; i < N; i++)
        {
            int v = analogRead(pins[c]);
            s += v;
            s2 += (double)v * v;
            if (v < lo) lo = v;
            if (v > hi) hi = v;
        }
        unsigned long us = micros() - t;
        double m = s / N;
        Serial.print("ch"); Serial.print(c);
        Serial.print(" mean="); Serial.print(m, 1);
        Serial.print(" sigma="); Serial.print(sqrt(s2 / N - m * m), 2);
        Serial.print(" pp="); Serial.print(hi - lo);
        Serial.print(" us/read="); Serial.println((float)us / N, 1);
    }
    Serial.println();
    delay(1000);
}
