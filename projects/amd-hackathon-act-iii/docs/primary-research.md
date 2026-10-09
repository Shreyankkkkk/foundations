# ACT III primary research

Date: 2026-10-09. Stage 1 per `projects/WORKFLOW.md`. Context: `docs/brief.md` (unchanged, main brief) + `STATE.md`. This file adds only what the brief and STATE do not already hold.
Tags: SOURCED = read in the source on the date above. RECALLED = from memory, must be verified. UNVERIFIED = a claim I could not open.
Re-read of event page 2026-10-09: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii (SOURCED). Getting-started guide link returned an empty shell to the fetcher (see U1).

## 1. Corrections and new findings vs brief/STATE
| # | Finding | Source | Action |
|---|---|---|---|
| F1 | Page says "Choose one or more tracks", but the submit list has a singular "Selected challenge". STATE row says "pick one". Conflict. | event page | Ask on Discord / rule book: can one project enter several tracks? Until answered, plan for one. |
| F2 | AMD is stated as required to be eligible for prizes (not only for scoring). A project with no AMD component in the demo wins nothing. | event page | Hard gate. Demo must show the AMD part running. |
| F3 | All four business tracks are marked "by partner: Vibe Generation". Vibe special prize has its own 3 criteria: Hybrid (strategy, quantified value, commercial attitude), Becreatives (technical execution, AI-tool orchestration, ability to ship), Vibe Generation (taste, originality, human+AI creative workflow). | event page | Treat as a second rubric on top of the 4 main criteria. |
| F4 | Page refers to Google prize ("one partner prize, or both partner prizes") but has no Google section, terms or tech list. | event page | UNVERIFIED that a Google prize exists with defined terms. Ask. |
| F5 | PwC Italy appears under partners with no stated role, prize or requirement. | event page | Ignore unless Discord says otherwise. |
| F6 | Evolus: the team reviews workspace config, connected model endpoint, building blocks used and API call counts. Using Evolus building blocks is checked by logs, not by your word. | event page | Anything claimed for the Evolus prize must be visible in the workspace. |
| F7 | Evolus credits: 50,000 per workspace, shared by up to 6 members, valid to 2026-10-31. Document reading, AI Tools and knowledge indexing run on Evolus and spend those credits. Credit cost per operation not stated. | event page | MEASURE (C7). Do not build a document-heavy demo before measuring. |
| F8 | Evolus: workspace agents may use any OpenAI-compatible provider, but the Evolus-track rule says the MAIN agent must use an open model on your own vLLM endpoint on AMD Developer Cloud. Read the track rule as the binding one. | event page | Confirm on Discord if the main agent can call a second non-AMD model for side tasks. |
| F9 | Evolus Studio download and developer quickstart (evolus.ai/developers) are "before kickoff"; event code only at kickoff. | event page | Check evolus.ai/developers before 10-12. |
| F10 | On-site: choose 1 of 3 cities (Rome, Milan, Imperia), approval required, selection criteria not stated, travel not covered. On-site hours given for 10-17 and 10-18. | event page | Decision depends on location; STATE open item 2. |
| F11 | Event schedule, mentor hours and workshop times: "To be announced". | event page | Cannot plan around them yet; recheck at kickoff. |
| F12 | STATE constant `days_to_kickoff` = 4 was computed on 2026-10-08. On 2026-10-09 it is 3 (10-12 minus 10-09). | calendar | DERIVED; update STATE when you next log. |

## 2. Unknowns I must confirm (U) and where
| # | Unknown | Where to find it | Blocks |
|---|---|---|---|
| U1 | Getting-started guide content (setup, what may be prepared before kickoff) | Open https://lablab.ai/getting-started-guide in a browser, paste it to me | prep plan |
| U2 | Eligibility (age, country), AI-assisted coding, third-party code/data, licence beyond "MIT-compliant" | Rule book https://lablab.ai/hackathon-rules (re-read for these 4 items only) and https://lablab.ai/terms-of-use#16-participation-terms | whether I may use AI and open code |
| U3 | Can work start before kickoff (repo, design, dataset prep)? | Rule book; else ask a mentor on Discord | commit-history rule below |
| U4 | Multiple tracks per project (F1) and multiple partner prizes | Discord organizers | track choice |
| U5 | AMD Developer Cloud: GPU type, price per hour, how $100 converts to hours, instance limits, idle shutdown, storage persistence | AMD Developer Cloud console after sign-in; AMD docs linked on the event page | C1 to C3 |
| U6 | Which model families run on the offered GPU with vLLM+ROCm and at what VRAM | vLLM and ROCm docs (secondary research) then a serve test on the real instance | model choice |
| U7 | Accepted demo hosting when the app depends on a GPU endpoint (rule book names Streamlit, Replit, Vercel) | Rule book; Discord | submission |
| U8 | Does the submission guide's "IBM Bob report" apply to ACT III? | Getting-started guide, Discord | submission checklist |
| U9 | Prize split per track | Prizes tab on the event page (not shown in the fetch) | track choice (low priority) |
| U10 | Is approval per member (ADP + lablab + Discord for each teammate)? | Dashboard after enrolling | team plan |
| U11 | Whether the lablab Enroll button and Discord join are done | Shreyank | registration closes 2026-10-12 15:00 UTC |
| U12 | Does ACT III count for AI Academy XP | `projects/amd-hackathon/` STATE, AMD AI Academy | only matters for goal priority 1 |

## 3. Constants to measure (all PLACEHOLDER until measured; each needs calculation + source)
| # | Name | How to measure | Needed for |
|---|---|---|---|
| C1 | credit_cost_per_gpu_hour | Read price on the Developer Cloud console for the chosen GPU | budget |
| C2 | credit_hours_total | $100 / C1 (DERIVED once C1 known). Free credit applies to new ADP members only (page) | budget |
| C3 | gpu_vram_gb | Console spec, confirm with `rocm-smi` on the instance | model size limit |
| C4 | model_vram_gb | Load the model with vLLM, read memory use | does it fit |
| C5 | tokens_per_second | Run a fixed prompt set against the vLLM endpoint, 3 runs, report mean | demo latency, claims in the pitch |
| C6 | cold_start_s | Time from instance start to first served token | how much time each restart burns |
| C7 | evolus_credits_per_op | Run one document/AI-tool call in the workspace and read the credit counter before/after | whether 50,000 is enough |
| C8 | hours_available | Shreyank (uni schedule), STATE placeholder | time split |
| C9 | demo_video_length_s | Final cut, must be under the 5 min limit in STATE | submission |
Any benchmark number in the pitch must come from C5-style runs, never from a vendor slide or from me.

## 4. Judge view (what is scored vs what must be shown)
| Criterion (page wording, paraphrased) | What the judge must see | Evidence to produce |
|---|---|---|
| Application of Technology: how well the models are integrated | AMD part running inside the working product | screen recording of the endpoint on AMD Cloud + latency C5 |
| Presentation | clear problem, user, demo | 5-min video, slides PDF, README |
| Business Value | fit to a business area, practical impact | one measurable before/after number per track brief ("Good projects will show") |
| Originality | not a standard chatbot/dashboard | one sentence stating what is new |
Track-specific demo rules (SOURCED, event page): T1 realistic industrial data with a useful alert/action; T2 visible uncertainty and human handover, no autonomous diagnosis; T3 explain how forecasts are computed, LLM not the only method; T4 two different audiences/inputs, cost per experience, who pays.
Commit spread across the event window is a stated positive signal (from STATE, lablab guide, not a rule): do not push all work in the last hours.

## 5. Track fit (ASSUMED, to be overwritten once skills and team are known)
- T1 Intelligent Industry matches the mechatronics background (sensors, maintenance data); needs realistic industrial data, which must be found or generated (secondary research; synthetic data must be labelled synthetic).
- T3 forces a non-LLM forecasting component; fits quant/statistics interest but adds scope.
- T2 carries the most safety obligations; most documentation work.
- Evolus is a separate path with the strictest checklist (containerized app, vLLM on AMD, 2 building blocks, API-driven).
- No decision: STATE keeps Track and Team as OPEN.

## 6. Order of work for the 3 days before kickoff
1. U11 (register) then U1 (paste getting-started guide) then re-read rule book for U2, U3, U7, U8.
2. If the Developer Cloud console is open: C1-C3. Do not spend credits before kickoff unless U3 allows work.
3. Post U1/U4/U7/U8 questions on Discord once; record the answers here with date and who answered.
4. Then secondary research (STATE queue) and only then a track decision.
