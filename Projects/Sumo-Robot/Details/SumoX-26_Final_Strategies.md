# SumoX-26 Final Strategy Spec — Two Toggleable Strategies (3kg class)

Two strategies, built on one shared skeleton, toggled with a mode switch (digital input pin, or `#define STRATEGY 1/2` flipped before each flash). They share almost all of their code — the only functional difference is *how the robot turns while approaching a detected opponent*.

- **Strategy 2 — Baseline (build this first):** simple, reliable, matches how most real competitive sumo robots are actually coded (Cytron/Team Ikedo's published tutorial code, and the "find opponent → push" philosophy described by BrooksBots for their own 3kg-class robot, ExSpurt/Executioner).
- **Strategy 1 — Flanking:** identical skeleton, but the approach uses proportional (P-controller) steering instead of a hard on/off turn, so the robot curves smoothly toward the opponent instead of pivoting — which can catch a dodging opponent from the side as a side effect of how it steers.

Build Strategy 2 completely and get it competition-ready first. Strategy 1 is then a small, incremental change to one function, not a second robot.

---

## Hardware / pin reference (from your wiring diagram)

- LEFT BTS7960: RPWM → D5, LPWM → D6, R_EN+L_EN → D7
- RIGHT BTS7960: RPWM → D9, LPWM → D10, R_EN+L_EN → D8
- Opponent sensors (GP2Y0A21, analog): 2 front-facing + 1 left side + 1 right side → A0–A3 (confirm exact pin-to-position mapping on the bench before writing detection logic)
- Edge sensors (TCRT5000, digital), one per corner: D10–D13 in your current pin map (or D3/D4/D12/D13 per the original spec — confirm against your finalized pin map before wiring code)
- Start button: D2 + GND

**Tunables to calibrate on the bench — do not guess final values:**

| Tunable | What it controls |
|---|---|
| `DIST_THRESHOLD` | raw ADC value at which a GP2Y0A21 reading counts as "opponent detected" |
| `EDGE_THRESHOLD` | digital state that counts as "white detected" per TCRT5000 |
| `Kp` | proportional steering gain (Strategy 1 only) |
| `ERROR_DEADBAND` | how small the left/right error must be before steering is treated as zero (Strategy 1 only) |
| `SQUARED_THRESHOLD` | how small the error must be, for how many consecutive loops, before committing to `attack()` |
| `SWEEP_SPEED_L` / `SWEEP_SPEED_R` | the two motor PWM values that produce your search arc |
| `LOST_TARGET_LOOPS` | consecutive below-threshold loops before a target is considered lost |
| `REPOSITION_MS` | how long to nudge forward/back before resuming search after a fruitless turn |

---

## SHARED CORE (identical in both strategies)

1. **Setup:** initialize motor PWM/enable pins as OUTPUT, GP2Y0A21 pins as ANALOG INPUT, TCRT5000 pins as INPUT, start button as INPUT_PULLUP. Motors stay at zero output.
2. **Wait for start:** poll the start button. On trigger, begin the mandatory 5-second stationary window — sensors already reading, motors still at zero.
3. **`readDistanceSensors()`:** read all 4 GP2Y0A21 analog pins every loop; push each into a small rolling buffer (3–5 samples) to smooth noise before comparing against `DIST_THRESHOLD`.
4. **`checkEdges()`:** read all 4 TCRT5000 pins every loop; return true immediately if any reads "white." Must be called and checked *before any drive command*, every loop, in every state, no exceptions.
5. **`edgeRecover(side)`:** reverse both motors briefly, pivot away from the triggering side, then return control to whichever state was active before the edge fired (search, approach, or attack all interrupt into this).
6. **`attack()`:** drive both motors forward at full matched PWM. Baseline behavior: no steering correction once called — commit fully. (See the "Destroy" note near the end for an optional upgrade once the baseline is solid.)
7. **`reposition()`:** if a search-and-turn cycle comes up empty (turned toward a detected sensor, signal vanished before squaring up, and the fallback/predict window — Strategy 1 only — also comes up empty), drive forward or backward for `REPOSITION_MS` before resuming search. This changes your vantage point instead of re-scanning from the exact same spot, since the ring is small and static.
8. **Main loop structure, all strategies:**
   ```
   loop():
     if checkEdges(): edgeRecover(triggeringSide); return
     readDistanceSensors()
     run the active strategy's state machine using the fresh sensor data
   ```

---

## STRATEGY 2 — Baseline (Search → Detect → Approach → Attack → Back Off)

This is the strategy the research backs most strongly: a real 3kg-class competitor's own description of their strategy across every robot they've built is literally "find the opponent, then push" — with the push depending on getting there before the opponent can dodge. A published tutorial from a real sumo-kit team runs the exact same four-part structure (start → search → attack → back off), with search implemented as a circular sweep by giving the two motors different fixed speeds.

### 1. Before searching (idle / pre-search)

- During the mandatory 5-second start window: motors at zero, `readDistanceSensors()` and `checkEdges()` already running every loop so you have live data the instant the window ends.
- Optional but worth adding cheaply: 1–3 short **start routines** — a brief fixed pre-programmed maneuver (e.g. "turn 45° right, then go straight for X ms, then fall into normal search") run once at the start of a round, before the main loop takes over. The idea (borrowed from real competitive practice) is that first contact made from the side or rear of the opponent is a free advantage, and varying which start routine you use between rounds means the opponent can't pre-plan around it. If you don't have time to build this, skip straight to Search — it's optional polish, not a requirement.

### 2. Search — what the robot does until any sensor detects something

This is the part you asked about directly. Do **not** spin in place. Drive the two motors at two different fixed PWM values (`SWEEP_SPEED_L` ≠ `SWEEP_SPEED_R`) so the robot traces a wide, continuous arc/circle while moving — covering ground across the ring while still scanning, rather than rotating on the spot and covering none. This is explicitly the most commonly used opponent-searching method among competitive teams, and matches what a real 3kg-class competitor describes: a search loop slow enough to spot an opponent entering the middle of the ring, but fast enough that the opponent can't easily get around to your side or rear while you're mid-sweep.

```
SEARCH:
  if checkEdges(): edgeRecover(); return      // shared core, checked first, always
  readDistanceSensors()
  setMotor(LEFT, SWEEP_SPEED_L)
  setMotor(RIGHT, SWEEP_SPEED_R)
  if any sensor reading crosses DIST_THRESHOLD:
    record which sensor, go to DETECT
```

Tune `SWEEP_SPEED_L`/`SWEEP_SPEED_R` on the bench: too close together and the arc is too wide (you'll drift toward the ring edge before completing a loop — watch your edge sensors during testing); too far apart and you're closer to pivoting-in-place, losing the ground-covering benefit. A moderate difference (e.g. one motor at ~60% of the other) is a reasonable starting point to test from.

### 3. Detect

The instant any sensor's rolling-average reading crosses `DIST_THRESHOLD`, stop the search sweep. If multiple sensors cross it in the same loop, pick the one with the strongest (closest) reading — that's your target direction.

### 4. Approach (Turn)

Hard on/off differential turn toward the detected sensor's side: the motor on the side *opposite* the detection runs at normal/high speed, the motor on the *same* side as the detection slows or stops, rotating the robot to face the target.

```
APPROACH:
  if checkEdges(): edgeRecover(); return
  readDistanceSensors()
  if detected sensor is LEFT-side:
    setMotor(LEFT, TURN_SLOW)
    setMotor(RIGHT, TURN_FAST)
  else if detected sensor is RIGHT-side:
    setMotor(LEFT, TURN_FAST)
    setMotor(RIGHT, TURN_SLOW)
  if front-center sensor(s) become the strongest reading:
    go to SQUARED-UP
  if all sensors drop below threshold for LOST_TARGET_LOOPS consecutive loops:
    reposition(); return to SEARCH
```

### 5. Squared-up → Attack

Once the front sensor(s) are the strongest reading — you're roughly facing the target — call `attack()`: both motors to full matched PWM, no correction, hold until either an edge fires (handled by shared core, interrupts everything) or the target is lost for several consecutive loops.

### 6. Lost target / edge → back to Search

- Lost target during Approach or Attack: don't immediately drop back to a blind Search. First try `reposition()` (nudge forward/back, since you may just be repeating a scan from the same spot), then resume Search.
- Edge fired: `edgeRecover()` handles the immediate reverse-and-pivot, then control returns to whatever state was active — if that was Search, resume the sweep; if it was Approach/Attack, drop back to Search once clear of the edge, since you've lost your positional reference anyway.

### Why this is the recommended baseline

Three independent sources converge on this exact shape (active circular search, full-speed straight attack once detected, edge-triggered back-off, nothing fancier): a real 3kg-class competitor's own strategy writeup, a published sumo-kit tutorial's actual code structure, and general competitive-build advice that actively seeking the opponent is an advantage over sitting still. It's also the fastest of the two strategies to get working end-to-end, which matters given where you are on the code right now (motor logic done, everything else remaining).

---

## STRATEGY 1 — Flanking (same skeleton, proportional-steering Approach)

Everything above is identical — same pre-search, same Search sweep, same Detect, same shared core, same edge/lost-target handling. The **only** change is what happens inside Approach.

### The steering logic

```
error = rightSensorReading - leftSensorReading
steering = Kp * error
leftMotor  = BASE_SPEED - steering
rightMotor = BASE_SPEED + steering
```

- `error` is a single number describing how far off-center the opponent is. Near zero → opponent is roughly centered. Large positive → opponent is well over to the right (right sensor reading higher/closer than left).
- `steering = Kp * error` scales that offset into a correction. `Kp` is a bench-tuned constant — too high causes oscillation/overshoot, too low turns too sluggishly to track a moving target.
- The result is a continuously variable arc instead of a fixed pivot: small error → gentle curve, large error → sharp curve.

```
APPROACH (flanking):
  if checkEdges(): edgeRecover(); return
  readDistanceSensors()
  error = rightReading - leftReading
  if abs(error) < ERROR_DEADBAND:
    steering = 0                       // prevents jitter from sensor noise near zero
  else:
    steering = Kp * error
  setMotor(LEFT,  BASE_SPEED - steering)
  setMotor(RIGHT, BASE_SPEED + steering)
  if abs(error) < SQUARED_THRESHOLD for several consecutive loops:
    go to SQUARED-UP → attack()
  if all sensors drop below threshold for LOST_TARGET_LOOPS consecutive loops:
    reposition(); return to SEARCH
```

### Sensor layout note — which pair to use for `error`

Your actual layout is 2 front sensors + 1 left side + 1 right side, not four symmetric sensors. Decide explicitly which sensors feed `error`:

- **Front pair for `error`, side sensors as an override:** while the opponent is still roughly ahead, use the two front sensors for fine, smooth centering. If a side sensor crosses `DIST_THRESHOLD` on its own (meaning the opponent has swung wide enough to leave the front cone entirely), treat that as a hard override — sharp turn toward that side — rather than feeding it into the same proportional formula. This gives you fine tracking most of the time and a fast wide-angle correction for the cases furthest to the side, which is where an actual flank becomes possible.
- Whichever pairing you choose, keep it consistent and document it in code comments — this is the one design decision in Strategy 1 that isn't fully determined by the formula alone.

### A caveat worth knowing before you tune

The GP2Y0A21's output voltage isn't linear with distance — it rises steeply as the opponent gets close and flattens out (and gets noisier) farther away. A fixed `Kp` will feel different at long range than at close range. In sumo, most of the actual engagement happens at short range, where the sensor's response is strongest, so this is usually manageable — but expect to tune `Kp` specifically against close-range behavior, not assume a single value works everywhere.

### Does this actually produce a flank?

It's a real tendency, not a guarantee. Turning while still moving forward (an arc) instead of pivoting in place means you keep closing distance while correcting heading — if your turn radius and the opponent's evasive movement line up, you end up approaching at an angle instead of dead-on, which can catch a side or rear panel instead of a front wedge-on-wedge collision. Whether it actually lands depends on `Kp`, your top speed, and how fast the opponent reacts. Treat it as "smoother tracking that sometimes catches a flank," not a dedicated flanking maneuver — that's consistent with the decision to not build a fully separate flanking strategy given the time available.

### Optional: vary the start routine instead of (or alongside) proportional steering

A structurally simpler way to increase the odds of a side/rear hit, used by real competitive robots, is to vary the **start routine** — the very first fixed maneuver run at the start of a round (e.g., turn 45° one way before falling into normal search) — so first contact is more likely to land on the opponent's side or rear rather than head-on. This costs almost nothing to add (a short fixed sequence run once before Search begins) and doesn't require any sensor math. Worth having as a cheap fallback if `Kp` tuning eats more bench time than expected.

---

## Optional upgrade (after both strategies work): continuous correction during Attack

The baseline `attack()` above is full commit, zero correction, once called — deliberately, for simplicity and to avoid losing push torque or your wedge's square-on angle mid-charge. A real 3kg-class competitor's robot instead runs a second program during the push itself: quick, small corrective direction changes to keep the opponent centered as it wriggles, using its outer sensors, and if contact is lost mid-push, it assumes the opponent spun to one side and backs up to reacquire from that side rather than resetting to a blind search. This is a meaningfully more complex behavior than what's specified above — don't build it until the baseline Search → Detect → Approach → Attack → Back Off loop is fully working and tested on the bench. If you have time left after that, it's a reasonable next thing to try, and it would slot in as a modification of `attack()` plus a variant of the lost-target handling already described above.

---

## Suggested build/test order

1. Shared core (sensor reads with rolling buffer, edge-check, edge-recover, `attack()`, `reposition()`) — test each in isolation first, especially edge detection, since it interrupts everything else.
2. Strategy 2 end-to-end (Search sweep → Detect → hard-turn Approach → Squared-up → Attack → Back Off). This is your competition-ready safety net — get this fully working before touching Strategy 1.
3. Strategy 1 — swap the Approach function for the proportional-steering version above; everything else is unchanged. Bench-test `Kp` and `ERROR_DEADBAND` extensively before trusting it in a match; start with a low `Kp` and increase gradually.
4. Wire the mode switch (or `#define STRATEGY`) so both can be flashed and tested head-to-head in practice matches before deciding which one goes into the actual competition, or whether you run Strategy 2 in Round 1 and Strategy 1 in Round 2 if Round 1 is lost.

## Reference material for dissecting real source code

- Four Arduino sumo-robot repositories already identified as reference material — full source, not tutorial snippets: `mechengineermike/SimpleSumo`, `ethanphunter/Mini-Sumo`, `OliverLSanz/project-pineapple`, `CodyKoInABox/sumoRobot`.
- Cytron's published sumo-strategy tutorial (search "Cytron Sumo Robot Game Strategies") walks through the same four-part start/search/attack/back-off structure with real Arduino-style code using their `MakerSumo` library — useful as a second reference implementation of the baseline loop above.
- Cytron's SUMO:BIT firmware repository (`CytronTechnologies/pxt-sumobit` on GitHub) has full driver source for the same logic, but written for the BBC micro:bit in MakeCode/JavaScript — the state-machine logic is directly comparable even though the code isn't portable line-for-line.
