# AMD Hackathon STATE

Lablab x AMD AI Academy Challenge. Status: day 0, not yet registered (confirm). Program: 2026-09-01 to 2026-12-01. Registration deadline (user-supplied): 2026-12-01 23:00 GST, UNVERIFIED (page states no separate cutoff or time zone, says "join at any point").
Goal: priority 1 = experience and learning; priority 2 = winning. Team: solo (rules are individual-only).

## Rules and constraints (rule | value | source)
| Rule | Value | Source |
|---|---|---|
| Participation | Individual only, no teams; each builder earns XP on own account | event page, FAQ |
| Sign-up | "Sign Up with AMD" (AMD AI Developer Program account) | event page |
| Schedule | Mini-challenge (MC) 1 opens 2026-09-01, MC2 2026-09-14, MC3 date?, MC4-6 "coming soon" | event page |
| MC1 | Onboarding: connect account, claim credits, finish an intro tutorial; no building | event page |
| MC2 | OCR: image in, text out (US plates, stop/speed/work-zone signs, adverse conditions) | brief PDF |
| MC3 | RAG: folder of mixed files, answer plus exact citation set; empty answer when absent | event page |
| MC4-6 | Web-scraping agent, multi-agent SWE solution, novel game via fine-tuning (per overview) | event page |
| Scoring MC2/MC3 | 10 hidden tests x 20 pts = 200; pass/fail per test; MC3 needs correct answer AND exact citation set | brief PDF, event page |
| Ranking | XP, ranks Bronze/Silver/Gold/Platinum/Legend; rank thresholds not published | event page |
| Cash prizes | Only first 3 to reach Legend: $2,500 / $1,500 / $1,000. Legend = XP + final challenge that unlocks near the end | event page |
| Certificate | AMD Certificate of Completion for those who complete the challenge | event page |
| Late join | Allowed; only activity after joining counts | event page, FAQ |
| New-member perks | $100 AMD Developer Cloud credits, 1 month DeepLearning.AI Pro (new sign-ups only) | event page |
| Hard gate: base image | Final stage FROM `rocm/pytorch:rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0`; no squash/flatten | brief PDF |
| Hard gate: size | 60 GiB uncompressed | brief PDF |
| Hard gate: VRAM | 1 to 48 GiB (+1% margin), sampled every 3 s, peak counts | brief PDF |
| Hard gate: time | Startup 10 min; 30 s per item; 10 min total run | brief PDF |
| Any gate failed | Score 0 for that submission | brief PDF |
| Code layout | `/app/app.py`, `/app/requirements.txt`, optional `/models`; output JSON in `/app/output/` | brief PDF |
| Submission | Public registry image, pullable without credentials. Do NOT commit the image reference to a public repo (this repo is public). No secrets in image or repo | brief PDF |
| Models | Any open-source model that runs on AMD GPU | brief PDF |
| GPU access | notebooks.amd.com/hackathon, 1 GPU per session, 48 GiB, 3 h/day quota (no rollover, idle time counts), first-come availability, ~25 GB persistent storage (path depends on pod URL: `/persistent` or `/workspace`) | brief PDF |
| pip trap | Installing torch-dependent packages can replace ROCm torch with CUDA torch; use `--no-deps`, verify `torch.__version__` ends in `+rocm` | event page |
| Office hours | 11:00-13:00 US Eastern | brief PDF |

## Constants (name | value | calculation or measurement | source | status)
| Name | Value | Calculation | Source | Status |
|---|---|---|---|---|
| days_left | 54 | 2026-12-01 minus 2026-10-08 = 23 (to Oct 31) + 30 (Nov) + 1 | calendar | DERIVED |
| gpu_hours_max | 162 h | 54 days x 3 h/day quota | days_left, brief PDF | DERIVED upper bound; availability first-come, not guaranteed |
| office_hours_gst | 19:00-21:00 until 2026-11-01, then 20:00-22:00 | 11:00 EDT = 15:00 UTC = 19:00 GST (UTC+4); after US clocks go back, 11:00 EST = 16:00 UTC = 20:00 GST | brief PDF | DERIVED |
| participants_2026-10-08 | 4,749 | read from live page | lablab live dashboard | MEASURED |
| top_xp_2026-10-08 | 5,250 (partial standings) | read from live page | lablab live dashboard | MEASURED |
| hours_per_week_available | ? | ask Shreyank | - | PLACEHOLDER |
| mc2_mc3_submission_deadlines | date? | not on the page; check Discord/dashboard | - | PLACEHOLDER |
| xp_threshold_silver_gold_platinum_legend | ? | not published; check dashboard | - | PLACEHOLDER |
| docker_linux_available | ? | ask Shreyank | - | PLACEHOLDER |

## Decisions (choice | reason | rejected | status)
| Choice | Reason | Rejected | Status |
|---|---|---|---|
| Solo | Rules are individual-only | Team of 6 | FINAL (by rules) |
| Register now, not near the deadline | Free; only post-join activity counts; learning XP available from day one; $100 credits for new sign-ups | Wait until Dec 1 | Recommended, pending Shreyank |
| Treat the cash prize as a bonus | First-3-to-Legend race among 4,749 participants, late start | Optimising for the prize | Recommended, pending Shreyank |

## Open items / next actions
1. Confirm sign-up status and answer the 3 questions in the chat.
2. Look-ups (see list in chat): per-challenge deadlines, Legend threshold, collaboration rules, Docker/Linux path, MC4-6 dates.
3. Do not start code until the look-ups are in this file.

## Where things are
- `docs/brief.md`: digest of the brief and the sources read
- `LOG.md`: dated changes
