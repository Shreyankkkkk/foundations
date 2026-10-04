# SumoX-26 Championship Playbook
### A complete, beginner-to-advanced guide to building a winning autonomous sumo robot for the Dubai Techbots League (Besomi Academy × Arduino × Qualcomm × Canadian University Dubai)

> **How to use this guide:** It's written so you can start at zero knowledge in any subsystem (mechanics, electronics, or code) and build up. Each part starts with "what this even means" before getting technical. Read it top to bottom once, then use it as a checklist while you build. When you want to go deeper on any one section — motor math, sensor code, whatever — just ask, and we'll zoom in from there.

---

## PART 1 — The World of Robot Sumo (learn from the champions)

### 1.1 Where this sport comes from
Robot sumo isn't new — it's one of the oldest and most respected robotics sports in the world, and understanding its history tells you exactly what wins.

<cite index="5-1">Robot-Sumo began in Japan in 1989, when FUJISOFT Inc. organized an experimental robot-sumo tournament that became the All Japan Robot Sumo Tournament</cite>. Since 1998, <cite index="5-1">FUJISOFT has worked with more than 30 countries, and the sport has spread and become one of the most popular robotics competitions in the world.</cite> That tournament — the **All Japan Robot-Sumo Tournament (AJRST)** — is the closest thing this sport has to a World Championship, and it's held every December in Tokyo, gathering national champions from around the globe to fight for the international title.

The physical rules of that original Japanese competition are almost identical to yours: <cite index="6-1">a robot sumo win happens when the opponent robot touches the outside area of the ring, the robot must be designed only to push, and weapons or damaging devices are prohibited. Robot sumo must weigh 3 kg or less and measure 20 cm × 20 cm or less, with no height restriction.</cite> That means your event is running the exact same weight class as the world's top tournament — you're not in some watered-down junior version, you're building to the same spec real champions use.

### 1.2 Champions worth studying
- **Sakin (Turkey)** — <cite index="3-1">Sakin placed 2nd at the 2014 All Japan International Robot Sumo Tournament, a competition where the reigning three-year-unbeaten Japanese champion was defeated for the first time — then went on to win 1st place outright in 2015.</cite> Lesson: dethroning Japan is possible with disciplined engineering, not just budget.
- **Senju (Sumozade-Era Robotics, Turkey)** — recognized as the <cite index="7-1">first non-Japanese team to win the Mega Sumo Autonomous world title</cite>, a genuine underdog story.
- **ThundeRatz (Brazil)** — <cite index="7-1">dominated the RoboCore 3kg RC sumo class for years with their robot "Stonehenge," known for engineering discipline.</cite>
- **Georgia Tech RoboWrestling (USA)** — an active university team that <cite index="4-1">competes annually at the All Japan Robot-Sumo Tournament grand final, and is also building 3kg autonomous bots for regional qualifiers like RSM International in Brazil, which draws over 1,000 competitors.</cite>

### 1.3 Where the sport is growing right now
- **Japan** — still the historic center of gravity, but <cite index="7-1">in a notable 2025 shift, FUJISOFT pivoted focus toward the smaller 50g Mini Sumo class specifically to lower the barrier to entry and spark innovation in micro-robotics</cite> — a sign the sport is actively evolving.
- **Brazil** — <cite index="5-1">home to RoboCore, which ran the first official national robot-sumo tournament in Brazil in 2008, and became "the Brazilian National Robotics Championship" through the 2010s.</cite>
- **Turkey, Romania, China** — <cite index="7-1">Turkey and Romania both field strong competitive scenes, and China's RobotChallenge hosts large-scale championships as well.</cite>
- **UAE** — your event (Dubai Techbots League, backed by Besomi Academy, Arduino, and Qualcomm) is part of a fast-growing regional robotics scene alongside events like MBZIRC and the Emirates Robotics Competition — this is a young but serious ecosystem, and being early gives you a real shot at being a name people remember.

### 1.4 The one lesson every champion shares
Every write-up on elite sumo teams comes back to the same idea, and it's worth internalizing before you touch a screwdriver:

> **"Speed is life, but traction is god."** A fast, powerful robot that can't grip the floor is worthless. **Weight matters** — every one of your 3,000 grams should be doing a job. **Sensors are eyes** — a robot that can't see the opponent or the edge, no matter how strong, will lose or drive itself off the arena.

---

## PART 2 — Decoding Your Rulebook (in plain language)

Before building anything, let's translate the official terms into beginner language, because misunderstanding these costs teams matches.

| Rulebook term | What it actually means |
|---|---|
| **Round** | One single fight, up to 3 minutes. Whoever loses the pre-round coin-toss places their robot first. |
| **Match** | Best of 3 rounds (win 2 to take the match). If it's 1–1, a 3rd deciding round happens. |
| **Warning (yellow card)** | An official strike against your team for a rule slip-up. 6 warnings in the whole event = automatic disqualification. |
| **Violation (red card)** | An immediate, single disqualifying offense (e.g., intentionally damaging the opponent's robot). Forfeits all points and prize eligibility instantly. |

### 2.1 The numbers you must design around

| Spec | Limit | Why it matters |
|---|---|---|
| Weight | ≤ 3 kg | This is the classic "Mega Sumo" weight class used worldwide — every gram should add pushing power or control, not decoration. |
| Footprint | ≤ 20 cm × 20 cm | Measured at the **start** — no height limit at all, which is a real design opportunity (see §3.2). |
| Controller | **Arduino UNO Q — mandatory, no other primary microcontroller allowed** | This is unusual and a genuine advantage — more on this in Part 3. |
| Control mode | 100% autonomous — remote control is strictly banned | Your robot has to think for itself in real time. |
| Arena | 1.5 m diameter, circular, wooden, white 3 cm frame, black surface, two 20 cm brown centre lines | Know this surface — you'll calibrate your sensors against these exact colors. |
| Round timer | Max 3 minutes, starts after both robots have been stationary for 5 seconds post-whistle | Moving before the 5 seconds is literally a *listed cause for a warning*. |

### 2.2 The five rules that quietly decide matches (read these twice)
1. **Your front (blade/wedge) must NOT be white**, or any color that could interfere with sensor readings. This isn't cosmetic — the arena frame is white, so a white robot front risks confusing edge-detection logic (yours or the opponent's), and referees will flag it.
2. **No suction, vacuum wheels, magnets, or adhesives** to grip the arena — traction has to come from honest tire grip.
3. **No liquids, gases, powders, or projectiles** — pure pushing only.
4. **Size can change *after* the round starts**, as long as everything stays attached to the main body — this legally allows a "deployable" design (see §3.2).
5. **3 warnings in a single round = automatic loss of that round.** A detached part (even a small one) costs a warning *per part* unless it clearly didn't affect the match — so build things to stay attached.

---

## PART 3 — The Build: Step by Step

We'll go in the order you should actually build: **plan → mechanics → electronics → code → test.** Each step assumes you're new to that specific skill.

### STEP 1 — Design Planning & Weight Budget
**Beginner concept:** A "weight budget" just means deciding, on paper, how many of your 3,000 grams go to each part *before* you buy anything — so you don't build a great chassis and then discover there's no weight left for motors.

A reasonable starting budget for a 3 kg competitive bot:

| Component | Typical weight |
|---|---|
| Chassis + wedge front | 400–700 g |
| 2× drive motors + gearboxes | 300–600 g |
| Wheels + tires | 100–200 g |
| Arduino UNO Q + motor driver + wiring | 150–250 g |
| Battery (LiPo) | 150–300 g |
| Sensors (opponent + edge) | 50–100 g |
| Ballast (tungsten/steel weights, added last) | **remaining budget** |

That last row is deliberate — top teams always finish light and add **ballast** (extra weight) strategically at the very end, low and centered, to hit exactly 3.00 kg with the best possible weight distribution. Never design "to the limit" from the start.

### STEP 2 — Mechanical Design & Chassis
**Beginner concept:** "Center of gravity" (CG) is the average point where your robot's weight is balanced. A **low, centered CG** is the single biggest predictor of sumo success — it's why every serious sumo robot looks squat and heavy, never tall and top-loaded.

- **Chassis material:** Aluminum (6061-T6) is the gold standard — <cite index="29-1">strong, machinable, and dense enough to fill your weight budget efficiently. HDPE plastic works well for secondary, non-structural brackets, while thin acrylic should be avoided for structural parts because it shatters on impact.</cite>
- **Shape:** <cite index="29-1">A wider chassis resists being flipped sideways. Place your drive wheels near the outer edges of the frame for stability, and a 2-wheel differential drive with wheels toward the rear-center gives good maneuverability with a forward push bias.</cite>
- **The wedge/blade front:** The most common and effective mechanical trick in sumo robotics is a low-angled wedge at the front that <cite index="5-1">gets underneath the opponent to lift it slightly and make it easier to push</cite>. Remember: **not white, not a color that messes with sensors.** Matte black or a dark, non-reflective color is the safe, common choice.
- **The "no height limit" opportunity:** Since your rulebook only restricts the 20×20 cm footprint at rest and allows shape changes *after* movement begins, this is where a **deployable design** becomes a legal advantage — for example, side "wings" or a rear panel that flip open once movement starts to make you a harder target to flank, as long as everything stays attached to the body (rule 4.3). This is an advanced technique — get your basic robot working first, then consider this as an upgrade.
- **Wheels:** <cite index="22-1">Purpose-made silicone sumo wheels (like JSumo's) give the best grip, though modified toy-car wheels with added-friction surfaces are a valid budget option. Make sure the wheel's mounting hole matches your motor's output shaft diameter exactly.</cite>

### STEP 3 — Motors, Gearing & Wheels (the push power)
**Beginner concept:** *Torque* is rotational force (how hard the wheel can push against resistance); *speed* (RPM) is how fast it spins. A **gear ratio** trades one for the other — gearing down a motor makes it slower but much stronger, which is exactly what sumo needs.

- Sumo motors typically run at fairly high gear reduction, prioritizing torque over top speed — since the fight happens at close range, raw shove power usually beats speed. <cite index="26-1">Brushed DC motors with a gear ratio of roughly 10:1 or higher are the standard choice for high torque; brushless motors are also used by advanced teams for efficiency.</cite>
- Real-world example for your weight class: <cite index="29-1">for a 3 kg robot, two motors delivering roughly 8–10 kg·cm of torque each, driving 80–100 mm wheels, produces about 2–3 kg of usable push force — generally enough to overpower most opponents in this class.</cite>
- **A simple way to test if your motors are strong enough (no advanced math needed):** disconnect the wheels, hook a fish/luggage scale to the front of the finished robot, and slowly pull. The force reading at the moment it starts sliding tells you the minimum push force you need to beat — aim for your motors to comfortably exceed that.
- **Formula, if you want the actual math:** `Output torque = Motor torque × Gear ratio × Gearbox efficiency (usually ~80–90%)`. More gear stages = more torque but more heat and complexity — pick the *lowest* ratio that still clears your target with some margin.

### STEP 4 — Electronics: Building Around the Arduino UNO Q
This is the part that makes your competition genuinely different from older-style sumo events, so let's slow down here.

**What the UNO Q actually is (beginner explanation):** Most classic sumo robots use a simple microcontroller — a small chip that runs one program, reading sensors and driving motors, nothing else. Your rulebook mandates something much more powerful: <cite index="12-1">the UNO Q is Arduino's first Linux-capable board, combining a quad-core Qualcomm Dragonwing QRB2210 processor with GPU for AI and vision tasks, together with a dedicated STM32U585 real-time microcontroller — running Arduino sketches — on a single board.</cite> In plain terms: **it's two brains in one board.**

- **The "MCU" side (STM32)** behaves like a normal Arduino — this is what you'll use for the time-critical stuff: reading edge sensors and driving motors instantly, with no lag. <cite index="14-1">This side runs on Zephyr RTOS with the familiar Arduino core on top, so your sketches work as expected, and it handles real-time I/O with predictable, glitch-free timing.</cite>
- **The "MPU" side (Qualcomm chip)** runs a full Linux computer, capable of running a camera and lightweight AI models. <cite index="15-1">This lets you plug in a USB or CSI camera and use the board's AI engine for object detection or pattern recognition, right on the robot, with no cloud connection needed.</cite>
- **Why this matters competitively:** classic IR sensors can be fooled by black robots, weird angles, or bright arena lighting. A robot that uses the camera + AI side to visually identify "that's a robot, not the black floor" is a genuine, rules-legal edge over teams using only basic IR sensors — and it's exactly the kind of "edge AI" use case this board and its Qualcomm sponsor are built for. **This is an advanced upgrade path — build the reliable IR-sensor version first, get it competition-ready, then experiment with vision as a stretch goal.**

**Core electronics checklist:**
| Part | Beginner explanation | Notes |
|---|---|---|
| Arduino UNO Q | Your robot's brain (mandatory) | Program the MCU side with Arduino IDE/App Lab for real-time motor + sensor logic |
| Motor driver (H-bridge) | A "translator" that lets a low-power signal from the Arduino control a high-power motor safely | Choose one rated for at least your motors' stall current |
| Battery | Power source | LiPo (lithium polymer) is standard — <cite index="22-1">high power for its size, commonly used in the 2–3 cell (7.4–11.1V) range for 12V-class motors</cite> |
| Opponent sensors (2–4x) | "Eyes" that detect the other robot | <cite index="27-1">Infrared or ultrasonic sensors both work — infrared/modulated light sensors generally have faster response times</cite>. Mount facing outward, covering front and sides |
| Edge sensors (4x minimum) | "Eyes" that detect the white boundary line so you don't drive off | <cite index="29-1">Place a minimum of 2 front and 2 rear sensors at the corners of the chassis so contact from any direction is caught — 4 total is standard, some teams add 2 more on the sides for full coverage</cite> |

### STEP 5 — Programming: Giving Your Robot a Brain
**Beginner concept:** Nearly every winning sumo robot — regardless of country or era — runs the same basic decision loop, called a **state machine**: a simple "if this happens, do that" flow with only a few possible modes.

Here's the logic in plain pseudocode before you write real code:

```
SETUP:
  wait for start signal (whistle / start module)
  stay still for 5 seconds  ← rule 6.2, moving early = warning

LOOP forever:
  1. Check edge sensors FIRST, always, on every single cycle
     → if any edge sensor detects the white line:
         stop, reverse briefly, turn away from that edge
         go back to step 1

  2. Check opponent sensors
     → if opponent detected:
         turn to face it, drive forward at full power (ATTACK)
     → if opponent NOT detected:
         rotate slowly in a search pattern (SEARCH)
         e.g. spin in place, or arc in a circle scanning outward

  3. repeat
```

<cite index="42-1">Some teams vary their start routine — for example turning 45° to one side before charging forward — specifically so an opponent can't pre-program a counter-attack against a predictable straight-line start.</cite> This is worth doing once your base logic works.

**Tuning tips from experienced builders:**
- <cite index="30-1">Calibrate edge sensor thresholds carefully — this is the single most common cause of accidentally driving off the arena.</cite>
- <cite index="26-1">If your reactions feel sluggish, your control loop code is likely too slow — simplify your logic and use interrupts for sensor reads rather than constantly polling in the main loop.</cite>
- Always check edge sensors *before* opponent sensors in your code, every single loop — a robot that's mid-attack but ignores the edge will drive itself out and lose instantly.

### STEP 6 — Testing & Practice
- Test on a surface as close to the real dohyo as possible — <cite index="29-1">different floor textures change traction dramatically, so borrow or replicate a sample of the black arena surface if you can.</cite>
- <cite index="29-1">Always bring two fully charged battery packs and 5+ spare fuses — motor stall current can blow fuses mid-event.</cite>
- <cite index="29-1">Weigh your robot before every single match — teams sometimes add last-minute ballast and accidentally go over the 3 kg limit.</cite>
- Run at least 20–30 full mock matches against a practice opponent (even a cardboard-weighted box on wheels) before competition day — most bugs only show up under real contact forces, not on a workbench.

---

## PART 4 — Competition Day Playbook

### 4.1 Team roles (per your rulebook)
- **2–3 members**, one designated **Team Leader** (talks to referees, runs team logistics)
- One **Team Supervisor**, locked in for the whole event — choose this person carefully, they can't be swapped later
- **Only one member may place/activate the robot per round** — decide in advance who that is and practice the placement + activation + step-away sequence so it's fast and clean

### 4.2 A warnings/violations checklist — don't lose the event to a rules mistake
| Avoid this | Why |
|---|---|
| Moving before 5 seconds after the whistle | Explicitly listed as a warning cause |
| Anyone approaching the robot/arena mid-round | Can cost you the round outright |
| A white or reflective front/blade | Warning risk + possible referee rejection at inspection |
| Loose screws/parts that could detach | 1 warning per detached part |
| Any last-second component swap after inspection | Can mean disqualification |
| Arriving late | More than 1 minute late forfeits the round; late twice in a row can forfeit the whole match |

Remember: **6 total warnings = automatic disqualification**, and if a tiebreaker is ever needed, "fewest warnings" is literally the first tiebreak criterion in Section 9. Clean play isn't just good sportsmanship here — it's a direct scoring advantage.

### 4.3 Referee & sportsmanship notes
- Treat the referee's calls as final in the moment — the rulebook gives them wide discretion (stopping/suspending rounds, judging what counts as "disruption," etc.)
- The tiebreak criteria (Section 9) explicitly reward **robot design/engineering quality** and **consistent, deliberate, non-random movement** — so a robot that visibly "knows what it's doing" (not just spinning randomly) is scored better even outside of pure wins.

---

## PART 5 — The Winning Formula (cheat-sheet summary)

1. **Weight-budget everything** — every gram of your 3 kg should do a job; finish under-weight and add ballast low and centered.
2. **Low, wide, centered chassis** beats tall and narrow, every time.
3. **Torque over top speed** — you're fighting at point-blank range in a 1.5 m ring, not racing.
4. **Edge sensors always win the priority check** in your code — check them before anything else, every loop.
5. **Never use a white or reflective front.**
6. **Use the UNO Q's dual-brain design as your edge** — reliable real-time IR-based logic first, camera/AI vision as your stretch goal.
7. **Practice your start routine and vary it** — predictability loses to teams who scout you.
8. **Zero warnings is a real strategic goal**, not just good manners — it's your tiebreaker insurance.

---

## PART 6 — Suggested Learning Roadmap (if you're starting from scratch)

| Week | Focus | Outcome |
|---|---|---|
| 1 | Rulebook mastery + design sketch + weight budget | A drawn/CAD concept and parts list |
| 2 | Chassis build + motor/wheel mounting | A rolling, driveable (manually wired) base |
| 3 | Arduino UNO Q basics — blink an LED, read a sensor, drive a motor via code | Comfort with the dev environment |
| 4 | Wire up opponent + edge sensors, calibrate thresholds | Reliable sensor readings on the real arena colors |
| 5 | Write and test the search → attack → edge-avoid state machine | A robot that survives on its own for a full round |
| 6 | Practice matches, tune motor speeds/turn angles, weigh & finalize | Competition-ready robot |
| 7+ | Stretch goal: camera-based opponent detection on the MPU side | Extra edge over IR-only competitors |

---

*This guide is based on your official SumoX-26 rulebook plus current (2026) research on world sumo robot competitions, engineering practices, and the Arduino UNO Q platform. Ask anytime you want to go deeper on a specific part — motor math, wiring diagrams, or actual starter code — and we'll build it out from wherever you are right now.*
