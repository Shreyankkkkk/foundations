// T3: spin rate + spin direction. Robot ON THE ARENA FLOOR (not lifted). Serial Monitor at 115200.
// Mark a tape line on the floor under the robot's nose and count full turns.
// Phase A uses the code's convention for spinCommand(towardLeft=true): left +, right -.
//   Write down the PHYSICAL direction seen from above (clockwise or counter-clockwise).
//   The strategy code and map expect towardLeft=true = COUNTER-CLOCKWISE.
// Rate (deg/s) = turns * 360 / 5.  Fill in SPIN_RATE_CCW_DEGS and SPIN_RATE_CW_DEGS.

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
    drive(0, 0);
    delay(5000);

    Serial.println("A) towardLeft=true (left +, right -) for 5 s: count turns + note direction");
    drive(255, -255);
    delay(5000);
    drive(0, 0);
    delay(4000);

    Serial.println("B) towardLeft=false (left -, right +) for 5 s: count turns + note direction");
    drive(-255, 255);
    delay(5000);
    drive(0, 0);
    Serial.println("done");
}

void loop() {}
