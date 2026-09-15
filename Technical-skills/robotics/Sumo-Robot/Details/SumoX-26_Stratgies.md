# Sumo Robot Strategy Specs — SumoX-26 (3kg class)

Hardware reference (from wiring diagram):
- LEFT BTS7960: RPWM → D5, LPWM → D6, R_EN+L_EN → D7
- RIGHT BTS7960: RPWM → D9, LPWM → D10, R_EN+L_EN → D8
- GP2Y0A21 distance sensors ×4 (analog, opponent detection): A0, A1, A2, A3
  - Assign each to a mounting position before coding, e.g. FL (front-left), FC-L (front-center-left), FC-R (front-center-right), FR (front-right)
- TCRT5000 edge sensors ×4 (digital, HIGH on black / LOW on white or vice versa — confirm with a multimeter test first): D3, D4, D12, D13
  - Assign each to a corner: e.g. front-left, front-right, back-left, back-right
- Start button: D2 + GND

Tunables to determine through bench testing (placeholders — do not guess final values, calibrate against your actual sensors and arena):
- `DIST_THRESHOLD` — raw ADC value at which a GP2Y0A21 reading counts as "opponent detected"
- `EDGE_THRESHOLD` — digital state that counts as "white detected" per TCRT5000
- `PREDICT_WINDOW_MS` — how long to keep turning after signal loss (Strategy 2 only)
- `SWEEP_ANGLE_MS` — motor-on time for one side of the fallback oscillation (Strategy 2 only)
- `SPIN_STEP_MS` — motor-on time per search increment (Strategy 3 only)

---

## SHARED CORE (build this first, all 3 strategies call into it)

1. **Setup**: initialize all pins (motor PWM/enable pins as OUTPUT, GP2Y0A21 pins as ANALOG INPUT, TCRT5000 pins as INPUT, start button as INPUT_PULLUP). Do not enable motors yet.
2. **Wait for start signal**: poll the start button (or however the round is triggered). On trigger, begin the mandatory 5-second stationary window — sensors already reading, motors still at zero output.
3. **`readDistanceSensors()`**: read all 4 GP2Y0A21 analog pins each loop, return an array/struct of 4 values. Push each into a small rolling history buffer (last 3–5 samples per sensor) for use by Strategy 2.
4. **`checkEdges()`**: read all 4 TCRT5000 digital pins each loop. Return true immediately if any reads "white." This function must be called and checked *before* any drive command is issued, every loop, in every strategy — no exceptions.
5. **`edgeRecover(side)`**: reverse both motors briefly, then pivot away from the triggering side, then return control to the active strategy's search state.
6. **`attack()`**: drive both motors forward at full matched PWM. Call only once the target sensor is roughly front-facing. No steering corrections once called — commit fully.
7. **Main loop structure** (applies to all 3 strategies):
   ```
   loop():
     if checkEdges(): edgeRecover(triggeringSide); return
     readDistanceSensors()
     run the active strategy's state machine using the fresh sensor data
   ```

---

## STRATEGY 1 — Sit, Wait, Scan, Move-Toward-Angle, Attack

No prediction, no rotation search. Stay stationary until a detection occurs, square up, then commit.

1. **IDLE**: motors at zero, keep calling `readDistanceSensors()` and `checkEdges()` every loop.
2. **DETECT**: if any sensor's latest reading crosses `DIST_THRESHOLD`, move to TURN state. If multiple sensors cross it, pick the one with the strongest (closest) reading.
3. **TURN**: apply differential PWM (motor on the opposite side of the detected sensor runs, motor on the same side slows/stops) to rotate toward the detected sensor's direction. Keep reading sensors each loop.
4. **CHECK-SQUARED**: once the front-center sensor(s) become the strongest reading (i.e., you're roughly facing the target), exit TURN and call `attack()`.
5. **ATTACK**: call `attack()`. Stay in this state until either (a) `checkEdges()` fires (handled by shared core, interrupts everything), or (b) all sensors drop below threshold for several consecutive loops (target lost) — then return to IDLE.
6. **LOOP**: after an edge recovery or a lost target, return to IDLE and repeat from step 1.

---

## STRATEGY 2 — Sit, Wait, Scan, Predict, Turn, Attack

Same as Strategy 1, plus a predictive-continuation layer when the signal disappears mid-engagement, and a bounded fallback sweep instead of giving up.

1. **IDLE**: same as Strategy 1 step 1.
2. **DETECT**: same as Strategy 1 step 2. Also record the detected sensor's direction and the loop's timestamp as `lastKnownDirection` and `lastSeenTime`.
3. **TURN**: same as Strategy 1 step 3, continuously updating `lastKnownDirection` while a signal is present.
4. **CHECK-SQUARED → ATTACK**: same as Strategy 1 steps 4–5, also continuously updating `lastKnownDirection` while attacking (in case the opponent slides off to one side mid-charge).
5. **SIGNAL-LOST**: if all sensors drop below threshold while in TURN or ATTACK, do NOT return to IDLE immediately. Instead:
   - Enter PREDICT state: keep turning in `lastKnownDirection` for up to `PREDICT_WINDOW_MS`, re-checking sensors every loop in case the target reappears (if it does, jump straight back to TURN/ATTACK as appropriate).
6. **FALLBACK SWEEP**: if `PREDICT_WINDOW_MS` elapses with nothing detected, perform a bounded oscillation: turn one direction for `SWEEP_ANGLE_MS`, then the other direction for `SWEEP_ANGLE_MS`, checking sensors continuously. If detected during the sweep, jump to TURN.
7. **GIVE UP TO IDLE**: if the sweep also finds nothing after a set number of oscillations, return to IDLE and repeat from step 1.

---

## STRATEGY 3 — Rotate, Scan, Attack

Simplest and most robust. No stationary phase beyond the mandatory 5s, no prediction — continuous rotation until something is found.

1. **SEARCH**: starting the moment the 5s window ends, rotate continuously in one direction (one motor forward, one motor reverse, or one motor forward/one motor stopped — pick whichever turn radius suits your wedge geometry) at a moderate speed. Read all 4 sensors every loop.
2. **DETECT**: the instant any sensor crosses `DIST_THRESHOLD`, stop rotating.
3. **SQUARE-UP** *(optional, can be skipped for max simplicity)*: brief correction turn toward the strongest sensor before attacking, same logic as Strategy 1 step 3–4. If skipped, just attack immediately in whatever heading you stopped at.
4. **ATTACK**: call `attack()`. Stay until edge-override fires or the target is lost for several consecutive loops.
5. **LOOP**: on lost target or after edge recovery, return to SEARCH (step 1) and resume rotating.

---

## Suggested build/test order

1. Shared core (sensor reads, edge-override, attack) — test in isolation first.
2. Strategy 3 — fewest states, fastest to get working end-to-end. This is your safety-net baseline.
3. Strategy 1 — small delta from Strategy 3 (swap rotate-search for stay-still-and-turn-to-signal).
4. Strategy 2 — build last, since `PREDICT_WINDOW_MS` and `SWEEP_ANGLE_MS` need real bench tuning against your actual sensors and motor response time.

Wire a mode switch (digital input pin, or a `#define STRATEGY 1/2/3` flipped before each flash) so all three can be tested head-to-head in practice matches before deciding which one goes into the actual competition.
