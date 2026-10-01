// T4: top speed. Robot ON THE ARENA FLOOR, clear 2 m of runway. Serial Monitor at 115200.
// Run 1 drives 2 s, Run 2 drives 3 s, both at full power. Reset the robot to the same start mark between runs.
// Measure the distance from the start mark to the front of the robot each time (D2, D3 in cm).
// DRIVE_SPEED_MAX_CMS = D3 - D2   (the extra 1 s of driving cancels out acceleration and braking)

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

void run(const char *label, unsigned long ms)
{
    Serial.println(label);
    drive(255, 255);
    delay(ms);
    drive(0, 0);
}

void setup()
{
    Serial.begin(115200);
    analogWriteResolution(8);
    int en[4] = {LEFT_L_EN, LEFT_R_EN, RIGHT_L_EN, RIGHT_R_EN};
    for (int i = 0; i < 4; i++) { pinMode(en[i], OUTPUT); digitalWrite(en[i], HIGH); }
    drive(0, 0);

    Serial.println("Place robot on start mark. Run 1 (2 s) in 8 s...");
    delay(8000);
    run("RUN 1: 2 s -> measure D2", 2000);

    Serial.println("Reset robot to start mark. Run 2 (3 s) in 15 s...");
    delay(15000);
    run("RUN 2: 3 s -> measure D3", 3000);
    Serial.println("done: speed = D3 - D2 (cm/s)");
}

void loop() {}
