# SumoX-26 Build — Key Terms & Design Reference

A working glossary of everything you need to understand to design this robot correctly, tied to your actual components (JSumo Titan 12V/200RPM motors, 52×30mm wheels, Arduino Uno Q) and the Dubai Techbots League rulebook.

---

## 1. Motor & Drivetrain Terms

| Term | What it means | Why it matters for your build |
|---|---|---|
| **Stall torque** | The maximum rotational force a motor produces when its shaft is prevented from turning at all (0 RPM), usually given in kg·cm or N·m. | Your Titan motor's 10.35 kg·cm stall torque is the number that determines your maximum theoretical push force — this is what you're fighting the opponent with during contact. |
| **Stall current** | The current a motor draws when stalled — always much higher than running current, since there's no back-EMF to limit it. | Your motor draws 4.1A at stall. This is the number your motor driver and power system (fuses, wiring gauge, capacitors) must be rated to survive repeatedly, since ramming an opponent puts the motor near stall constantly. |
| **No-load current / no-load speed** | Current drawn and RPM reached when the motor spins freely with nothing attached. | Your motor's 60mA no-load current tells you baseline power draw when just driving around, not pushing. |
| **RPM (output)** | Rotational speed of the *output shaft*, after any internal gearbox — not the raw motor speed. | Your "200 RPM" spec is already the geared-down output speed, which is what determines your wheel speed. |
| **Gear ratio** | The reduction between the motor's internal shaft speed and the output shaft speed (e.g., 60:1 means the motor spins 60 times for every 1 output rotation). | Higher ratios trade speed for torque. Your Titan's built-in 60:1 gearbox is fixed — you're not choosing this yourself, but you should understand *why* it's high (sumo needs torque over speed). |
| **kg·cm (kilogram-centimeter)** | A torque unit — the force (in kgf) applied at a 1cm lever arm. Convert to linear push force at the wheel by dividing by wheel radius (in cm). | This is how you calculated push force per wheel earlier: 10.35 kg·cm ÷ 2.6cm radius (52mm wheel) ≈ 3.98 kgf per wheel. |
| **Watts (motor power rating)** | Electrical power the motor is designed to handle continuously (V × A). | Used to size your power system and confirm the motor won't overheat under sustained load. |

---

## 2. Traction & Mechanical Terms

| Term | What it means | Why it matters for your build |
|---|---|---|
| **Coefficient of friction (μ)** | A ratio describing how much grip exists between two surfaces (wheel and arena floor). Max friction force = μ × Normal force (weight on the wheel). | This is your *actual* limiting factor, not motor torque — if μ × weight is less than your motor's theoretical push force, your wheels slip instead of pushing. |
| **Contact patch** | The area of wheel actually touching the ground. | Wider wheels (your 52×30mm) have a larger contact patch, which increases usable grip before slipping — this is why we picked it over the narrower 43×11mm option. |
| **Wedge angle** | The angle of your robot's front plate relative to the ground. | 8–12° (your target) lets the wedge slide under an opponent's chassis to lift/destabilize them, while staying shallow enough not to dig into the arena floor. |
| **Ground clearance** | Gap between the wedge's leading edge and the arena floor. | Your 0.5–1mm target is tight enough to get under most opponents without scraping or catching on the floor surface. |
| **Center of gravity (CG)** | The point where a robot's weight is balanced. | A low, rear-biased CG improves push stability and resistance to being lifted or flipped by an opponent's wedge. |
| **Weight distribution** | How the robot's total mass is spread across its footprint, especially over the drive wheels. | More weight on the drive wheels increases normal force → increases available friction → increases usable push force (ties directly into the μ × N relationship above). |

---

## 3. Electrical & Power System Terms

| Term | What it means | Why it matters for your build |
|---|---|---|
| **H-bridge** | A switching circuit (the core of any motor driver) that lets a motor spin forward or backward by controlling current direction. | Every motor driver you're evaluating (BTS7960, Cytron, etc.) is built around this. |
| **Motor driver current rating (continuous vs. peak)** | Continuous = current a driver can sustain indefinitely without overheating; peak = brief current it can survive. | Your driver needs continuous rating comfortably above your motor's 4.1A stall current — this was the deciding factor when comparing driver options earlier. |
| **PWM (Pulse Width Modulation)** | A technique for controlling motor speed by rapidly switching power on/off, varying the % of time it's "on" (duty cycle). | This is how your Arduino Uno Q will vary drive speed for PID-based steering corrections rather than just full on/off. |
| **Brownout** | A voltage drop severe enough to reset or glitch a microcontroller, often caused by a sudden current spike elsewhere in the circuit. | Your spec flagged this directly — motor stall current spikes on impact can brown out the Uno Q mid-match if the power system isn't buffered. |
| **Bulk/decoupling capacitors** | Capacitors placed near a power input to absorb sudden current demand spikes, keeping voltage stable. | The fix for the brownout risk above — placed on your VIN line. |
| **Voltage regulator / BEC (Battery Eliminator Circuit)** | A circuit that converts battery voltage down to a stable voltage for your control electronics, separate from the main motor power line. | Keeps your Uno Q's logic supply clean and isolated from the noisy, current-hungry motor circuit. |

---

## 4. Control & Sensing Terms

| Term | What it means | Why it matters for your build |
|---|---|---|
| **PID controller** (Proportional-Integral-Derivative) | An algorithm that continuously calculates the error between a target and current value, then smoothly adjusts output — instead of a jerky on/off response. | Central to your strategy: used both for smooth opponent-tracking turns and for keeping two drive motors matched during a straight-line charge. |
| **Kp, Ki, Kd** | The three tuning constants of a PID loop — Proportional (reacts to current error), Integral (corrects accumulated past error), Derivative (dampens overshoot by reacting to rate of change). | These *cannot* be copied from another robot — you'll tune them empirically on your assembled robot, as your spec correctly noted. |
| **Debounce / debounce timing** | Filtering logic that ignores rapid, spurious sensor state changes and only reacts to a sustained signal. | Prevents your robot from twitching left-right when both opponent sensors briefly trigger at once near contact. |
| **ADC (Analog-to-Digital Conversion)** | The process of converting a sensor's continuous analog voltage (like an IR distance sensor's output) into a digital value the Uno Q can read. | Relevant because the Uno Q's architecture differs from a classic AVR Arduino — worth confirming its analog input specs directly, since it's a newer Linux-based board. |
| **IR reflectance (edge) sensor** | A sensor that shines infrared light down and measures reflection to distinguish the dark arena floor from "no floor" (i.e., the edge). | Your edge-detection system — must be tuned against the rulebook's white 3cm arena frame, since the sensor is reading contrast, not distance. |
| **IR proximity/distance sensor** | A sensor that detects how far away a reflective object (the opponent) is. | Your opponent-detection/tracking system feeding into the PID loop. |
| **False-trigger filtering** | Logic to reject sensor readings caused by glare, lighting, or unintended reflective surfaces rather than the real target. | Needed because the rulebook's arena has a **white painted frame** — a strong reflective surface your edge sensors must correctly interpret as "the boundary," not ignore or misread. |

---

## 5. Rulebook-Driven Design Constraints (things the terms above must work within)

| Constraint | Rule reference | Design implication |
|---|---|---|
| **Max weight: 3kg** | 4.1 | Every component choice (motors, wheels, battery, chassis material) must be weighed against this budget — this is why we favored lighter/cheaper options where torque/traction weren't compromised. |
| **Max footprint: 20×20cm** (no height limit) | 4.2 | Leaves you room to go tall if needed, but constrains wedge width and wheelbase. |
| **Controller must be Arduino Uno Q — no other primary microcontroller allowed** | 4.4 | **This overrides my earlier suggestion to use a Nano instead.** You must learn the Uno Q's specific I/O, PWM, and ADC behavior (it's a newer Linux-based SBC, not a classic AVR board) since your whole PID/sensor/motor-driver logic has to run on it specifically. |
| **Fully autonomous — no remote control** | 4.4 | Your decision loop (edge check → opponent check → PID drive) must run entirely onboard with no human input after activation. |
| **Front/wedge must not be white or a color that affects sensor readings** | 4.5 | Confirms your matte non-white wedge finish decision was correct — this is a hard rule, not just good practice. |
| **No magnets, suction, vacuum wheels, or adhesives** | 4.6 | Confirms your traction strategy must come entirely from wheel width/compound (like the 52×30mm silicone wheel), not from artificially anchoring to the floor. |
| **5-second mandatory stationary period after activation** | 6.2 | Your control loop must include a hard-coded 5-second delay before any movement — moving early is an explicit warning-triggering offense (7.3). |
| **3-minute round timer** | 6.7 | Your search-pattern/engagement logic needs to be effective within this window — long, cautious search patterns risk timing out without contact. |
| **Arena: 1.5m diameter, white 3cm frame, black surface** | 5.1 | Confirms your edge sensors are distinguishing black (safe) from the white frame boundary (edge) — directly relevant to the false-trigger filtering concept above. |

---

## 6. What to Actually Study (in priority order)

1. **DC motor fundamentals** — torque/speed/current relationships, stall vs. running behavior. Directly explains every number on your motor's datasheet.
2. **Basic mechanics (torque → force conversion, friction)** — lets you calculate push force and understand why wheel width matters more than raw torque once you're traction-limited.
3. **Arduino Uno Q specifics** — since it's a newer Linux-based board rather than a classic AVR Arduino, its GPIO/PWM/ADC handling may differ from typical tutorials. Worth reading its official documentation directly rather than assuming it behaves like an Uno R3.
4. **PID control basics** — enough to implement and then manually tune Kp/Ki/Kd on your actual robot.
5. **Power electronics basics** — capacitor sizing for brownout protection, how voltage regulators/BECs work.
6. **Sensor debouncing and filtering logic** — small but critical code patterns that prevent erratic behavior near contact.
