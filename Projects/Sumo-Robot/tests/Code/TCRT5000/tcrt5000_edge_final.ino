/*
  TCRT5000 Edge Sensor - Final Logic
  -----------------------------------
  Behavior required:
    WHITE (border)     -> logical HIGH -> trigger edge-recovery
    BLACK (arena)       -> logical LOW
    BROWN (start line)  -> logical LOW

  Uses raw analog readings (not the onboard digital/comparator output),
  with a threshold calibrated PER SENSOR from tcrt5000_calibration_test.ino,
  because unit-to-unit gain variance makes a single shared threshold unreliable.

  *** REPLACE THE THRESHOLD VALUES BELOW WITH YOUR MEASURED NUMBERS ***
  For each sensor: threshold = midpoint between its WHITE reading and its
  highest BLACK/BROWN reading, e.g. if white=850 and black/brown max=300,
  threshold = (850 + 300) / 2 = 575.
*/

const uint8_t SENSOR_PINS[4] = {A0, A1, A2, A3};
const char* SENSOR_NAMES[4]  = {"S1_FL", "S2_FR", "S3_BL", "S4_BR"};

// TODO: replace with your measured per-sensor thresholds from calibration
int sensorThreshold[4] = {575, 575, 575, 575};

// Optional: simple debounce so a single noisy reading doesn't trigger recovery
const uint8_t DEBOUNCE_SAMPLES = 3;
uint8_t highCount[4] = {0, 0, 0, 0};

bool edgeState[4] = {false, false, false, false}; // true = HIGH = white/border detected

void setup() {
  Serial.begin(9600);
  for (uint8_t i = 0; i < 4; i++) {
    pinMode(SENSOR_PINS[i], INPUT);
  }
  Serial.println(F("TCRT5000 edge sensor - final logic running."));
}

// Reads one sensor and returns true if it currently reads HIGH (white/border)
bool readEdgeHigh(uint8_t index) {
  int raw = analogRead(SENSOR_PINS[index]);
  return raw > sensorThreshold[index];
}

void loop() {
  bool anyEdgeTriggered = false;

  for (uint8_t i = 0; i < 4; i++) {
    bool instantHigh = readEdgeHigh(i);

    // Debounce: require several consecutive HIGH samples before trusting it
    if (instantHigh) {
      if (highCount[i] < DEBOUNCE_SAMPLES) highCount[i]++;
    } else {
      highCount[i] = 0;
    }

    bool debouncedHigh = (highCount[i] >= DEBOUNCE_SAMPLES);

    if (debouncedHigh && !edgeState[i]) {
      // Rising edge: sensor just went HIGH
      edgeState[i] = true;
      Serial.print(SENSOR_NAMES[i]);
      Serial.println(F(" -> HIGH (border detected)"));
    } else if (!debouncedHigh && edgeState[i]) {
      edgeState[i] = false;
      Serial.print(SENSOR_NAMES[i]);
      Serial.println(F(" -> LOW"));
    }

    if (edgeState[i]) anyEdgeTriggered = true;
  }

  if (anyEdgeTriggered) {
    triggerEdgeRecovery();
  }

  delay(20); // ~50 Hz sensor loop; adjust to match your main control loop rate
}

void triggerEdgeRecovery() {
  // Hook your recovery logic here:
  //   - which sensor(s) are HIGH tells you which side went over the border
  //   - reverse + turn away from that side, then resume search/attack mode
  //
  // Example skeleton:
  // if (edgeState[0] || edgeState[1]) { reverseAndTurn(RIGHT); }
  // if (edgeState[2] || edgeState[3]) { reverseAndTurn(LEFT);  }
}
