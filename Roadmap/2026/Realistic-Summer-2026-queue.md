# The Queue: Aug 1 → Oct 3
### One thing at a time. No clock. Cross it off, move on.

This replaces the time-blocked version. That version was wrong for you — you've already proven your actual method works: Python basics to completion, *then* Git/GitHub to completion, LLM tinkering only as a burnout release valve. This plan just extends that same method forward instead of fighting it with a schedule you'd abandon by Wednesday.

**The two exceptions that don't count as "another thing":**
- Trading (07:30–08:30-ish) — an established routine, not a study item, runs unchanged regardless of what's next in the queue
- Ordering sumo parts — a 10-minute errand you do *whenever*, ideally in the first few days, because shipping doesn't care what you're currently studying

Everything else follows the queue below. No overlap. No "let me also start Fusion 360 while I finish pandas."

---

## The Queue

### 1. Data Analysis — Kaggle (not freeCodeCamp)
Skip the Kaggle "Python" module — you already have that from freeCodeCamp. Go straight into:
- **Pandas** (Kaggle Learn)
- **Data Visualization** (Kaggle Learn)
- **Data Cleaning** (Kaggle Learn)

Then — and this matters more than the courses themselves, given how you actually like to work — pick one real dataset (a forex/market dataset, or your own trade log exported as CSV) and build **one self-directed project end to end**: load it, clean it, analyze it, visualize it, write it up. Not because a course told you to, but because that's the "10%-filled canvas" version of a data analysis project instead of five prescribed ones. It goes on GitHub with a README either way.

**Done when:** the three Kaggle tracks are finished and you have one original project committed, documented, and something you could explain line by line without looking at it.

---

### 2. Fusion 360 (Autodesk Design Academy)
Straight CAD learning, no robot decisions yet beyond what you've already locked in (Baiter+Flanker toggle, side sensor placement for ~270° coverage). Learn the tool.

**Done when:** you can model a basic chassis shape from scratch without tutorial hand-holding.

---

### 3. Sumo robot chassis design
Now apply Fusion 360 to your actual robot. Model the chassis around your sensor and strategy decisions. Finalize the Bill of Materials.

**Order the parts as soon as the BOM is locked — don't wait until this step is "done."** This is the errand exception above.

**Done when:** CAD model is final and parts are ordered.

---

### 4. Arduino C (Coursera — Introduction to Arduino)
Pure language/platform learning, no robot code yet. Loops, pin I/O, sensor reading logic — the foundation your university C course hasn't taught you yet.

**Done when:** you're comfortable writing and debugging basic Arduino sketches without copying examples.

---

### 5. Physical build
Assembly and wiring. Chassis, motors, side sensors, wheels. This is hands-on and will surface problems your CAD couldn't predict — that's normal, not a failure of Step 3.

**Done when:** the robot moves under manual/basic motor control code.

---

### 6. Strategy code
Baiter/Flanker state machine, the pre-round toggle, sensor logic feeding into behavior. This is where everything from Steps 3–5 comes together.

**Done when:** the robot reacts correctly to edge detection and opponent presence in isolation (not yet battle-tested).

---

### 7. Integration testing + iteration
Full battle tests against a teammate's bot or a mock opponent. Fix what breaks. This step will eat more time than you expect — budget for it, don't rush past it.

**Done when:** you've run real test matches and the robot performs consistently enough that you'd trust it on Oct 3.

---

## The one hard constraint: Oct 3 doesn't move

Everything above is sequential by choice — but Steps 2–7 (the entire robot) need to be *finished*, not just started, before Oct 3, and Sept 24 brings university back into your day. That means:

- **Data Analysis (Step 1) needs to wrap by roughly mid-August.** Not because a clock says so, but because every day past that is a day subtracted from a robot build that has zero flexibility on its deadline.
- If you're deep in Step 1 past that point and it's going well, that's fine — just know you're borrowing time from Step 7, which is the step most likely to reveal problems you need days (not hours) to fix.
- If Step 1 is dragging because Kaggle's pacing doesn't suit you, that's a signal to timebox it loosely in your head — not "2 hours a day," but "if this is still open in three weeks, finish the current module and move to the robot regardless."

Nobody's stopping you from moving fast through Data Analysis. You've already shown you can — Python basics in under two weeks, Git/GitHub in about a week. If this queue moves at that pace, you'll hit the robot with plenty of runway. The only failure mode worth watching for is Step 1 quietly expanding because it's comfortable and the robot is unfamiliar and a little intimidating.

---

## Everything else (SQL, Stat 110, linear algebra, finance papers, Monte Carlo dissection, Notion automation, HFT prototype)

Not in the queue at all right now. They live in the same place LLM tinkering does — genuine free time, burnout-relief time, whenever you're between queue items and want a change of pace without starting the *next* queue item early. Once Step 7 is done and Oct 3 has passed, they go back into the queue in whatever order makes sense then.
