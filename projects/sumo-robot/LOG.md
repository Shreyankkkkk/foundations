# Sumo-Robot LOG

Format: `date | what changed | why | evidence`. Newest at the bottom. Add backfilled entries in date order.
Path map (folders renamed 2026-10-06; entries below may use the old names): `Strategy/` = `firmware/strategy/`; `tests/Code/` = `firmware/tests/`; `tests/Design/` = `design/parametric/`; `Design/1_Design`, `Design/2_Design` = `design/cad-v1`, `design/cad-v2`; `Details/markdown/` = `docs/specs/`; `Details/pdfs/` = `docs/rulebook/` (scans moved to `notes/scans/`); `Notes/` = `notes/`.

## Dated entries (from file metadata and the repo)

2026-09-24 | scanned handwritten pages | design/calibration notes | notes/scans/2026-09-24-scan.pdf
2026-09-25 | scanned notes + 6 design photos; first sensor calibration sketches | design v2 body + GP2Y0A21 calibration | notes/scans/2026-09-25-scan.pdf, design/cad-v2/, firmware/tests/
2026-09-26 | parametric CAD for front wedge and main deck | wedge/deck geometry from code | design/parametric/front_wedge_PARAMETRIC_SOURCE.py, main_deck_PARAMETRIC_SOURCE.py
2026-09-30 | scanned notes | TODO describe | notes/scans/2026-09-30-scan.pdf
2026-10-0? (last day before the event) | created v2.2, v2.3, v2.4 and renamed all versions from N_strategy to vX.Y | final strategy iterations | firmware/strategy/v2.2_Strategy ... v2.4_Strategy
2026-10-04 | competition: match 1 skipped (wiring not done); match 2 stalemate, won coin flip; match 3 stalemate, lost coin flip, eliminated | wiring never finished; robot too low for opponent sensors to detect; v2.4 and motion constants never tested | projects/sumo-robot/STATE.md
2026-10-04 | set up MCP logging for the repo (AI-CONTEXT.md, STATE.md, LOG.md) | cut tokens per chat, keep proof of work | AI-CONTEXT.md
2026-10-06 | backfilled this log from 33 chat summaries (18 from account 1, 15 from account 2); extended STATE.md constants; wrote Retrospective.md; added chat index | prove the work, build the project template | notes/chat-summaries/INDEX.md, Retrospective.md
2026-10-06 | restructured the repo: folders lowercased and regrouped (learning/, projects/, certificates/, journal/, _local/); Sumo split into docs/, design/, firmware/, notes/ | professional learning-log layout | README.md, AI-CONTEXT.md

## Backfill: chat history

The summaries carry no dates. Order below is inferred from cross-references between chats (file names, version numbers, "prior agent" mentions) and the dated anchors above. Confirm real dates from the chat sidebar and fill `notes/chat-summaries/INDEX.md`; then move these lines up into the dated section.
ID = `A1-nn` / `A2-nn`: chat nn in the account-1 / account-2 summary file. Raw summaries: `Notes/chat-summaries/`. Chat naming differs from repo folders: chat v3 = Hybrid = v1.2, chat v4 = Strategy_Ram = v1.3, chat v5 = map-based = v2.0/v2.1.

### Phase 1: planning, learning, parts
A1-10 | picked Baiter R1, Flanker R2, R3 repeats winner (strategy v3 spec); rejected omni wheels, circular wedge, forklift | strategy drives chassis; mirror-wedge matchup is a coin flip | chat only
A1-10 | chose Titan 12V 200RPM + JS5230 52x30 wheels (10.35 kg-cm = 1.015 N·m, 4.1 A stall); torque exceeds traction at every wheel size | motor/wheel check | chat only
A1-10 | Wokwi exercises 01-04 (blink, button-LED, multi-sensor priority, toggle edge-detect) + notes/references | user new to C | Notes/arduino-fundamentals.md
A1-09 | Python-to-C table, blink sketch, fundamentals-first reset; edge sensors digital, TCRT5000 on 3.3 V | pin-map-first was too advanced | chat only (blink never run)
A1-01 | parts pass: opponent sensors 6 to 4, PCF8574 dropped (12 pins fit), chassis 3 mm Al CNC at university, jumpers 20 cm, 8x 10k dividers, lever nuts PTC-213 x11 + PCT-212 x2 | pin budget, 20x20 footprint | Details/materials.xlsx
A1-01 | sourcing: only 100RPM in stock, later back to 200RPM; wrongly cut "owned" parts (-869 AED), corrected: only UNO Q owned, total 1068.89 AED (200RPM) | ownership was assumed | chat only
A1-01 | flagged KCD4 switch rated for AC only | ~8.2 A DC stall load | OPEN
A2-01 | researched strategies; edge-check first, Search/Attack/Edge state machine; rejected continuous spin (no source); 3 selectable strategies, build order core, S3, S1, S2 | proven architecture + fallback | sumo_robot_strategies.md v1
A2-01 | flagged 18650 cells bought instead of 3S LiPo | invoice vs wiring plan | OPEN
A2-02 | read materials.xlsx, strategies md, rulebook; fetched SimpleSumo, Mini-Sumo, project-pineapple; ideas only (servo-based, licence conflict) | find patterns | none
A1-02 | same repos + materials.xlsx; UNO Q pinout (3.3 V logic, PWM 3,5,6,9,10,11); rulebook limits saved | prep before code | none (coding at 0%)

### Phase 2: wiring and architecture
A1-08 | wiring doc v1 to v3: "all 3.3 V" claim corrected (A0/A1 not 5 V tolerant); 10k/10k dividers on GP2Y, board on VIN, BTS7960 VCC 5 V, TCRT5000 3.3 V; pins D2-D9 motors, D10-D13 edge, A0-A3 opponent; added 8x 10k | two team reviews | sumox26_wiring.md v3
A1-03 | wiring v3 made authoritative over two other pin maps; wrote Hardware.h, Motors.h/.cpp; start button A4; layered files | 3 conflicting pin maps | Hardware.h, Motors.*
A1-07 | 3 strategies cut to 2 toggleable; wrote Final_Strategies.md, Sensors, Robot, signed drive(), ROUND_BUTTON A5; STL measured 200.01 mm (zero margin) | clean split | SumoX-26_Final_Strategies.md, 12 files
A1-07 | reviewed rewritten codebase + Claude Code port; kept v2 (hammer, push correction, start palette); attackDeadline latch for GP2Y blind zone; fixed link error, search never running, side override halved by Kp | regressions found | Robot.*, Strategy_1/2

### Phase 3: Hybrid firmware (v3) audits
A2-03 | 28-item audit; rewrote 11 files + MotorBench.ino + SensorCalibration.ino; 12-bit ADC, per-sensor offset/gain, median-of-5 time-gated, edge confirm, reversal brake, attack latch; fixed inverted reposition() and recovery pivots | second-AI patches verified, not blindly accepted | tests/Code/
A2-04 | merged S1+S2 into Strategy_Hybrid (S1 P-control + side-override debounce); deleted Strategy_2; stop gate in loop(); START/ROUND polled in blocking loops; hammerAttack split; dead code removed | C1-C5 audit findings | Strategy_Hybrid.*, Robot.*, main.ino
A1-04 | Motors rewrite; reset-on-OFF; primeOpponentSensors; edge recovery rewritten (mirrored arcs, side edge, fallback); side override only when front clear | stale buffers, wrong-side arcs | Robot.*, Strategy_Hybrid.*
A1-04 | timed switch filter rejected ("no deliberate amount of time") | user requirement; later replaced by 100 ms filter in A1-05 | none
A1-05 | 100 ms glitch filter (arming stays raw), setMotorsEnabled gate, PUSH_READING = SENSOR_PEAK x85/100 + static_asserts, ATTACK_COMMIT 500 to 300, side-override watchdog 800/700 ms, SENSOR_DEBUG mode; host stub + 7 scenario tests; rulebook check | blip caused 5.2 s freeze | 7 files delivered
A2-05 | removed lostTargetLoops OR-clause, added randomSeed, ROUND_BUTTON rising edge, sideOverride==0 gate on hammer | false hammer, round switch dead after match 1 | main.ino, Robot.cpp, Strategy_1.cpp
A1-06 | firmware ported to JS; HTML simulator (ring 150 cm, STL 200x200x73.2 mm, live sliders, dark mode); strategy advice only (symmetric head-on push stalemates) | show teammates behaviour | sumox26-simulator.html
A1-11 | STL audit: original non-manifold, 23 bodies, ~65 deg wedge; designed 2-part printable chassis (wedge 32 deg, 186x192 mm); user rejected it | print/fit failures | Final_Sumo_Robot.stl; wedge.py, deck.py not kept

### Phase 4: sensor bring-up and calibration
A2-06 | review: compiles; 8x 10k dividers on A0-A3 only; DIST_THRESHOLD 400 to 100, SENSOR_PEAK 960 to 220 (divider halves scale); staged switches (START standby, START+ROUND = round); diagonal opening step; firmware report | divider, brown-line concern | SumoX-26_Firmware_Report.md; Robot.h/.cpp, .ino delivered (applied unconfirmed)
A1-12 | sensor audit, no code: calibration procedure, 7-step priority list; pin 13 is both LED and back-right edge sensor | find must-fix items before competition | none
A1-13 | code audit by reading; wrote GP2Y0A21_Calibration/_Manual and TCRT5000 bench sketches; calibration moved to a plain Uno | sensors never calibrated | tests/Code/
A2-07 | GP2Y manual vs auto logger; TCRT5000 board is a 3-pin module with no pot; pin-2 test: nothing LOW, anything HIGH; unit may be damaged | sensor bring-up | tests/Code/
A2-08 | GP2Y log flat 330-360 with dropouts (loose wiring or ripple); wrote live test, logger v2, fit_calibration.py, sensor_bench_monitor.ino (median of 7) | unusable data | tests/Code/
A1-14 | TCRT5000 output is binary; usable window 1.5-3 cm (white HIGH, black LOW); brown untested; 10k/10k divider on TCRT OUT for UNO Q | height sweep | tests/Code/

### Phase 5: v4 Ram strategy (v1.3)
A2-09 | v3 frozen, v4 started: 3 opponent + 2 edge sensors; Search, Triage, Align, Commit; bounded +-100 deg sweep with dead-reckoned heading; drive-until-clear edge recovery; engaged latch; no switch pins in code | drop calibration-heavy logic | Strategy_Ram.* (v1.3_Strategy)
A1-15 | compile fixes (identifier case, orphan block, guards); removed pinMode on PWM pins (UNO Q); align flip limit, REACQUIRE, side-steered COMMIT, goSearch(), trackHeading | compile errors, oscillation bait | Strategy_Ram.*, Robot.cpp
A2-10 | engagedSinceMs reset every frame so ENGAGE_MAX never fired, fixed; bench: GP2Y no object <100, 0-10 cm 250-350, 10 cm 600-700; DETECT 150 / ENGAGE 480 recommended | code review + bench data | Strategy_Ram.cpp, Hardware.h
A2-11 | keep 12 files in one sketch folder named like the main .ino, do not merge | Arduino build rules | none
A2-12 | judge Q&A walkthroughs; DETECT 100 / ENGAGE 465 (idle reads 80-90); TURN_RATE 0.18 to 0.216; sweep 100 to 180 deg | calibration + Q&A prep | Hardware.h
A2-13 | removed ENGAGE_MAX_MS; creep latch; TURN_RATE 0.312; trackHeading scaled by PWM; forceCommit; recoverFromEdge rewritten; continuous x,y tracking rejected | live-push cut-off, one-shot creep bugs | Strategy_Ram.*, Robot.cpp, Hardware.h

### Phase 6: v5 map-based and v2.x (v2.0 to v2.4)
A1-16 | v4.2: recover/commit use "detected" not "engaged" (contact reads 250-350 < engage 465); v5 designed (ram at t=5 s, center-anchored map, 6 files, non-blocking recovery); 4 patches given; zip sent to team | retreating mid-push | v2.0/v2.1 (5_Strategy)
A2-14 | edge-abort, double-edge escape, centerSustainedBand, strategyEngage, swingClear, EDGE_SUPPRESSION off, COMMIT_VOID_PWM; T0-T5 measurement sketches; BlindSumo.ino (ram, reverse, turn 10 deg) | v5 hardening; team's blind idea | Strategy.cpp, Robot.cpp, T0-T5 .ino, BlindSumo.ino
A2-15 | found no start button (5 s counted from boot, ~4.85 s guessed); debounced start press, release-first; spinCommand sign swap (ALIGN turned away, RETURN deadlock); host sim; v2.2, v2.4 compiled on stub; IDE errors (analogWriteResolution, arduino:zephyr platform) | rule 6.2 compliance | v2.2_Strategy, v2.4_Strategy
A1-17 | v2.2 to v2.4: median ADC oversample N=7, release hysteresis, MIN_MOVE_PWM 90, slew limiter, latching rocker on A4 (3.3 V + 10k pull-down), Hardware.h/Formulas.h split, thresholds x0.5 for dividers, edge polarity auto-detect, rear-clear guard, Calibrate.ino, PC sim + fuzz | UBEC ripple, no time to calibrate | v2.3, v2.4, CodeGuide.md
A1-18 | BlindSumo: sensor-free timed ram, reverse, turn 10 deg, 15 s power-on delay, no switch | team fallback idea | single .ino; not used at the event

TODO: confirm real dates for the 33 chats (INDEX.md); fix the "2026-10-0?" line.
