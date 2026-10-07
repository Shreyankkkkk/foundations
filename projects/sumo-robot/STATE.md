# Sumo-Robot STATE (SumoX-26, TechBots League Dubai)

Status: finished. Eliminated after the first 3 matches (2026-10-04). Retrospective: `Retrospective.md`.
Controller: Arduino UNO Q (sole controller, fully autonomous, max 20x20 cm / 3 kg).
Code that was on the board: `firmware/strategy/v2.4_Strategy/`.
Full history: `LOG.md`. Raw per-chat summaries: `notes/chat-summaries/`.

## Result
| Match | Outcome |
|---|---|
| 1 | skipped, wiring not finished |
| 2 | stalemate, won coin flip (wiring still not finished) |
| 3 | stalemate, lost coin flip, eliminated (wiring still not finished) |

Causes: (1) the whole competition day went on wiring and it was never completed; (2) the robot sat so low that opponents' sensors could not detect it.
v2.4 and every motion constant below were never tested on the real robot (no time).

## Version map (folders in `firmware/strategy/`; name used in chats)
| Folder | Chat name | What it is |
|---|---|---|
| v1.0_Strategy | 1_strategy | first strategy split: Strategy_1/2 files only |
| v1.1_Strategy | 2_strategy | first full modular sketch: Hardware, Motors, Robot, Sensors + Strategy_1/2 |
| v1.2_Strategy | 3_strategy ("v3") | Hybrid: Strategy 1 P-control + side-override debounce, hammer attack, start palette |
| v1.3_Strategy | 4_strategy ("v4") | Strategy_Ram: 3 opponent + 2 edge sensors, Search/Align/Commit, dead-reckoned heading |
| v2.0_Strategy, v2.1_Strategy | 5_strategy ("v5") | map-based: ram at t=5 s, center-anchored position map, 6 files |
| v2.2 / v2.3 / v2.4 | created on the last day | v2.2 = start-flow + spin-sign fixes; v2.3 = ADC median, slew limiter, re-arm; v2.4 = Hardware.h/Formulas.h split, auto edge polarity |

## Hardware (as built)
- 3x GP2Y0A21 opponent sensors (front, left/right at 45 degrees), through 10k/10k dividers (A0-A2)
- 2x TCRT5000 edge sensors (front D10, back D11), mounting height band ~1.5-3 cm
- 2x BTS7960 drivers, 2x Titan 12V 200 RPM motors, coaxial as built (initial plan was staggered), 2x JS5230 52x30 mm wheels + 2 idlers
- UBEC steps 5V down to 3.3V for the board; sensors on 5V; KCD4 main switch cuts battery; start trigger = latching rocker on A4
- Black matte PETG detachable wedge, very low ground clearance
- Power as bought per chats: 35 A fuse, one 2200 uF cap on the motor bus, 470 uF on the UBEC 5 V rail, 8x 10k resistors for dividers
- Battery: 3S nominal 11.1 V (3 x 3.7), full 12.6 V (3 x 4.2); cell type never settled in the summaries (18650 holder vs LiPo): UNCONFIRMED
- KCD4 switch DC rating never confirmed (listing gives 16 A / 250 VAC only; load ~8.2 A stall): UNCONFIRMED
- Files: `docs/specs/final_wiring.md` (materials.xlsx is not in the repo)

## Rulebook limits used in code and design
| Rule | Value | Where used |
|---|---|---|
| 4.1 / 4.2 | 3 kg, 20x20 cm, no height limit | chassis, ROBOT_* geometry |
| 4.4 | UNO Q sole controller, fully autonomous | whole design |
| 4.5 | front must not be white | chassis finish |
| 4.7 / 6.11 | no changes after inspection | flash final build; detachable wedge needs referee OK |
| 5.1 / 5.2 | ring 150 cm, 3 cm white border, 2 brown lines 2 cm x <=20 cm, 10 cm from center | arena constants, start pose |
| 6.2 / 7.3 | 5 s stationary or warning; 3 warnings lose a round, 6 = DQ | START_COUNTDOWN_MS |
| 6.6B | no touching the robot mid-round | switch OFF only after round ends |
| 6.6D | referee stops a stuck robot after 30 s | STALEMATE_HARD_CEILING_MS |
| 9 | 25-30 cm safety zone; tie-break prefers non-random movement | SAFETY_ZONE_MIN_CM, random opening move removed in v5 |

## Constants (value | calculation or measurement | source | status)
Rulebook
| Constant | Value | Calculation / measurement | Source | Status |
|---|---|---|---|---|
| ARENA_RADIUS_CM | 72 | (150 - 2x3)/2 | rulebook s5.1, Formulas.h | derived |
| ARENA_OUT_RADIUS_CM | 75 | 150/2 | rulebook s5.1 | derived |
| START_COUNTDOWN_MS | 5050 | 5000 mandatory delay + 50 margin | rulebook, Hardware.h | derived |

Robot geometry (ruler)
| Constant | Value | Calculation / measurement | Source | Status |
|---|---|---|---|---|
| WEDGE_TO_FRONT_SENSOR_CM | 4.7 | ruler | Hardware.h | measured |
| REAR_TO_BACK_SENSOR_CM | 3.6 | ruler | Hardware.h | measured |
| ROBOT_LENGTH_CM / ROBOT_WIDTH_CM | 20 / 20 | marked MEASURE in code; equals rule maximum | Hardware.h | UNCONFIRMED |
| REAR_TO_AXLE_CM | 3.6 | marked MEASURE; equals rear-to-back-sensor value. One axle line is valid (motors coaxial) | Hardware.h | value UNCONFIRMED |
| ROBOT_L_F_CM | 16.4 | 20 - 3.6 | Formulas.h | derived |
| START_POSE_RADIUS_CM | 27.4 | 11 + 16.4 | Formulas.h | derived |
| ROBOT_R_SWING_CM | 19.21 | max(hypot(10,16.4), hypot(10,3.6)) | Formulas.h | derived |
| OPEN_SWEEP_HALF_ANGLE_DEG | 35.5 | atan(20/(2x11+16.4)) + 8 deg aim error = 27.5 + 8 | Formulas.h | derived |
| EDGE_SENSOR_FRONT_OFFSET_CM | 11.7 | L_F - 4.7 = 16.4 - 4.7 | Formulas.h | derived |
| Chassis STL (first design) | 200.006 x 200.008 x 73.17 mm | trimesh bounding box; zero margin to the 200 mm cap | Final_Sumo_Robot.stl | measured (design file, not final print) |

Drivetrain and mass (derived from vendor specs; none measured on the robot)
| Constant | Value | Calculation | Source | Status |
|---|---|---|---|---|
| Wheel circumference | 163.4 mm | pi x 52 mm | JS5230 listing | derived |
| Wheel speed | 3.333 rev/s | 200 RPM / 60 | Titan listing | derived (vendor RPM) |
| Free-run top speed | 54.45 cm/s | 163.4 mm x 3.333 | A1-10, A1-16 | derived upper bound |
| Top speed at 12.6 V | 57.2 cm/s | 54.45 x 12.6/12 | A1-16 | derived (linear-in-voltage assumed) |
| Stall torque per motor | 1.015 N·m | 10.35 kg-cm x 0.0980665 | vendor | derived (vendor figure) |
| Stall current | 4.1 A each, ~8.2 A both | vendor; 2 x 4.1 | vendor | vendor / derived |
| Max wheel force | 78 N | 2.03 N·m / 0.026 m | A1-10 | derived (stall, upper bound) |
| Friction force at 3 kg, mu 0.6 | 17.7 N | 0.6 x 3 x 9.81 | A1-17 | derived from PLACEHOLDER mu |
| Free-run turn rate | 312 deg/s | omega = 2v/L = 2 x 0.5445 / 0.20 = 5.445 rad/s | A2-13 | derived upper bound (L = 20 cm ASSUMED) |
| Turn rate, 194 mm track variant | 321.7 deg/s | 2 x 0.5445 / 0.194 | A2-12 | derived (track from user figure) |
| Turn rate at PWM p | 312 x p/255 | 0.1835 deg/ms at PWM 150, 0.208 at 170 | A2-13 | derived (linear PWM scaling ASSUMED) |
| Non-chassis mass | ~939 g | 48+180+25+360+60+100+30+30+8+10+50+18+20 | A1-01 | PLACEHOLDER (mostly typical estimates; no weigh-in recorded) |

Electrical (from chats)
| Constant | Value | Calculation / measurement | Source | Status |
|---|---|---|---|---|
| UNO Q VIN range | 7-24 V | Arduino docs | docs | vendor |
| Divider ratio | 0.5 | 9.9k/(9.9k+9.9k), multimeter | Hardware.h | measured |
| GP2Y peak through divider | ~480 counts | 3.1 V x 0.5 = 1.55 V; 1.55/3.3 x 1023 | A1-17 | derived (3.1 V peak ASSUMED, datasheet not fetched) |
| START_SWITCH_ON_ADC | 775 | 2.5 V/3.3 V x 1023 | Hardware.h | derived |
| START_SWITCH_THRESHOLD_ADC | 387 | 775/2 | Hardware.h | derived |
| TCRT5000 HIGH through 10k/10k | 2.5 V | 5 x 10k/(10k+10k) | A1-14 | derived |

Sensors
| Constant | Value | Calculation / measurement | Source | Status |
|---|---|---|---|---|
| SENSOR_DIVIDER_RATIO | 0.5 | 9.9k/(9.9k+9.9k), multimeter | Hardware.h | measured |
| BENCH_NO_OBJECT_MAX | 100 | bench ADC, no divider | Hardware.h | measured (pre-divider) |
| BENCH contact / peak bands | 250-350 / 600-700 | bench ADC, no divider | Hardware.h | measured (pre-divider) |
| TCRT5000 height window | 1.5-3 cm | white HIGH (~1015), black LOW (0); below 1.5 cm both HIGH; above 3 cm both LOW | A1-14, A2-10 | measured (lit room; brown never tested on the real arena) |
| WEAK_THRESHOLD | 75 | 100 x 0.5 x 1.5 | Formulas.h | derived |
| CONTACT band | 125-175 | bench x 0.5 | Formulas.h | derived, never measured through dividers |
| PEAK band | 300-350 | bench x 0.5 | Formulas.h | derived, never measured through dividers |
| ADC_NOISE_SIGMA | 20 | none | Hardware.h | PLACEHOLDER |
| SENSOR_SAMPLE_INTERVAL_MS | 15 | ceil((38.3 - 9.6)/2), datasheet refresh 38.3 +/- 9.6 ms | Formulas.h | derived |
| WEAK_CONFIRM_SAMPLES | 4 | ceil((38.3 + 9.6)/15) | Formulas.h | derived |
| ADC_OVERSAMPLE_N | 7 | (20 / (50/6))^2 = 5.76, rounded up to odd | A1-17 | derived from PLACEHOLDER sigma |

Motion (never tested on the robot)
| Constant | Value | Needed measurement | Status |
|---|---|---|---|
| DRIVE_SPEED_MAX_CMS | 45 | distance / time at PWM 255 | PLACEHOLDER |
| SPIN_RATE_CW/CCW_DEGS | 120 | stopwatch spin test | PLACEHOLDER |
| STOP_DISTANCE_CM | 16 | slide after cutting power at full speed | PLACEHOLDER |
| FRICTION_MU | 0.6 | spring-scale pull / weight | PLACEHOLDER |
| MIN_MOVE_PWM | 90 | lowest PWM that moves loaded robot | PLACEHOLDER |
| DRIVE_DECEL_CMS2 | 63.3 | v^2/(2d) = 45^2/(2x16) | derived from placeholders |
| COMMIT_SOFT_START_S | 0.0765 | v/(mu x g) = 45/(0.6 x 981) | derived from placeholders |
| MOTOR_SLEW_PWM_PER_MS | 3.34 | 255/(0.0765 x 1000) | derived from placeholders |

Values that changed between versions (check before trusting any old number)
| Constant | History | Why it moved |
|---|---|---|
| START_COUNTDOWN_MS | 5200 (v3 Hybrid) > 5000 (v4) > 4850 (early v5, boot-based) > 5050 (v2.2+) | 5 s rule + margin; boot-based timing broke the rule |
| ADC resolution | 10-bit > 12-bit (one rewrite) > 10-bit | divider loss vs verified behaviour; never confirmed on UNO Q |
| Opponent divider | 10k/10k (0.5) > 10k/22k (0.688) discussed > 9.9k/9.9k measured | installed value was unknown for a while |
| DIST_THRESHOLD | 400 > 100 | divider halves the ADC scale |
| SENSOR_PEAK | 960 > 220 | same; the 220 arithmetic was flagged as possibly ~2x low (recomputed 387-480), not resolved |
| DETECT / ENGAGE (v4) | 150/550 > 150/480 > 100/465 | bench bands 250-350 and 600-700; idle reads 80-90 |
| TURN_RATE_DEG_PER_MS | 0.18 > 0.216 (no calc shown) > 0.312 (derived above) | 0.312 is a free-run upper bound |
| Arena diameter in BlindSumo | 100 cm (placeholder) vs 150 cm rulebook | conflicting statements, never settled; blind sketch constants unreliable |

## Strategy summary (v2.4)
5 ms loop: stop switch > edge sensors > strategy > motors > map update. States: OPEN_SWEEP, SEARCH, ALIGN, COMMIT, RETURN, STALEMATE_BREAK. Dead-reckoning map with uncertainty limits speed so the robot can stop before the rim. Detail: `firmware/strategy/CodeGuide.md` (OUTDATED). Fallbacks that existed: v4 (Strategy_Ram, v1.3) and BlindSumo (sensor-free, timed).

## Lessons
- Very low ground clearance meant opponents' sensors could not see the robot. Check ground clearance against typical opponent sensor height at design time.
- Wiring is the critical path: finish and test it days before the event, not on the day.
- Untested constants make the strategy unverifiable: bench-test motion constants early.
- Full lessons by stage: `Retrospective.md`.

## Where things are
- Strategy code: `firmware/strategy/v1.0_Strategy` ... `v2.4_Strategy`
- Tests/calibration sketches: `firmware/tests/` (GP2Y0A21, TCRT5000, Calibrate, Motor_Sensor, robot_testing)
- CAD: `design/` (`cad-v1`, `cad-v2`, `parametric`)
- Docs: `docs/specs/`, rulebook PDF in `docs/rulebook/`
- Notes: `notes/` (scans in `notes/scans/`); chat summaries and index: `notes/chat-summaries/`

## TODO
- Clean up `v2.4_Strategy` (unnecessary lines; user estimates 300+). Keep the original, work on a copy.
- Update or archive `firmware/strategy/CodeGuide.md` to match the clean-up
- Confirm real dates for the 33 backfilled chats (`notes/chat-summaries/INDEX.md`), then move them into dated LOG lines
