// T1: sensor readings. Serial Monitor at 115200.
// Prints raw ADC for the 3 opponent sensors, min/max since boot, and the 2 edge pins (0/1).
// Set SPIN_MOTORS to true ONLY with wheels LIFTED, to log noise with motors at full power.

const bool SPIN_MOTORS = false;

const int OPP[3] = {A0, A1, A2}; // left, center, right
const int EDGE_FRONT = 10, EDGE_BACK = 11;

const int LEFT_L_EN = 2, LEFT_R_PWM = 3, LEFT_R_EN = 4, LEFT_L_PWM = 5;
const int RIGHT_L_PWM = 6, RIGHT_R_EN = 7, RIGHT_L_EN = 8, RIGHT_R_PWM = 9;

int mn[3] = {9999, 9999, 9999}, mx[3] = {0, 0, 0};

void setup()
{
    Serial.begin(115200);
    delay(1500);
    analogReadResolution(10);
    for (int i = 0; i < 3; i++) pinMode(OPP[i], INPUT);
    pinMode(EDGE_FRONT, INPUT);
    pinMode(EDGE_BACK, INPUT);

    if (SPIN_MOTORS)
    {
        analogWriteResolution(8);
        int en[4] = {LEFT_L_EN, LEFT_R_EN, RIGHT_L_EN, RIGHT_R_EN};
        for (int i = 0; i < 4; i++) { pinMode(en[i], OUTPUT); digitalWrite(en[i], HIGH); }
        analogWrite(LEFT_R_PWM, 255);  // left forward
        analogWrite(RIGHT_L_PWM, 255); // right forward (inverted side)
    }
}

void loop()
{
    int v[3];
    for (int i = 0; i < 3; i++)
    {
        v[i] = analogRead(OPP[i]);
        if (v[i] < mn[i]) mn[i] = v[i];
        if (v[i] > mx[i]) mx[i] = v[i];
    }
    Serial.print("L="); Serial.print(v[0]);
    Serial.print(" C="); Serial.print(v[1]);
    Serial.print(" R="); Serial.print(v[2]);
    Serial.print(" | min/max L "); Serial.print(mn[0]); Serial.print("/"); Serial.print(mx[0]);
    Serial.print(" C "); Serial.print(mn[1]); Serial.print("/"); Serial.print(mx[1]);
    Serial.print(" R "); Serial.print(mn[2]); Serial.print("/"); Serial.print(mx[2]);
    Serial.print(" | edge F="); Serial.print(digitalRead(EDGE_FRONT));
    Serial.print(" B="); Serial.println(digitalRead(EDGE_BACK));
    delay(200);
}
