# SumoX-26 Team Brief — paste this into your own Claude chat

We're building an autonomous sumo robot for the **Dubai Techbots League SumoX-26** (Besomi Academy × Arduino × Qualcomm × Canadian University Dubai). Use the block below to get Claude up to speed instantly, then jump to your role's starter prompt.

---

## STEP 1 — Paste this shared context into a new Claude chat first

```
I'm on a team building an autonomous sumo robot for the Dubai Techbots League
SumoX-26 competition (organized by Besomi Academy, with Arduino and Qualcomm
as sponsors). Here are the key rules:

- Weight limit: 3 kg max
- Footprint: 20cm x 20cm max at start (no height limit, and the robot CAN
  change shape/size after movement begins, as long as all parts stay attached
  to the main body)
- Controller: MUST use the Arduino UNO Q as the primary/only microcontroller
  (no other microcontrollers allowed). It's a dual-brain board: an STM32
  microcontroller for real-time motor/sensor control, plus a Qualcomm
  QRB2210 Linux processor capable of running a camera and AI models.
- The robot must be 100% autonomous - remote control is strictly banned
- Arena: circular wood, 1.5m diameter, white 3cm frame, black surface, two
  brown 20cm center lines
- Round: max 3 minutes, robot must stay stationary for 5 seconds after
  activation before moving
- Match = best of 2 rounds (3rd if tied 1-1)
- Rule violations to avoid: front of the robot (blade/wedge) must NOT be
  white or any color that could interfere with sensor readings; no magnets,
  suction, vacuum wheels, or adhesives to grip the arena; no liquids, gases,
  powders, or projectiles; 3 warnings in one round = automatic round loss;
  6 total warnings = disqualification; any robot part detaching = 1 warning
  per part

My team already has a full build playbook covering: sumo robot world
championship research (All Japan Robot-Sumo Tournament history and past
winners), mechanical design (low center of gravity, wedge front, motor/gear
selection), electronics (motor driver, battery, opponent + edge sensors),
and a search -> attack -> edge-avoid programming logic. I'm now going deeper
on one specific part of the build. Please treat me as a beginner in this
specific area and build up my understanding step by step as we go, the same
way you'd teach someone new to the topic, then increase depth based on my
follow-up questions.
```

---

## STEP 2 — Add your role's starter prompt on top of that

Pick whichever matches what you're focusing on. If your team hasn't split roles yet, use the General one.

### 🔧 Mechanical / chassis lead
```
My focus is the mechanical build: chassis, wedge front, wheels, motor
mounting, and weight distribution. Help me design this step by step -
starting with material choice (aluminum vs polycarbonate vs HDPE), then
chassis shape and wedge geometry, then wheel/motor mounting, then a full
weight budget that lands at or just under 3kg with room for ballast.
Ask me what tools/materials I actually have access to before recommending
specifics.
```

### ⚡ Electronics / sensors lead
```
My focus is the electronics: the Arduino UNO Q setup, motor driver
selection, battery choice, and the opponent-detection + edge-detection
sensors. Walk me through setting up the UNO Q from scratch first (App Lab,
the MCU vs MPU split, running a first test sketch), then help me pick and
wire a motor driver and sensors that fit a 3kg autonomous sumo robot. Explain
each component's job before we pick parts.
```

### 💻 Programming / code lead
```
My focus is the code: the robot's decision logic (search -> attack ->
edge-avoid state machine) running on the Arduino UNO Q. Help me build this
from scratch, starting with the simplest possible version (basic edge
avoidance + move forward), then layer in opponent detection, then attack
behavior, then tuning. If it's useful, also explain how I could eventually
use the UNO Q's camera/AI side for smarter opponent detection as a stretch
goal - but let's get the reliable IR-sensor version working first.
```

### 🧭 General / not yet specialized
```
I don't have a specific role locked in yet. Can you help me understand the
full build process end to end at a beginner level - mechanical, electronics,
and code - so I can see which part I'm most drawn to, then we go deep on
that one?
```

---

## Notes for whoever's coordinating

- Everyone should also upload the actual **Dubai Techbots League SumoX-26 Rulebook PDF** to their own chat if they have it, so their Claude has the full original wording, not just this summary.
- Since each teammate's chat is separate, decisions made in one chat won't automatically show up in another — plan for someone (probably the Team Leader) to consolidate what each person's chat produces into one shared doc or group chat before final assembly.
- If two teammates' chats land on conflicting recommendations (e.g. different motor torque suggestions), that's normal — bring both back to the group and decide together rather than assuming either Claude session has the full picture.
