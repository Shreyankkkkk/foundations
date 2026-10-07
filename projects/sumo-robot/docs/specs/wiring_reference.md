==================================================
SUMOX-26 WIRING REFERENCE (current hardware.h)
==================================================

--- POWER ---
6x 18650 pack -> 35A fuse -> KCD4 main switch -> positive bus
Positive bus -> UNO Q VIN
Positive bus -> BTS7960 (L) B+
Positive bus -> BTS7960 (R) B+
Positive bus -> ZORZA 5V 5A UBEC input
Positive bus -> 2200uF 35V cap (+), cap (-) -> common ground
UBEC 5V out -> 470uF 16V cap (+), cap (-) -> common ground
UBEC 5V out -> GP2Y0A21 VCC (all sensors)
COMMON GROUND: pack-, UNO Q GND, both BTS7960 GND, UBEC GND,
both cap negatives, all GP2Y0A21 GND, all TCRT5000 GND,
all divider bottom legs -- ONE shared ground net, no exceptions

--- MOTOR DRIVERS (BTS7960 x2) ---
D2 -> LEFT_L_EN
D3 -> LEFT_R_PWM (PWM)
D4 -> LEFT_R_EN
D5 -> LEFT_L_PWM (PWM)
D6 -> RIGHT_L_PWM (PWM)
D7 -> RIGHT_R_EN
D8 -> RIGHT_L_EN
D9 -> RIGHT_R_PWM (PWM)
Both drivers: B+ -> positive bus, B- -> common ground
M1/M2 -> motor terminals (swap pair to fix spin direction, never rewire logic pins)

--- EDGE SENSORS (TCRT5000 x2 -- FRONT/BACK ONLY, matches this code) ---
D10 -> EDGE_FRONT (DO)
D11 -> EDGE_BACK (DO)
Each sensor: VCC -> 3.3V, GND -> common ground, DO -> pin above

--- OPPONENT SENSORS (GP2Y0A21 x3 -- LEFT/CENTER/RIGHT) ---
A0 -> OPPONENT_LEFT (through its own divider)
A1 -> OPPONENT_CENTER (through its own divider)
A2 -> OPPONENT_RIGHT (through its own divider)
Each sensor: VCC -> UBEC 5V (NOT UNO Q 3.3V/5V pin), GND -> common ground

--- VOLTAGE DIVIDER (build 3x, one per sensor, 6 resistors total) ---
GP2Y0A21 OUT --- R1 (10k) ---+--- UNO Q analog pin (A0/A1/A2)
|
R2 (10k)
|
common ground

Steps per sensor:

1. R1 leg 1 -> sensor OUT wire
2. R1 leg 2 -> tap point -> UNO Q analog pin (this is what gets read)
3. Same tap point -> R2 leg 1
4. R2 leg 2 -> common ground
   Result: pin reads ~half of sensor output (5V sensor swing -> ~2.5V at pin, safe under 3.3V max)

--- NOT WIRED IN THIS CODE VERSION ---

- No A3 (4th opponent sensor) -- add if you physically have 4 sensors
- No D12/D13 (3rd/4th edge sensor) -- add if you physically have 4 sensors
- No A4/A5 start/round buttons -- currently just a fixed 5s countdown from power-on

==================================================
