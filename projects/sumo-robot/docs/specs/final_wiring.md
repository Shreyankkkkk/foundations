==================================================
SUMOX-26 COMPLETE WIRING PLAN (based on latest code: 3 opponent + 2 edge sensors)
Pack confirmed: 3x 18650 in series (3S), 9.0-12.6V range
==================================================

MATERIALS LIST + WHY EACH IS THERE
-----------------------------------
1. 3x 18650 cells (3S series)      - main power source, 9-12.6V range
2. 2x 3-way 18650 holder (1 active, 1 spare) - enables mid-match hot-swap
3. BH-042100-04U 4-way charger     - charges spare set between/before matches
4. 35A blade fuse + waterproof holder - protects pack/wiring from short-circuit fire risk
5. KCD4 main switch (DC 12-24V rated) - master on/off, cuts all power at once
6. AC rocker start/trigger switch  - low-current logic-side start trigger
7. ZORZA 5V 5A UBEC                - steps 9-12.6V pack down to safe, stable 5V
                                      (sensors are rated 4.5-5.5V, raw pack would destroy them)
8. 2200uF 35V capacitor            - bulk smoothing on positive bus, absorbs motor
                                      current spikes so UNO Q doesn't brown out
9. 470uF 16V capacitor             - local smoothing on UBEC 5V output, keeps
                                      sensor supply clean/quiet for analog readings
10. 2x BTS7960 43A motor driver    - PWM + direction control for each drive motor
11. 2x Titan 12V 200RPM motors     - drivetrain
12. 3x GP2Y0A21 IR sensor          - opponent detection (left/center/right)
13. 6x 10kOhm resistors            - 3 voltage dividers (2 per sensor) protecting
                                      UNO Q's 3.3V-max analog pins from sensor output
14. 2x TCRT5000 edge sensor        - front/back white-line detection
15. UNO Q board                    - mandated controller, runs all logic

==================================================
POWER WIRING
==================================================
Pack(+) -> 35A fuse -> KCD4 switch -> POSITIVE BUS
  reason: fuse = fire/short protection, switch = single master cutoff

POSITIVE BUS -> UNO Q VIN
  reason: powers board via its own onboard regulation

POSITIVE BUS -> BTS7960 (L) B+
POSITIVE BUS -> BTS7960 (R) B+
  reason: motors need raw pack voltage directly, not regulated 5V

POSITIVE BUS -> UBEC 5V 5A input
  reason: steps pack voltage down to safe 5V for sensors

POSITIVE BUS -> 2200uF 35V cap (+), cap(-) -> ground
  reason: dampens current spikes right at the source before they
          propagate through the whole system

UBEC 5V OUT -> 470uF 16V cap (+), cap(-) -> ground
  reason: local smoothing right where sensors draw power

UBEC 5V OUT -> all 3x GP2Y0A21 VCC
  reason: sensors need clean regulated 5V, never raw pack voltage

UBEC 5V OUT -> AC rocker start/trigger switch
  reason: low-current logic switch is fine off the regulated rail

COMMON GROUND: pack-, UNO Q GND, both BTS7960 GND, UBEC GND,
both cap negatives, all 3 GP2Y0A21 GND, both TCRT5000 GND,
all 3 divider bottom legs
  reason: one shared ground reference is mandatory -- any ground
          offset between sensor and board corrupts analog readings
          and defeats divider math

==================================================
MOTOR DRIVERS (BTS7960 x2)
==================================================
D2 -> LEFT_L_EN      D6 -> RIGHT_L_PWM (PWM)
D3 -> LEFT_R_PWM(PWM) D7 -> RIGHT_R_EN
D4 -> LEFT_R_EN       D8 -> RIGHT_L_EN
D5 -> LEFT_L_PWM(PWM) D9 -> RIGHT_R_PWM(PWM)
  reason: EN pins enable each half-bridge, PWM pins set speed/direction
Driver B+ -> positive bus, B- -> ground, M1/M2 -> motor terminals
  reason: swap M1/M2 pair (not logic pins) if a motor spins backward

==================================================
EDGE SENSORS (TCRT5000 x2: front, back)
==================================================
D10 -> EDGE_FRONT (DO)
D11 -> EDGE_BACK  (DO)
Each sensor: VCC -> 3.3V, GND -> common ground, DO -> pin above
  reason: 3.3V keeps sensor logic level matched to UNO Q's native
          digital input, no divider needed for digital signals

==================================================
OPPONENT SENSORS (GP2Y0A21 x3: left, center, right) + DIVIDERS
==================================================
A0 -> OPPONENT_LEFT   (through its own divider)
A1 -> OPPONENT_CENTER (through its own divider)
A2 -> OPPONENT_RIGHT  (through its own divider)

Each sensor: VCC -> UBEC 5V, GND -> common ground
  reason: sensor needs real 5V to operate correctly, must never
          touch raw pack voltage (9-12.6V would destroy it)

DIVIDER (build 3x, one per sensor):
Sensor Vo --- R1(10k) ---+--- UNO Q analog pin
                          |
                        R2(10k)
                          |
                      common ground
  reason: sensor output can peak near/above 3V, UNO Q ADC max is
          3.3V with thin safety margin -- divider halves the
          voltage reaching the pin, protecting the board from any
          spike, noise, or unit-to-unit variance

==================================================
NOTES
==================================================
- This plan reflects the LATEST code (3 opponent + 2 edge sensors).
  If you're still physically building toward 4+4, flag that --
  the extra sensors (A3, D12/D13) need both wiring AND code changes.
- No start/round buttons wired in current code (A4/A5 unused) --
  countdown is a fixed timer from power-on.
- Threshold constants in Hardware.h must be recalibrated using
  readings taken THROUGH the dividers, on the real UNO Q, not
  raw bench values.
==================================================