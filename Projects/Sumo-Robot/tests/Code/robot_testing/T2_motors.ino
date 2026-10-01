// T2: wheel check. WHEELS LIFTED. Runs once after a 5 s wait. Serial Monitor at 115200.
// Watch each step and write down which PHYSICAL wheel moves and which way.
// Pass = "LEFT" steps move the robot's physical LEFT wheel, forward when told forward.

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

void step(const char *label, int l, int r)
{
    Serial.println(label);
    drive(l, r);
    delay(1500);
    drive(0, 0);
    delay(1000);
}

void setup()
{
    Serial.begin(115200);
    analogWriteResolution(8);
    int en[4] = {LEFT_L_EN, LEFT_R_EN, RIGHT_L_EN, RIGHT_R_EN};
    for (int i = 0; i < 4; i++) { pinMode(en[i], OUTPUT); digitalWrite(en[i], HIGH); }
    drive(0, 0);
    delay(5000);

    step("1) LEFT wheel FORWARD", 150, 0);
    step("2) LEFT wheel BACKWARD", -150, 0);
    step("3) RIGHT wheel FORWARD", 0, 150);
    step("4) RIGHT wheel BACKWARD", 0, -150);
    step("5) BOTH FORWARD", 150, 150);
    step("6) BOTH BACKWARD", -150, -150);
    Serial.println("done");
}

void loop() {}
