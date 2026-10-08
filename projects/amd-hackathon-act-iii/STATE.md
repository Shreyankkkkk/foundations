# AMD Hackathon ACT III STATE

AMD Developer Hackathon: ACT III (lablab.ai x AMD). Hybrid: online build 2026-10-12 to 2026-10-18, optional on-site 10-17/18 in Italy (travel not covered).
Status: day 0, pre-kickoff. AMD sign-up done (new account). lablab "Enroll" and Discord join: unconfirmed.
Goal: priority 1 = experience and learning; priority 2 = winning. Team: 1-6 allowed; solo vs friends undecided.
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
| days_to_kickoff | 4 | 2026-10-12 minus 2026-10-08 | calendar | DERIVED |
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
| Team vs solo | Allowed 1-6; undecided | - | OPEN |
| Track | Not chosen; needs team and skills known | - | OPEN |

## Open items / next actions
1. Confirm lablab enrollment and Discord join (deadline above). Shreyank.
2. Answer the 3 setup questions (hours per day, solo or team and skills, online only); fills `hours_available`, team decision.
3. Read the getting-started guide in a browser (fetcher cannot render lablab guide pages reliably); settle the "Not covered by the rule book" row.
4. Check whether ACT III counts toward AI Academy XP (see `projects/amd-hackathon/`).
5. Primary research queue (not started): AMD Developer Cloud GPU type, $/h, credit hours, vLLM serve test; Docker/Linux on Shreyank's machine; schedule and mentor hours in GST; track requirements vs skills.
6. Secondary research queue (not started): past lablab/AMD winners in tracks of interest, vLLM-on-ROCm docs, Evolus quickstart, track datasets. Tag each finding SOURCED or RECALLED.
7. No code until primary research is logged here.

## Where things are
- `docs/brief.md`: complete brief (event, tracks, rules, submission, judging, discrepancies, sources)
- `LOG.md`: dated changes
