# SumoX-26 code guide (v2.4)

## 1. The idea in one paragraph
Every **5 ms** the robot repeats one cycle (`robotLoop()` in `Robot.cpp`): **check the stop switch → read sensors → check the edge (top priority) → ask the strategy what to do → drive the motors → update the map.** The strategy is a small state machine: sweep, search, align, charge, return, back off. A dead-reckoning map estimates where we are and how wrong that guess could be, and it limits our speed so we can stop before the rim.

## 2. Files
| File | Job (in plain words) |
|---|---|
| `SumoX26.ino` / `v2.4_Strategy.ino` | Entry point. `setup()` calls `initRobot()` once, `loop()` calls `robotLoop()` forever. |
| `Hardware.h` | Numbers **you type**: pins, rulebook values, ruler/stopwatch measurements, tuning knobs. |
| `Formulas.h` | Numbers the code **calculates** from `Hardware.h`. Never type here. (`Hardware.h` includes it at the bottom.) |
| `Motors.cpp/.h` | The only code that touches motor pins. |
| `Sensors.cpp/.h` | Decides what counts as "opponent" and "edge". |
| `Map.cpp/.h` | Position guess, uncertainty, speed limit. |
| `Strategy.cpp/.h` | The brain: picks what to do. |
| `Robot.cpp/.h` | The conductor: startup, stop switch, priority order, edge recovery. |
| `Calibrate.ino` (separate folder) | Prints sensor readings so you can fill in thresholds. |

## 3. Hardware.h — what you type
- **Wiring:** `LEFT_L_EN`, `LEFT_R_PWM`, `LEFT_R_EN`, `LEFT_L_PWM` (pins 2-5) and the right driver (6-9); `EDGE_FRONT` D10, `EDGE_BACK` D11; `OPPONENT_LEFT/CENTER/RIGHT` A0-A2; `START_BUTTON_PIN` A4 (the rocker).
- **Flags:** `LEFT_MOTOR_INVERTED` / `RIGHT_MOTOR_INVERTED` (flip if a wheel spins backward), `EDGE_WHITE_STATE` (fallback only, auto-detected at start), `POWER_BUTTON_PRESENT = false` (KCD4 is the power switch), `START_IS_LATCHING = true` (rocker stays ON), `START_SWITCH_ANALOG = true` (A4 is read as a voltage), `REARM_ENABLED`.
- **Rulebook:** `ARENA_TOTAL_DIAMETER_CM` 150, `ARENA_FRAME_THICKNESS_CM` 3, start-line numbers, `START_DELAY_MS` 5000, `STALEMATE_HARD_CEILING_MS` 30000.
- **Robot measurements:** `ROBOT_LENGTH_CM`, `REAR_TO_AXLE_CM`, `WEDGE_TO_FRONT_SENSOR_CM` 4.7, `REAR_TO_BACK_SENSOR_CM` 3.6, `ROBOT_WIDTH_CM`.
- **Motion (placeholders until measured):** `DRIVE_SPEED_MAX_CMS`, `SPIN_RATE_CW_DEGS`, `SPIN_RATE_CCW_DEGS`, `STOP_DISTANCE_CM`, `FRICTION_MU`, `MIN_MOVE_PWM`.
- **Sensor calibration:** `SENSOR_DIVIDER_RATIO` (9.9k/9.9k = 0.5), old bench numbers (`BENCH_*`), five `MEASURED_*` values, the switch `USE_MEASURED_THRESHOLDS`, and `ADC_NOISE_SIGMA`.
- **Tuning knobs:** `ALIGN_*`, `STALEMATE_*`, `EDGE_RECOVER_*`, `COMMIT_VOID_PWM`, etc.

## 4. Formulas.h — what the code calculates
- **Arena:** `ARENA_RADIUS_CM` 72 (black surface), `ARENA_OUT_RADIUS_CM` 75 (out line).
- **Robot shape:** `ROBOT_L_F_CM` (pivot to nose), `ROBOT_L_B_CM` (pivot to rear), `EDGE_SENSOR_FRONT/BACK_OFFSET_CM`, `ROBOT_R_SWING_CM` (farthest corner when spinning), `START_POSE_RADIUS_CM`.
- **Opening sweep:** `OPEN_SWEEP_HALF_ANGLE_DEG` = atan(20 / (22 + nose length)) + aiming error. `OPEN_SWEEP_LEG_A_MS`/`LEG_B_MS` turn it into times.
- **Motion:** `DRIVE_DECEL_CMS2` = v² / 2d. `COMMIT_SOFT_START_S` = v / (μg), the fastest push-off without wheel slip. `MOTOR_SLEW_PWM_PER_MS` = how fast power may rise.
- **Thresholds:** `WEAK_THRESHOLD`, `STRONG_THRESHOLD`, `NEAR_THRESHOLD`, `CONTACT_BAND_LOW/HIGH`, `PEAK_BAND_LOW/HIGH`. With `USE_MEASURED_THRESHOLDS = false` they are the old bench numbers x 0.5. Two `static_assert` lines stop the build if their order is wrong.
- **Timing:** `SENSOR_SAMPLE_INTERVAL_MS` 15 (from the sensor's refresh time), `WEAK_CONFIRM_SAMPLES` 4, `LOST_CONTACT_GRACE_MS` 60.
- **Noise filter:** `ADC_OVERSAMPLE_N` = number of reads we take and take the median of. N = (noise / (smallest threshold gap / 6))², made odd.
- **Start/stop:** `START_COUNTDOWN_MS` 5050, `REARM_HOLD_MS` 300, `START_SWITCH_THRESHOLD_ADC` ~387.
- **Search/align:** `SEARCH_SPIN_PWM`, `ALIGN_TIMEOUT_MS`, `SEARCH_COVERAGE_SWEEP_DEG` 270, `SEARCH_DWELL_MS` 60.
- **Stalemate:** `STALEMATE_BACKOFF_CM` = how far the 300 ms back-off travels.

## 5. Motors.cpp
- `initMotors()` enables the drivers at PWM 0. `disableMotorDrivers()` turns them fully off (boot state). `stopMotors()` stops instantly.
- `drive(left, right, immediate)`: clamps to ±255, limits acceleration (`slewToward()`), applies the inversion flags, and writes PWM through `setSide()` (positive → R pin, negative → L pin). Slowing down is never delayed. A reversal goes through zero first. `immediate = true` skips the limiter (edge recovery, stopping).
- `curL`/`curR` remember what was sent; `getAppliedLeft()`/`getAppliedRight()` give it to the map.

## 6. Sensors.cpp
- `readFiltered(pin)`: one throwaway read, then N reads, median. The UBEC ripple spikes get thrown out.
- `updateOpponentSensors()`: every 15 ms updates three channels (`updateChannel()`):
  - **Detected** = 2 strong readings (≥125) in a row, or 4 weak (≥75) in a row.
  - **Cleared** = 2 misses in a row.
  - **`near` latch** = set once a detected target reads ≥237, cleared when it's lost.
- `anyContact()`: true if `near` was latched **and** the reading is now in the contact band. The sensor peaks at ~6-10 cm then drops, so "peaked, then dropped" means touching.
- `primeOpponentSensors()` wipes the state. `getOpponentReadings()` gives raw numbers; `getOpponentDetection()` gives yes/no flags.
- **Edge:** `calibrateEdgePolarity()` reads both edge sensors while the robot sits on black and learns which pin state means white (falls back to `EDGE_WHITE_STATE` if they disagree). `readEdgeSensors()` reads twice, 200 µs apart, and both must agree.

## 7. Map.cpp
- **Pose** = x, y (cm from arena center) and heading. `initMap()` starts at (−`START_POSE_RADIUS_CM`, 0) facing the center.
- `mapUpdateMotion()`: moves the pose from the PWM actually applied (dead reckoning — it drifts).
- `mapUpdateContact()`: during a push the wheels slip, so x, y freeze and uncertainty grows 45 cm/s.
- **U** (`getUncertainty()`) grows with distance, turning, heading error and pushing.
- `mapSnapEdge()`: an edge hit tells us exactly where we are (radius 72). Position corrects and U resets; heading error does not.
- `isMapVoid()`: true once U ≥ 72 − swing radius − stop distance (36.8 cm by default). Past that the map isn't trusted.
- `getGovernedMaxSpeedCms()`: top speed that still lets us stop before the rim = √(2 × decel × margin).
- `shouldReturn()`, `getReturnHeadingDeg()`, `getReturnTurnDeltaDeg()`: "are we off-center, and which way to face the center".
- `getRearMaxRadius()`: how far the rear corners reach (used before backing off).
- `isPhantomDetection()` and `isEdgeReadingImplausible()` exist but are switched off.

## 8. Strategy.cpp — the states
Variables to know: `state`, `lastSeenSign` (+1 left, −1 right, 0 never), `alignFlipCount`, `contactStartMs`, `lastDetectMs`, `returnPhase`, `stalemateBreakCount`.
1. **OPEN_SWEEP:** spin left 35.5° (295 ms), then right 71° (590 ms). Any sighting ends it early.
2. **SEARCH:** spin up to 270° toward the last-seen side, pause 60 ms, flip direction. After the first leg: `RETURN` if the map is trusted and we're off-center, otherwise keep scanning.
3. **ALIGN:** spin toward the side that sees the opponent (170 PWM plus up to 85 more as the reading rises). Center sees it → charge. Lost → search. 3 side flips or 562 ms → charge anyway.
4. **COMMIT (charge):**
   - Touching: 255 PWM plus steering trim.
   - Not touching: ramp up over 76 ms, capped by the governor (never below `MIN_MOVE_PWM`, or `COMMIT_VOID_PWM` if the map is void).
   - Target lost for 60 ms → search.
   - Pushing for 9 s → `STALEMATE_BREAK`, **but only if** `rearClearForBackoff()` says the rear is provably clear. During a push the map usually becomes void, so most of the time it just keeps pushing.
5. **STALEMATE_BREAK:** reverse 300 ms (about 9 cm) with a sideways bias that alternates each time, then re-pick from the sensors.
6. **RETURN:** turn to face the center (within 5°), drive there until the distance ≤ U, then search. If it sees an opponent it aborts and fights (a center sighting always; a side sighting only if our swing radius won't hang over the edge).

## 9. Robot.cpp — the conductor
**Start (`initRobot()` then `armAndStart()`):**
1. Drivers off. `constantsValid()` halts the robot if a key constant is zero or NaN.
2. `initMotors()`, `initSensors()` (10-bit ADC).
3. `armAndStart()`: `initMap()`, `primeOpponentSensors()`, `waitForPress()` (rocker released 30 ms, then ON 30 ms — a rocker already ON at power-up is ignored until you flip it OFF and ON), `calibrateEdgePolarity()`, a **5.05 s countdown with motors at 0** (sensors still reading), then `resetStrategy()`: attack if an opponent is visible, otherwise start the sweep.

**Every tick (`robotLoop()`):**
1. Stop check: rocker OFF for 300 ms (`REARM_HOLD_MS`) → `armAndStart()` again (motors stop, wait for the next ON).
2. `updateOpponentSensors()`, `readEdgeSensors()`.
3. **Both** edge sensors white → drive up to 150 ms toward the end nearer the center (backward if the map is void).
4. **One** edge sensor white → `mapSnapEdge()` then recover (`handleEdgeRecoveryTick()`): front fired → reverse, back fired → forward, at 170 PWM (255 if touching the opponent). It ends when the opposite sensor fires, or the sensor has been clear for 110 ms and our swing fits inside the ring, or after 700 ms. Then it re-engages if an opponent is visible, otherwise returns/searches.
5. Otherwise: `updateStrategy()` picks the motor command, `drive()` applies it, and the map updates (`mapUpdateContact()` if touching, else `mapUpdateMotion()`).

**Priority:** stop switch → edge → strategy.

## 10. Calibrate.ino
Prints for A0, A1, A2 and A4: `mean`, `sigma` (noise), `min`, `max`, `us/read`, plus the two edge pin states. Run with motors off, then on (`RUN_MOTORS`). Use the numbers to fill the `MEASURED_*` values and `ADC_NOISE_SIGMA` in `Hardware.h`.

## 11. One round, as a story
Robot is placed, the lid is lifted, the whistle blows, you flip the rocker. It learns edge polarity, stays still 5.05 s, then attacks if it sees the opponent or sweeps left and right until it does. It charges; if the opponent disappears it searches; if an edge sensor sees white it backs away first and thinks later. After the round you flip the rocker OFF and the robot stops and waits for the next ON.

## 12. Honest limits (say these first)
- Speed, spin rate, friction and stop distance are placeholders until measured.
- Sensor thresholds are scaled estimates until measured through the dividers.
- The left/right turn direction must be checked on the real robot.
- The front edge sensor is 4.7 cm behind the wedge tip but the white frame is only 3 cm, so the tip can be past the line when the sensor fires. The map's speed limit helps; it cannot be guaranteed.
- When reversing onto the edge, the wheels are already over the white when the back sensor fires.
- The phantom gate is off, so a person standing near the arena (the safety zone) could be seen as an opponent.
- Logic was tested in a PC simulation (scripted sensors, 5 random-input runs of 90 simulated seconds, no errors). Physics was not tested.
