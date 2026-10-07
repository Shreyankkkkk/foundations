// T5: edge response. Robot ON THE ARENA with a white line (tape or the real border) ahead. Serial Monitor at 115200.
// Robot drives at the line, polling the edge sensor every 5 ms (same as the real loop), then reacts.
// Measure how far the NOSE ends up past the white line's start, and film it in slow-mo to see the max overshoot.
// Change the three settings below between runs. Start 80+ cm from the line.

const int RUN_PWM = 255;             // try 255, then 170
const bool TEST_BACK = false;        // false: drive forward at the FRONT sensor, true: reverse at the BACK sensor
const bool REVERSE_ON_HIT = false;   // false: just stop (brake). true: reverse 150 ms at 170 then stop (like edge recovery)

const int EDGE_FRONT = 10, EDGE_BACK = 11;
const int EDGE_WHITE_STATE = HIGH;

const int LEFT_L_EN = 2, LEFT_R_PWM = 3, LEFT_R_EN = 4, LEFT_L_PWM = 5;
const int RIGHT_L_PWM = 6, RIGHT_R_EN = 7, RIGHT_L_EN = 8, RIGHT_R_PWM = 9;
const bool LEFT_MOTOR_INVERTED = false;
const bool RIGHT_MOTOR_INVERTED = true;

static void setSide(int rPwmPin, int lPwmPin, int s)
{
    if (s >= 0) { analogWrite(lPwmPin, 0); analogWrite(rPwmPin, s); }
    else        { analogWrite(rPwmPin, 0); analogWrite(lPwmPin, -s); }
}

void drive(int l, int r)
{
    l = constrain(l, -255, 255);
    r = constrain(r, -255, 255);
    if (LEFT_MOTOR_INVERTED) l = -l;
    if (RIGHT_MOTOR_INVERTED) r = -r;
    setSide(LEFT_R_PWM, LEFT_L_PWM, l);
    setSide(RIGHT_R_PWM, RIGHT_L_PWM, r);
}

void setup()
{
    Serial.begin(115200);
    analogWriteResolution(8);
    int en[4] = {LEFT_L_EN, LEFT_R_EN, RIGHT_L_EN, RIGHT_R_EN};
    for (int i = 0; i < 4; i++) { pinMode(en[i], OUTPUT); digitalWrite(en[i], HIGH); }
    pinMode(EDGE_FRONT, INPUT);
    pinMode(EDGE_BACK, INPUT);
    drive(0, 0);
    Serial.println("Starting in 8 s...");
    delay(8000);

    int dir = TEST_BACK ? -1 : 1;
    int sensor = TEST_BACK ? EDGE_BACK : EDGE_FRONT;
    drive(dir * RUN_PWM, dir * RUN_PWM);

    unsigned long t0 = millis(), last = 0;
    bool hit = false;
    while (millis() - t0 < 6000)
    {
        if (millis() - last < 5) continue; // 5 ms tick like the real loop
        last = millis();
        if (digitalRead(sensor) == EDGE_WHITE_STATE) { hit = true; break; }
    }

    if (!hit) { drive(0, 0); Serial.println("NO EDGE SEEN (6 s timeout)"); return; }

    if (REVERSE_ON_HIT) { drive(-dir * 170, -dir * 170); delay(150); }
    drive(0, 0);
    Serial.print("EDGE HIT at ms: "); Serial.println(millis() - t0);
    Serial.println("Measure nose overshoot past the line (cm) -> STOP_DISTANCE_CM (stop mode)");
}

void loop() {}
