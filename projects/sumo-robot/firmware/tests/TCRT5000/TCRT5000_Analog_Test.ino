const int SENSOR_PIN = A0;

//const int WHITE_VALUE = 200;
//const int BLACK_VALUE = 800;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int rawAnalog = analogRead(SENSOR_PIN);

  Serial.print("Raw Sensor Value: ");
  Serial.println(rawAnalog);
  delay(150);
}