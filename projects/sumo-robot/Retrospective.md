# Sumo-Robot Retrospective (SumoX-26)

Outcome: eliminated after 3 matches (1 skipped, 2 stalemates). Code on the board: v2.4, untested on the robot. Two causes: wiring never finished; robot too low for opponent sensors to see. Source: 33 chat summaries (2 accounts), see `LOG.md`.
This was the first project run through the AI-context setup (`AI-CONTEXT.md`, STATE/LOG per project), so the lessons below are also the first draft of a reusable project template.

## Stage 1: primary research (own measurements, rulebook, hardware facts)
Worked
- TCRT5000 height sweep found the only usable band (1.5-3 cm, white HIGH / black LOW).
- GP2Y0A21 bench bands (<100 none, 250-350 at 0-10 cm, 600-700 at 10 cm) exposed the near-field dip, which changed the design (detect-level latch instead of engage-level).
- Rulebook cross-checks turned up the rules that drive code: 5 s stationary, 30 s stuck rule, 25-30 cm safety zone, no changes after inspection, front not white.
- STL parse showed 200.006 mm (zero margin) before inspection.
Did not work
- Calibration started late and was partial: first GP2Y logs were unusable (flat 330-360 with dropouts, likely loose wiring); TCRT5000 units varied 0.5-4 cm in range, one possibly damaged, no trim pot.
- Thresholds were measured without dividers, then scaled x0.5 (derived, never measured through the dividers).
- Brown start lines never tested on the real arena (later sidestepped with a box lid).
- Motion constants (speed, spin rate, stop distance, mu, min PWM) never measured; T0-T5 sketches were written but not run on the robot.
- No weigh-in, battery/motor weights estimated; arena size stated as 100 cm in one sketch vs 150 cm in the rulebook.
- Ground clearance never compared with opponent sensor height: the robot was undetectable.
Template rule: list every constant the strategy needs, measure each on the real hardware before writing strategy code, and mark the rest `PLACEHOLDER`.

## Stage 2: secondary research (repos, papers, forums, other AIs)
Worked
- Repos gave usable patterns (rolling average, stuck counter, test-sketch-per-subsystem order); architecture consensus: Search / Attack / Edge-avoid, edge check first.
- A thesis comparison (tornado search worst, tracking best) backed the bounded-sweep + align design.
- UNO Q docs caught real wiring risks: A0/A1 not 5 V tolerant, divider needed on GP2Y outputs.
- Forum finding: `pinMode(OUTPUT)` on a PWM pin breaks `analogWrite` on UNO Q.
Did not work
- Several "research" claims were recalled, not looked up (GP2Y fold-back distance, datasheet voltages, TCRT5000 polarity).
- An AI research report cited Uno R3 docs for UNO Q; a boot time of ~43 s stayed unconfirmed; a quoted "IR-absorbing brown" rule clause was not in the SumoX-26 rulebook.
- Reviewers contradicted each other (reposition direction inverted twice, pivot sign rules, spin polarity), costing several chats.
- Some repos blocked by robots rules; one licence conflict (CC BY-NC-SA vs GPL-3.0), so ideas only.
Template rule: tag each research line SOURCED or RECALLED; verify RECALLED items on the target hardware before they become constants. Treat a second AI's review as a claim to verify, not a patch to apply.

## Stage 3: implementation (code, build, test)
Worked
- Layered files (Hardware / Motors / Sensors / Robot / Strategy) and version folders; later Hardware.h + Formulas.h so every number is traceable.
- Host-side stubs, scenario tests, PC sim and fuzz runs caught real bugs: switch blip freezing the robot for 5.2 s, inverted spin polarity (ALIGN turned away, RETURN deadlock), stale buffers, dead start switch after match 1.
- `static_assert`s on thresholds; software-only mitigation for UBEC ripple (median oversampling, release hysteresis).
- Logic kept on the MCU; fallbacks kept (v4, BlindSumo).
Did not work
- Strategy rewritten four times (Hybrid, Ram, map-based, Blind); each rewrite reset calibration and moved effort away from wiring.
- Piecemeal patches confused the user; in roughly ten chats a patch was "given, application unconfirmed". Full-file replacements worked better.
- Spec docs drifted from the code (twice flagged).
- Not compiled on the real UNO Q core in the summaries; last-day IDE errors (`analogWriteResolution`, `arduino:zephyr` platform).
- A redesigned printable chassis was rejected; the final robot was too low for opponent detection.
- Wiring was left to the competition day and never finished.
Template rule: freeze the hardware build date first; no new strategy rewrite after the freeze; confirm each patch is applied (diff against the repo) before the next review.

## Decision register (final choices; superseded ones in brackets)
| Decision | Reason | Superseded / rejected |
|---|---|---|
| Edge check first, every loop | self-exit is a guaranteed loss | attack-before-edge (one repo) |
| Layered multi-file sketch, one folder, one .ino | Arduino compiles the folder | single merged .ino |
| Wiring v3 pin map D2-D13 / A0-A3, start on A4 | most reviewed, stable | 2 other pin maps |
| GP2Y on 5 V with 10k/10k divider; TCRT5000 on 3.3 V | A0/A1 not 5 V tolerant | direct connection |
| Median filter, not mean | spikes | mean [10-bit/12-bit ADC flip-flopped] |
| Detect-level (not engage-level) latch for contact | contact reads 250-350 < engage 465 | engage threshold |
| One strategy (Hybrid) over 3 selectable | no mode switch needed | S1/S2/S3 toggle |
| v5 center-anchored map, ram at t=5 s | known arena geometry | tornado search, 41-block grid |
| Latching rocker on A4 via 3.3 V + pull-down | 5 V must not reach the pin | push button, 1.2 s hold-to-stop |
| Hardware.h / Formulas.h split, thresholds x0.5 | traceable numbers; dividers halve ADC | single file |
| Keep v4 as fallback | safety | none |
| BlindSumo as last-resort fallback | sensors unreliable | not used at the event |

## Open at the end (never resolved)
- Brown-line behaviour of TCRT5000 on the real arena; edge polarity (auto-detect added, not verified).
- GP2Y thresholds through the dividers; SENSOR_PEAK 220 flagged as possibly ~2x low.
- All motion constants; motor direction and corner pin mapping; BTS7960 VCC and 3.3 V logic check.
- KCD4 DC rating; battery type; detachable wedge vs rule 4.7 (ask referee).
- Compile and run on the real UNO Q core; `STALEMATE_BREAK_ENABLED=false` edit not confirmed applied.

## Project template (draft, from this project)
1. Primary research: rulebook checklist; constants register (name, how to measure, status); bench sketches per sensor and for motion; weigh-in; opponent-view check (ground clearance, sensor heights).
2. Secondary research: sources tagged SOURCED / RECALLED; repo/licence notes; second-AI reviews logged as claims with a verification step.
3. Implementation: hardware freeze date; wiring tested end-to-end before strategy work; one version per day with a fallback; compile on the real target early; patches as full files or diffs checked against the repo; end-of-session LOG line and STATE update.
