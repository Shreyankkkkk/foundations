# AMD Hackathon ACT III STATE

AMD Developer Hackathon: ACT III (lablab.ai x AMD). Hybrid: online build 2026-10-12 to 2026-10-18, optional on-site 10-17/18 in Italy (travel not covered).
Status: kickoff passed (2026-10-12 19:00 GST), build window open. AMD sign-up done (new account). lablab enrollment and Discord join: confirmed 2026-10-11 19:00 (stated by Shreyank 2026-10-12; GST assumed).
Goal: priority 1 = experience and learning; priority 2 = winning. Team: decided 2026-10-09 meeting; 6 members (2 backend incl. Shreyank, 2 frontend, 1 marketing, 1 repo), which is the maximum allowed. Roles in Decisions.
Idea (current, per Team Playbook 2026-10-10): Procedure Drift Finder, see project section below. SUPERSEDED (inferred from the Playbook, confirm with team): the earlier 3D walkthrough idea "Google Earth for the inside of a building".
Old idea (initial, from team meeting): "Google Earth for the inside of a building". Owner sends static images; AI converts them into a 3D simulation to walk through remotely. Uses named: hotels; factories where machinery is dangerous so students can view remotely. Not validated, see Risks.
Note: the earlier Dec 1 date belonged to a different event (AMD AI Academy Challenge, see `projects/amd-hackathon/`). It does not apply here.

## Rules and constraints (rule | value | source)
| Rule | Value | Source |
|---|---|---|
| Registration | Closes at kickoff: 2026-10-12 15:00 UTC; approval needs AMD AI Developer Program membership plus lablab enrollment and Discord | live page, event page |
| Submission deadline | 2026-10-18 15:00 UTC; judging starts then | live page |
| Team size | 1 to 6; teammates findable on dashboard or Discord | event page |
| Challenge | Pick one of 4 business tracks (Intelligent Industry, Health and Wellbeing, Reinvent Commerce, Create a New Kind of Experience), or the Evolus partner track | event page |
| AMD requirement | A meaningful part of the workload must run on AMD (Developer Cloud, Instinct, ROCm, Ryzen AI, Radeon) AND be part of the working product shown to judges | event page |
| Models and tools | Own choice of compatible models, frameworks and tools | event page |
| Submit | Title, short and long description, track, tech tags, cover image, demo video, slide deck, public GitHub repo, demo platform, application URL, working prototype | event page |
| Judging | Application of Technology, Presentation, Business Value, Originality | event page |
| Track 3 rule | Do not use an LLM as the only forecasting method; explain how predictions are calculated | event page |
| Track 2 rule | No autonomous diagnosis or treatment advice; show uncertainty, human review, handling of sensitive data | event page |
| Track 4 rule | Show the experience changing for at least 2 audiences or inputs; state cost per experience and who pays | event page |
| Evolus track | Free Evolus workspace via event code shared at kickoff (valid to 2026-10-31, up to 6 members, 50,000 credits); main agent must use an open model on own vLLM endpoint on AMD Developer Cloud; at least 2 Evolus building blocks; drive Evolus through its APIs; containerized app, public repo, runnable README | event page |
| Vibe Generation special prize | AirPods 5 for each member of the best solution; judged on Hybrid, Becreatives, Vibe Generation | event page |
| Prize pool | $12,000+; split per track not shown on the page | event page |
| Credits | $100 AMD Developer Cloud credits for new ADP members | event page |
| Originality and licence | Submissions must be original and MIT-compliant | event page |
| Prize payout | Up to 90 days | event page |
| Secrets | Never commit API keys; use environment variables | event page (Evolus track) |
| Submission limits | Title clear and descriptive (max 50 chars per guidelines article); short description max 255 chars; long description min 100 words covering problem, solution, audience, unique features; tags; cover image PNG/JPG 16:9; video MP4 max 5 min (under 300 MB per guidelines article); slides PDF; public GitHub repo; demo platform; application URL | rule book, submission guide, guidelines article |
| Demo platform | Rule book names Streamlit, Replit or Vercel. Evolus track needs a containerized app. Which hosts are accepted for a GPU-backed app is not stated | rule book, event page; UNVERIFIED |
| Repo visibility | Private repo means judges cannot fully review; lower score. Judges check the repo; commits spread across the event window are a stated positive signal (lablab guide, not a rule) | submission guide, how-to-win guide |
| Late submission | Manual submission only for 6 h after the deadline, only with a valid reason and prior approval from organizers or mentors | rule book |
| Conduct | Plagiarism, gaming voting, unauthorized automation, tampering or fraud: removal or disqualification. Not following submission guidelines: lower score or exclusion | rule book |
| IBM Bob report | Submission guide asks for an exported IBM Bob report. Not mentioned on the ACT III event page, so likely carried over from another event; check the getting-started guide | submission guide; UNVERIFIED for ACT III |
| Team approval | Each member needs AMD AI Developer Program membership + lablab enrollment + Discord before kickoff; assumed per person, UNVERIFIED | event page |
| Not covered by the rule book | Eligibility (age, country), what may be prepared before kickoff, AI-assisted coding, third-party code and data, licensing detail beyond MIT. Getting-started guide still unread | rule book; open |

## Constants (name | value | calculation | source | status)
| Name | Value | Calculation | Source | Status |
|---|---|---|---|---|
| days_to_kickoff | 0 | kickoff passed 2026-10-12 19:00 GST (was 3 on 2026-10-09, 4 on 2026-10-08) | calendar | DERIVED |
| kickoff_gst | 19:00 GST on 2026-10-12 | 15:00 UTC + 4 h (GST = UTC+4) | live page | DERIVED |
| submission_close_gst | 19:00 GST on 2026-10-18 | 15:00 UTC + 4 h | live page | DERIVED |
| build_window_h | 144 h | 6 days x 24 h (kickoff to submission close) | live page | DERIVED (calendar hours, not working hours) |
| manual_submission_close_gst | 01:00 GST on 2026-10-19 | 15:00 UTC on 10-18 + 6 h = 21:00 UTC; + 4 h GST | rule book, live page | DERIVED (needs prior approval; not a plan) |
| registered_2026-10-08 | 5,007 | read from live page | live dashboard | MEASURED |
| teams_forming_2026-10-08 | 871 | read from live page | live dashboard | MEASURED |
| hours_available | ? | ask Shreyank (uni schedule) | - | PLACEHOLDER |
| time_split | 20% research / 60% build / 20% demo, README, submission, of hours_available | WORKFLOW.md rule of thumb | WORKFLOW.md | ASSUMED until hours_available is known |
| freeze_date | date? | set once hours_available and track are known | - | PLACEHOLDER |
| credit_cost_per_gpu_hour | ? | measure on AMD Developer Cloud | - | PLACEHOLDER |
| credit_hours_total | ? | $100 divided by credit_cost_per_gpu_hour | page, measurement | PLACEHOLDER |

## Decisions (choice | reason | rejected | status)
| Choice | Reason | Rejected | Status |
|---|---|---|---|
| Enroll before kickoff | Registration closes at 2026-10-12 15:00 UTC | Enrolling late | Recommended, pending Shreyank |
| Team vs solo | Team (decided at team meeting, 2026-10-09 report by Shreyank) | Solo | DECIDED |
| Idea | Procedure Drift Finder (notes vs SOPs, drift flags with verified quotes) per Team Playbook | Indoor 3D walkthrough from owner images (superseded, inferred) | CURRENT per Playbook; team confirmation of the switch not seen |
| Roles | 6 members. Backend: Shreyank + 1 teammate. Frontend: 2 teammates. Marketing: 1 teammate (contact other teams, sponsors). Repo: 1 teammate sets up the repo, all are contributors, work comes as pull requests he reviews and merges. Corrected 2026-10-10: marketing is a separate person, not one of the frontend two | - | AGREED, stated by Shreyank |
| Track | Playbook states Track 1 Intelligent Industry; the one-or-more-tracks question (F1/U4) still open. Older note: the 3D idea fit Create a New Kind of Experience (needs 2 audiences/inputs and cost per experience) or Intelligent Industry (factory case needs realistic industrial data and an alert/action). Event page says "one or more tracks" but submit form says "Selected challenge"; plan for one until answered (primary-research F1/U4) | - | OPEN |
| Repo and publishing | Public repo `https://github.com/Shreyankkkkk/procedure-drift-finder` owned by Shreyank. Code is built in Foundations (`projects/amd-hackathon-act-iii/backend/`; Claude can only edit inside Foundations), copied with `robocopy <backend> backend /E /XD __pycache__ .pytest_cache /XF *.pyc` into the local clone `C:\Users\Shreyank\Documents\Development\procedure-drift-finder`, then git add, commit, push straight to main (no pull requests). Teammates send files in the WhatsApp group; Shreyank places them in the right folder and commits. Per Shreyank the repo teammate does not use git. Supersedes the Roles row's repo-person and pull-request arrangement. UPDATE 2026-10-16: frontend/ is published the same way (robocopy frontend into the clone with the same /XD and /XF flags, commit, push); the teammate's front-end zips are placed into Foundations first | Foundations as the hackathon repo (mixes projects, teammates cannot contribute); moving the project out and back; pull requests to himself (no review value) | DECIDED 2026-10-15, stated by Shreyank; visibility and MIT licence set as advised, not verified |

## Open items / next actions
1. DONE 2026-10-11: lablab enrollment and Discord join confirmed (Shreyank).
2. Answer the remaining setup questions (hours per day per member, online only); fills `hours_available`. Team is decided.
3. Read the getting-started guide in a browser (fetcher cannot render lablab guide pages reliably); settle the "Not covered by the rule book" row.
4. Check whether ACT III counts toward AI Academy XP (see `projects/amd-hackathon/`).
5. Primary research queue (checklist done 2026-10-09 in `docs/research/primary-research-checklist.md`: findings F1-F12, unknowns U1-U12, constants C1-C9; measurements and answers still pending): AMD Developer Cloud GPU type, $/h, credit hours, vLLM serve test; Docker/Linux on Shreyank's machine; schedule and mentor hours in GST; track requirements vs skills.
6. Secondary research queue (not started): past lablab/AMD winners in tracks of interest, vLLM-on-ROCm docs, Evolus quickstart, track datasets. Tag each finding SOURCED or RECALLED.
7. SUPERSEDED: the backend code was written 2026-10-15/16 under the Backend plan, before the primary research was logged.
8. Idea validation (primary research, not started): what input quality the image-to-3D step needs (single photos vs many overlapping photos), whether it runs on AMD GPU and at what time/cost per building, existing indoor-tour products to compare against.

9. DONE 2026-10-12: Playbook, Front-End Guide and data contract text pasted by Shreyank and folded in (project section below). Open: which builder (A or B) Shreyank is; who is data lead.
10. Send Claude the AMD machine facts (price per hour, OS, Python version, ROCm and Docker preinstalled or not); creating the 1xMI300X machine is Shreyank's step. Needed for the runbook and the vLLM smoke test.
11. Share the repo link in the team group and ask teammates to send files via WhatsApp (not confirmed done).
12. DONE 2026-10-16: all backend code stages and tests written (see Backend plan, Status 2026-10-16). Left: AMD machine facts, GPU runs per backend/docs/amd-runbook.md, judge timeout and retry.
13. Second backend teammate: benchmark.py and tests/test_benchmark.py were already written by Claude on 2026-10-16, so the remaining suggested start is hand-written notes and reviewing wrong flags and missed drifts (see backend/README.md); role not confirmed.
14. hours_available is still unknown; Shreyank to give hours per day.
15. Housekeeping (2026-10-16): delete the old skeleton docstring at the top of backend/src/config.py; re-run pytest, python -m src.evaluation.benchmark --fake and python scripts/check_data.py and confirm results; push backend/ to the team repo (the repo's earlier src/__init__.py was the broken version if it was pushed).
16. Front end v3 received 2026-10-16 (see Frontend section). Next: run it (streamlit run src/app.py, python -m pytest from frontend/), then work through the alignment list in that section. Direction agreed by Shreyank: the backend adapts to the front end; the front end changes only if necessary.
17. Evolus partner track: Shreyank pasted the track text 2026-10-16 (requirements in the Rules table). NOT DECIDED whether we enter it. Backend plan 2026-10-13 says Evolus excluded; the front end still has an "AMD and Evolus" page with Evolus fields in amd.json. Needs a team decision, then either build the Evolus part (2 building blocks, REST API calls, open model on our vLLM endpoint) or remove the Evolus text and fields from the front end.
18. Submission checklist (stated by Shreyank 2026-10-16): project title, short and long descriptions, selected challenge, technology tags, working prototype, cover image, demo video, pitch presentation, clear explanation of the problem and intended user, plus the GitHub repo.

## Research folder summary (docs/research/, read 2026-10-12)
- `opportunity-research-report.md` (2026-10-10, analyst report; was Opportunity_Research_Report.md): covers the four tracks and shortlists 8 areas (1.2, 1.3, 2.1, 2.2, 3.1, 3.2, 3.3, 4.1). Provisional analyst-judgment ranking: 2.1 discharge comprehension 21; 3.2 SMB forecasting and 2.2 language barriers 20; 1.2 defect detection 19; 3.3, 1.3, 3.1 at 18; 4.1 audio description 17. States it does not choose a project. No SOP/procedure-drift area is analysed in it.
- AMD path facts it records (SOURCED to vLLM/AMD docs): pre-built vLLM ROCm wheels need Python 3.12 only; MI300-class GPUs supported; AMD Developer Cloud offers 1x MI300X (192 GB) or 8x MI300X. Still unverified there: instance availability and quota in event week, VLM-specific throughput, speech/TTS on ROCm.
- `primary-research-checklist.md` (2026-10-09; was research_1.md): findings F1-F12, unknowns U1-U12, constants C1-C9 (C1-C9 still unmeasured). U11 (enrollment/Discord) is now resolved; F12 (days_to_kickoff) corrected above.
- `brief.md`: reduced version only, see its own warning.
- Playbook PDF, Front-End Guide PDF and data contract .docx (moved 2026-10-14 to `docs/guides/`): AI could not read the files; Shreyank pasted their text 2026-10-12 and it is folded into the project section below.

## Project: Procedure Drift Finder (Team Playbook and Front-End Guide 2026-10-10, data contract; text pasted 2026-10-12)
- What: Track 1 Intelligent Industry. User: plant safety/process manager. Reads the notes a plant already writes (handover, near-miss, maintenance) against its SOPs, finds drift, shows the exact quote as proof. Data is synthetic and labelled so.
- Pipeline: load SOP steps (F1) > load notes (F2) > matcher picks top 3 candidate steps per note (F3) > judge model returns step, drift type, exact quote, confidence (F4) > plain code checks the quote appears word for word in the note, else the flag is dropped (F5) > human approve/reject (F6, front end) > SOP-fix draft for outdated/unclear flags (F11) > benchmark vs 25 planted drifts (F8).
- Drift types: skipped_step, reordered_steps, workaround_substitution, sop_outdated_or_impractical, sop_unclear.
- Rules: flag only what a note says (silence is not evidence); report on steps and shifts, never people; human decision on every flag; not a safety control; no keys or endpoints in the repo.
- Roles: Builder A (back end 1): AMD GPU, vLLM, F3-F5, F11, F12, F15. Builder B (back end 2): aggregation, benchmark, F7 data, F12 workflow. Data lead (flex): SOPs, notes, answer key, planted drifts (critical path). Which builder Shreyank is: assumed Builder A (2026-10-13 plan); confirmation with the backend teammate pending.
- Interface (data contract): backend delivers JSON files read by the Streamlit front end; front end writes data/decisions.json. flags: flag_id, sop_id, step_id, note_id, date, shift, drift_type, quote, confidence (0-1), status (pending/approved/rejected), suggested_fix (text or null). sop: sop_id, step_id, title, text. notes: note_id, date, shift, source (handover/near-miss/maintenance), text. benchmark: precision, recall, quote_verified_rate, notes_per_minute, matcher_model, judge_model, gpu, false_alarms (list). Front end builds on fake data, swaps to real output 2026-10-15; do not change the format without asking.
- Test data plan (Playbook targets): 3-5 SOPs (8-15 steps each), 25 planted drifts, about 200 notes (some drift, some clean, some traps), a different model family writes the notes than the one that judges, teammates hand-write about 30, answer key lists which note has which drift.
- Schedule/gates: 10-12 test AMD GPU with vLLM and 2 models, Evolus workspace, repo; 10-13 first pipeline on 10 notes, evening gate: drop Evolus if it cannot call our endpoint; 10-14 quote verifier, all notes, test container; 10-15 real data to front end, clean-machine container test; 10-16 benchmark, freeze features; 10-17 record demo, submit early; 10-18 buffer, confirm deadline.
- Never cut: F5, F8 and answer key, AMD proof, container. Cut order: stretch > F15 > F11 > F12 > trend charts. Prize priority: core + AMD proof + benchmark, then Evolus, then Google.
- Design rule: one function judge_note can call either Evolus or our vLLM endpoint directly.
- NotebookLM summary conflicts with the Playbook: Dec 1 deadline is wrong (other event); FastAPI endpoints, vector DB and a Drift Score are not in the Playbook or the data contract.
- Playbook's Discord questions still open: tracks, Google rules, Vibe Generation tech requirements, exposing vLLM to Evolus, synthetic data acceptable, exact deadline.

## Backend plan (agreed 2026-10-13 21:00 GST; Claude writes and tests the code, Shreyank runs only what needs his accounts and the AMD machine)
- Status 2026-10-15: DONE: synthetic data (3 SOPs, 32 steps; 200 notes = 25 drift + 30 trap + 145 clean; answer key; check_data.py passed when built; re-run after the folder move not confirmed), backend regrouped into src/ (stages, models, evaluation), scripts/, data/, tests/, docs/, backend/README.md written as a folder map for teammates, public repo created with the first backend push. (The NOT DONE part of this 2026-10-15 status is superseded by the 2026-10-16 status in the next bullet.)
- Status 2026-10-16: DONE (code written by Claude, pasted and run by Shreyank): config, loader, matcher, judge, quote_check, fake_model, pipeline, benchmark, package __init__ files, pytest.ini, requirements.txt, tests for every stage, runbook draft (machine facts still PLACEHOLDER). Confirmed by Shreyank: 94 of 95 tests passed once (the one failing pipeline test was fixed afterwards); fake run over 200 notes: 29 flags kept, 47 dropped by the quote check (pretend model, numbers say nothing about the real one). Quote check ignores capitals, spacing, curly quotes and punctuation at word edges; punctuation inside a word must match. Benchmark counts a flag correct only if note, SOP, step and drift type all match; a second flag for the same drift is a false alarm; benchmark.json has exactly the contract fields, extra detail goes to benchmark_details.json. NOT CONFIRMED: full pytest run after the benchmark and __init__ fixes; benchmark --fake run; check_data.py re-run after the folder move. NOT DONE: AMD machine facts (open item 10), vLLM smoke test and GPU runs 1 to 4, request timeout and retry in judge.py (placeholders), SOP-fix drafts, README section that runs. Plan is about one day behind and the freeze date 10-16 is today; if no GPU today, the hosted-model fallback is due.
- Deliverables: sop.json, notes.json, flags.json, benchmark.json (filename for the accuracy-test results) in the contract format; saved copy in data/demo/ for Demo mode; README section that runs; numbers sheet for video and slides.
- Pipeline: read SOP steps and notes > matcher picks top 3 steps per note by shared words (plain Python, no second model) > judge model replies in fixed format > plain code checks the quote is in the note (same words, same order, ignoring capitals and extra spaces) and drops the flag if not > write flags.json (status pending).
- Decisions: one open instruct model of about 7-8 billion parameters on vLLM (memory about 7-8e9 x 2 bytes = 14-16 GB vs 192 GB on MI300X; model names to be checked on the model page); temperature 0; Evolus excluded; test data generated by Claude (different family from the judge), 3 SOPs of 8-15 steps, 25 planted drifts, about 200 notes (drift, clean, trap), answer key; data lead's hand-written notes added if delivered before 2026-10-15 noon. Every constant (retry limit, matcher size, fix-round cap) is measured or calculated and logged here.
- Who: Claude = all code, test data, fixes from returned output, runbook, backend facts for the submission. Shreyank = log into AMD Developer Cloud, claim credits, create 1xMI300X machine, run commands and paste output back, move backend/ into the team repo, coordinate with teammates. Front end reads the JSON files; marketing does submission texts, video, slides.
- Schedule (GST): 10-13 night: Shreyank sends price per hour, OS, Python version, ROCm/Docker status, repo link; Claude builds data and code and tests with a pretend model. 10-14: vLLM smoke test, 10-note run, fixes, real-format sample to front end (slips Playbook's 10-13 pipeline test by one day). 10-15: timed full run, notes per minute and cost per 1,000 notes computed from measured times, outputs into shared data/ and data/demo/, backend/ into team repo, front end swaps to real data, SOP-fix drafts (first thing cut). 10-16: accuracy test, wrong flags and missed drifts reviewed, prompt wording changes only, final run, numbers sheet to marketing, AMD proof screen capture, FREEZE. 10-17: README tested in a clean folder, backend facts for descriptions and pitch, demo recording and submission. 10-18: buffer only; deadline 19:00 GST (15:00 UTC).
- GPU runs (only runs Shreyank does): 1 smoke test (1 note), 2 ten notes, 3 full run timed, 4 final run after fixes, 5 recording. Fix-round cap = floor(minutes from first accuracy run to freeze / minutes per full run), calculated after run 3. Credit hours = 100 / price per hour; shut the machine down when idle.
- Fallbacks: vLLM not starting by 10-14 noon: run the model on the AMD machine with Hugging Face transformers; no GPU by 10-14 evening: develop against any hosted model with the same address style and ask mentors on Discord, final run must still be on AMD; behind: cut SOP-fix drafts first, never cut the quote check, accuracy test, AMD proof or the front end's container; late data lead: Claude's data stands in.
- After the event: Claude writes a walkthrough in learning/ explaining each backend file line by line, with exercises that rebuild each stage; learning order = JSON and dicts, functions across files, environment variables, terminal and tmux, API calls with requests, prompts for fixed JSON replies, try/except, string search, tests, timing, counting, Git.

## Frontend (Streamlit app, `frontend/`; built by the two frontend teammates, received as zips, placed by Shreyank)
- Status 2026-10-16: version 3 received and placed in `frontend/`; Shreyank had asked the teammate to follow the backend-style folder layout (src/, scripts/, data/, tests/, docs/) from the Foundations copy pushed to GitHub. Teammate is not confirmed finished. v3 not yet run by Shreyank or Claude; what follows is read from git status and code, not executed.
- New or changed in v3 (git status): new `src/ingest.py` (turns uploaded Word, PDF, text, CSV or JSON into sop.json and notes.json), `src/quote.py` (finds a quote in its note with the backend's tolerant rule and returns its position for highlighting), `src/views/upload.py` (Add Documents page: upload, edit, check required fields as in backend loader.py, export), `scripts/sync_backend_data.py` (copies backend sop/notes and flags/benchmark into frontend/data; `--source fake|real|demo`; leaves amd.json alone; backs up decisions.json), `tests/test_ingest.py`, `pytest.ini`, `docs/sample_uploads/` (synthetic sample files), requirements gained pypdf and python-docx. Modified: app.py, analytics.py, review.py, README.md, .dockerignore, .gitignore, data/benchmark.json, flags.json, notes.json, sop.json.
- Closed since the 2026-10-16 backend-vs-frontend compatibility review (by code reading): quote highlighting now uses the backend's rule (quote.py); `false_alarms` accepts flag ids or the backend's objects with reasons; null benchmark values show as a dash with a pretend-model caption.
- Still open after v3 (by code reading): page text still says "Two models, one GPU" and that matching runs on the GPU, but the matcher is plain Python (only the judge uses the GPU); "AMD and Evolus" page and Evolus fields remain; amd.json is still invented (cost_per_1000_notes 0.42, evolus_api_calls 128) and the backend produces no amd.json; Live mode needs an HTTP endpoint the backend does not have; decisions are keyed by flag_id and the backend renumbers flag ids each run (sync script backs decisions up for this reason); `quote_verified_rate` means kept/proposed in the backend but the Overview treats it as the share of shown flags verified; SOP labels show only sop_id and step (no SOP name in the contract); trend ("is it growing?") may be flat on the planted data (inferred from note ids, unchecked).
- DATA WARNING: `frontend/data/` currently holds the backend's pretend-model run (precision 0.276, recall 0.32, judge_model and gpu null, notes_per_minute 185175). These numbers say nothing about the real model and must never reach the demo, slides or submission. Replace with the real run via `python scripts/sync_backend_data.py --source real` after the GPU runs.
- Alignment work list (agreed 2026-10-16 in chat, produced by Claude; status NOT STARTED unless stated; items 1 to 3 partly overtaken by v3):
  1. benchmark.json: keep false_alarms as objects (front end now reads both) or switch to ids; always fill the fields on a real run; require --gpu; decide the quote_verified_rate definition.
  2. Write the exact matching text from the note as the flag's quote (less urgent now that quote.py is tolerant).
  3. Stable flag ids built from note, SOP, step and drift type.
  4. Produce amd.json from run_stats.json, price per hour and real Evolus call counts (front end requires it).
  5. Evolus integration if the team enters the track (item 17); keep the 10-13 gate rule (drop it if Evolus cannot call our endpoint).
  6. Live mode: small read-only server for /sop /notes /flags /benchmark /amd so AMD is visibly part of the working product.
  7. Publish script: validate against the contract, refuse pretend-model output, build amd.json, copy to frontend/data and backend/data/demo (frontend/scripts/sync_backend_data.py already copies but does not validate or refuse fake output); replace the invented numbers.
  8. Fix the matcher wording in the front end (the one front-end change counted as necessary).
  9. SOP-fix drafts (suggested_fix) for outdated and unclear flags; first thing cut if behind.
  10. Check the planted-drift timing for the heat strip; adjust build_data.py only if it stays honest synthetic data.
  11. AMD machine facts, vLLM smoke test, GPU runs 1 to 4, notes per minute, cost per 1,000 notes, rocm-smi and vLLM screenshots.
  12. Container and README that run on a clean machine; replace judge timeout and retry placeholders with measured values.
  13. Repo cleanup: delete old skeleton docstrings at the top of loader.py and matcher.py; re-run pytest, benchmark --fake and check_data.py; write the agreed contract into backend/README.md and docs/.
  14. Submission assets from real numbers only (marketing teammate).

## Risks (3D idea, superseded; all ASSUMED until researched)
- Turning a few static images into a believable 3D space is hard; single images give invented geometry. Demo must not claim measured accuracy it cannot show. RECALLED, verify.
- AMD must be a real part of the shown product (prize gate): the generation step is the natural place; needs a vLLM/ROCm or equivalent path tested on Developer Cloud.
- Existing indoor 3D tour products exist; originality has to come from the image-to-simulation step and the factory training use case.
- One reviewer merging all pull requests is a bottleneck during a 144 h window; agree review turnaround.

## Where things are
- `docs/research/brief.md`: REDUCED brief (event page and live page only); the full version was overwritten 2026-10-08, rule-book facts live in the Rules table above
- `docs/research/primary-research-checklist.md`: primary research checklist (findings F1-F12, unknowns U1-U12, constants C1-C9, judge view, track fit); earlier called research_1.md and docs/primary-research.md
- `docs/research/opportunity-research-report.md`: analyst report, 8 shortlisted areas, provisional ranking; earlier called Opportunity_Research_Report.md
- `docs/guides/`: `team-playbook.pdf`, `frontend-duo-guide.pdf`, `data-contract.docx` (unread by AI, text pasted 2026-10-12 and folded in above; moved here from docs/research/ on 2026-10-14 and renamed)
- `docs/notes/`: `notes_0.md`, `notes_1.md` not read
- `backend/`: `src/` (config.py, pipeline.py; `stages/` = loader, matcher, judge, quote_check; `models/` = fake_model; `evaluation/` = benchmark), `scripts/` (build_data.py generates the data, check_data.py checks it), `data/` (sop.json, notes.json, answer_key.json; `demo/` = saved demo copy), `output/` (run results, git-ignored), `tests/`, `docs/amd-runbook.md`, `README.md`, `requirements.txt`; see `backend/README.md`
- `https://github.com/Shreyankkkkk/procedure-drift-finder`: the public hackathon repo; `backend/` is published into it from here (see the Repo and publishing decision); no STATE, LOG or docs go there
- `frontend/`: Streamlit app from the frontend teammates (version 3 placed 2026-10-16): `src/` (app, config, theme, data_loader, ingest, quote; `views/` = analytics, review, upload), `scripts/` (make_fake_data.py, sync_backend_data.py), `data/`, `tests/`, `docs/sample_uploads/`, Dockerfile, README.md; see `frontend/README.md` and the Frontend section above
- `LOG.md`: dated changes
