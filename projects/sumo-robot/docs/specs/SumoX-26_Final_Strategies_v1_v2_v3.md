# SumoX-26 Final Strategy & Behavior Specification

This document serves as the definitive guide to the behavior and logic implemented in the SumoX-26 robot. It describes the shared core, the specific combat strategies, and the tactical optimizations that govern the robot's actions.

## 1. System Architecture & Priority
The robot operates as a high-priority state machine. In every loop, the following priority is enforced:
1. **Emergency Stop**: If the `START_BUTTON` (A4) is released, motors stop immediately and the robot returns to a waiting state.
2. **Edge Recovery**: If any edge sensor detects white, all other logic is bypassed to execute `edgeRecover()`. This event also resets target tracking state to prevent "ghost" attacks after recovery.
3. **Target Tracking**: If an opponent is detected, the robot enters the `approachTarget()` and `attack()` sequence.
4. **Search Arc**: If no opponent is detected and the robot is not in a blind-window attack, it executes a circular search sweep.

---

## 2. The Shared Core (Common Logic)

### A. Startup & The Randomized Start
To avoid predictability and "wedge-locks" at the start of a match, the robot uses a **Randomized Start Palette**.
- **The Sequence**: After the mandatory 5-second countdown, the robot randomly selects one of four maneuvers:
    - **Balanced Offset**: 200ms pivot $\rightarrow$ 300ms forward.
    - **The Aggressor**: 100ms pivot $\rightarrow$ 400ms forward (fastest approach).
    - **The Flanker**: 300ms pivot $\rightarrow$ 200ms forward (wide angle).
    - **The Blitz**: 0ms pivot $\rightarrow$ 300ms straight burst (maximum aggression).
- **Randomness**: The system is re-seeded using `micros()` at the moment the round-start button is confirmed, ensuring unique patterns even across power-cycles.
- **Safety**: All start maneuvers are safety-aware; if an edge is hit during the start move, it immediately triggers `edgeRecover()`.

### B. Sensor Processing
- **Opponent Sensing**: GP2Y0A21 sensors are sampled every 40ms. A rolling median buffer of 5 samples is used to eliminate noise before comparing against `DIST_THRESHOLD` (400).
- **Sample Gating**: Tracking logic is gated by the sample count; state changes (like counting lost targets) only occur when a new physical sample is read, preventing CPU-speed logic errors.
- **Edge Sensing**: TCRT5000 sensors are polled digitally. Any "White" detection (`HIGH`) triggers an immediate interrupt.

### C. Edge Recovery & Repositioning
- **`edgeRecover()`**: A state machine that determines the direction of the edge hit (front, back, or corner) and executes a deterministic retreat and pivot. It includes ambiguity handling (e.g., safe-pivot fallbacks) when multiple sensors trigger.
- **`reposition()`**: A fallback maneuver used when a target is lost. It nudges the robot forward or backward for 300ms to change its vantage point.
- **`executeBalancedOffset()`**: A specific version of repositioning used after losing a target, shifting the robot slightly to avoid a head-on collision on the next attempt.

---

## 3. Combat Strategies

### Strategy 1: Flanking (Proportional Tracking)
Designed for smooth, curving approaches.
- **Approach**: Uses a P-controller based on the difference between left and right sensor readings.
- **Hard Override**: If a side sensor is triggered, the robot bypasses proportional math and executes a maximum-rate turn to snap back onto the target.
- **Steering**: Otherwise, it calculates a `correction` value ($\text{Kp} = 0.5$). The robot doesn't pivot; it drives in a continuous arc toward the opponent.
- **Engagement**: Once the opponent is squared up (error $< 20$), it commits to the attack.

### Strategy 2: Baseline (Discrete Tracking)
Designed for reliability and sharp corrections.
- **Approach**: Uses discrete steering states (`STEER_LEFT`, `STEER_RIGHT`, `STEER_STRAIGHT`).
- **Hysteresis**: To prevent "jitter" between left and right turns, the robot uses a `SIDE_TURN_MARGIN` (25) and a `SIDE_TURN_HYSTERESIS` (10) zone.
- **Confirmation**: A steering change is only committed if the target remains in that direction for 50ms.
- **Engagement**: Once front sensors are strongest, it commits to the attack.

---

## 4. Tactical Optimizations (The "Combat Edge")

### A. Active Push Correction
The robot does not simply drive straight when attacking. It applies a continuous steering correction during the push:
- **Logic**: `drive(ATTACK_SPEED + correction, ATTACK_SPEED - correction)`.
- **Purpose**: Keeps the robot's wedge centered on the opponent even if the opponent drifts or the robot slips.
- **Gain (Strategy 2)**: $\text{Push Kp} = 2$.

### B. The Hammer Attack & Blindness Protection
To win a "lock" where both robots are pushing against each other, the robot employs PWM oscillation:
- **Hammer Logic**: Rapidly toggles the base attack speed between `ATTACK_SPEED` (240) and `(ATTACK_SPEED - HAMMER_AMPLITUDE)` (190) every 100ms to break static friction.
- **Blindness Protection**: Once a push is committed (latched via `attackDeadline`), the robot continues to hammer for a short window (`ATTACK_COMMIT_MS`) even if sensor contact is lost. This ensures the robot doesn't abort an attack just because the opponent entered the sensor's near-field blind zone.

---

## 5. Calibration Cheat Sheet (Current Values)

| Parameter | Value | Unit/Description |
|---|---|---|
| **Sensing** | | |
| `DIST_THRESHOLD` | 400 | ADC value for detection |
| `SENSOR_SAMPLES` | 5 | Rolling buffer size |
| **Search** | | |
| `SEARCH_SLOW_SPEED` | 120 | PWM for slow motor |
| `SEARCH_FAST_SPEED` | 180 | PWM for fast motor |
| `SEARCH_FIRST_ARC_MS` | 600 | Initial pivot duration |
| `SEARCH_ARC_FLIP_MS` | 1100 | Standard arc flip duration |
| **Approach** | | |
| `APPROACH_SPEED` | 165 | Base approach speed |
| `TURN_SPEED` | 100 | Pivot speed during approach |
| `S1_Kp` | 0.5 | Proportional gain |
| `S1_DEADBAND` | 20 | Error threshold for attack |
| `S2_MARGIN` | 25 | Side detection threshold |
| **Attack** | | |
| `ATTACK_SPEED` | 240 | Base push power |
| `HAMMER_AMPLITUDE` | 50 | PWM oscillation depth |
| `HAMMER_PERIOD_MS` | 100 | Oscillation frequency |
| `S2_PUSH_KP` | 2 | Push correction gain |
| **Safety** | | |
| `REPOSITION_MS` | 300 | Nudge duration |
| `EDGE_RECOVER_SPEED` | 170 | Retreat speed |
| `OFFSET_SPEED` | 150 | Maneuver speed |
