# Brief: AMD Developer Hackathon ACT III

Read 2026-10-08. Paraphrased, not copied. Tags: SOURCED = read directly from the source; PASTED = text Shreyank pasted from the source; UNREAD = not read; UNVERIFIED = stated somewhere but not confirmed for this event.

## Sources
- Event page (SOURCED): https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii
- Live dashboard, snapshot 2026-10-08 (SOURCED): .../live
- Hackathon Guidelines article (SOURCED): https://lablab.ai/ai-articles/hackathon-guidelines (generic lablab process)
- Rule book (PASTED): https://lablab.ai/hackathon-rules (the fetcher could not render it)
- Submission Guide, "AI Hackathons: The Complete Guide" and "How to Win an AI Hackathon" (PASTED): generic lablab articles, not specific to this event
- Getting-started guide (UNREAD): https://lablab.ai/getting-started-guide
- Evolus developer quickstart, evolus.ai/developers (UNREAD; published "before kickoff")
- Event Discord (UNREAD): schedule, mentors, #looking-for-team

## 1. The event
- Hybrid AMD x lablab.ai hackathon. Online build 2026-10-12 to 2026-10-18; optional on-site phase 10-17/18 in Rome (Link Campus University), Milan (SmartCityLab) or Imperia (IMPERIAWARE). On-site is for approved participants only, one city each; travel and accommodation not covered.
- Everything runs in the cloud on AMD GPUs (AMD Developer Cloud, ROCm). No local GPU needed. Open to all experience levels.
- Prize pool $12,000+; split per track not published. Prize payout up to 90 days. Submissions must be original and MIT-compliant.
- Key times (UTC / GST): kickoff and registration close 10-12 15:00 UTC / 19:00 GST; submissions close and judging starts 10-18 15:00 UTC / 19:00 GST.
- Scale at snapshot: 5,007 registered builders, 871 teams forming.

## 2. The core requirement
Build a working product that solves a real problem for a real user. A meaningful part of the workload must run on AMD infrastructure (Developer Cloud, Instinct, ROCm, Ryzen AI, Radeon, or other approved AMD infrastructure) and that part must be in the product shown to judges. Language models, vision, audio, agents, predictive models or any mix are allowed; models, frameworks and tools are free choice.

## 3. Tracks (Vibe Generation is the partner on tracks 1 to 4)
| Track | What to build | Hard rules in the brief |
|---|---|---|
| 1 Intelligent Industry | Help a manufacturer cut downtime, improve quality or safety, or use resources better (failure prediction, defect detection, anomaly explanation, manual and maintenance-record search, safety monitoring, waste reduction) | Demo realistic industrial data in, useful alert/explanation/recommendation/action out; not only a dashboard; show a measurable gain |
| 2 Health and Wellbeing | Make one part of the patient journey safer, clearer or easier (intake, record summaries, appointment prep, care navigation, discharge instructions, multilingual communication, document processing, admin automation, prevention) | No autonomous diagnosis or treatment advice. Must show uncertainty and when a human takes over; explain handling of wrong or unsupported answers, sensitive data, high-risk decisions, human review |
| 3 Reinvent Commerce | Help a business attract, serve, convert or retain customers (shopping assistants, recommendations, support, demand and inventory planning, catalogue enrichment, review analysis, promotions, churn, multilingual and accessible shopping, in-store vision) | If predicting demand, sales or behaviour, explain how the prediction is calculated; a language model must not be the only forecasting method |
| 4 Create a New Kind of Experience | Media, marketing or entertainment experience not practical before generative AI; responds to the audience or context, not just one generated image/ad/chatbot | Show the experience changing for at least 2 audiences, situations or inputs; explain what was created, what the models generated or decided, quality control, cost per generated experience, who pays and why |
| Partner track: Evolus Business Agents on AMD | An agent that runs a real business process end to end on Evolus (inputs: email, PDF, recording, web form, chat; actions: run an Evolus workflow, extract documents to data, use AI Tools, update systems, hand off to a person) | Free Evolus event workspace (event code at kickoff, valid to 2026-10-31, up to 6 members, 50,000 credits, no card); main agent on an open model served through your own vLLM endpoint on AMD Developer Cloud; at least 2 Evolus building blocks; drive Evolus through its REST API (agent chat also via OpenAI-compatible endpoint); containerized app, public repo, README that runs; no API keys in the repo. Evolus reviews workspace configuration and API usage to verify |

Track 1 to 4 projects shown "good" when they show: a real problem, a working product, understandable results, a measurable improvement (the Track 4 version asks for original concept, strong experience, realistic cost).

Evolus building blocks: workflows, document extractors, 11 AI Tools (document to data, table extraction, layout-keeping translation, PDF redaction, summaries, meeting minutes, email, rewriting, simplification, sentiment, text comparison), knowledge libraries (RAG), MCP connectors, sub-agents, chat widget, webhooks. Evolus also exposes an MCP server and a coding agent (Evolus Studio).

## 4. Prizes and partner awards
- Main prize per challenge. Google and Evolus technologies are optional; using an eligible partner technology adds a chance at that partner's prize. One project can qualify for the main prize, one partner prize, or both partner prizes. Google's technologies and prize terms are not described on the page.
- Vibe Generation special prize: AirPods 5 for every member of the best solution. Judged on Hybrid (strategy, quantifying value, commercial attitude), Becreatives (technical execution, AI orchestration, ability to ship), Vibe Generation (taste, originality, human plus AI workflow).
- Credits: $100 AMD Developer Cloud for new AMD AI Developer Program members.

## 5. Judging (all tracks)
1. Application of Technology: how effectively the models are integrated. On the Evolus track: depth of Evolus building-block use and quality of the AMD-hosted model integration.
2. Presentation: clarity and effectiveness.
3. Business Value: impact and practical fit to a business area.
4. Originality: uniqueness and creativity.
Weights are not published. lablab's guide adds these signals (a guide, not a rule): working and deployed demo, a real repo with commits across the event window, AI doing more than a chatbot wrapper, a specific user, a rough market size, a revenue model.

## 6. Eligibility, registration, teams
- Approval needs: sign up with AMD (create an AMD AI Developer Program account if none), enroll on lablab, join the lablab Discord. Registration closes at kickoff.
- Teams of 1 to 6; find teammates on the dashboard (teams marked "looking for members") or Discord #looking-for-team. Solo allowed.
- Rule book does not state age, country or employment eligibility, what may be prepared before kickoff, rules on AI-assisted coding or third-party code. Open.

## 7. Submission (all required unless marked)
| Item | Requirement | Source |
|---|---|---|
| Title | Clear and descriptive; max 50 chars | rule book; guidelines article |
| Short description | Max 255 chars | rule book; submission guide |
| Long description | At least 100 words: problem, solution, audience, unique features | submission guide |
| Track and tags | Technology and category tags, proper categorization | rule book |
| Cover image | PNG or JPG, 16:9 | rule book |
| Video | MP4, max 5 min; under 300 MB (guidelines article). Intro, then slides, then product features | rule book; submission guide |
| Slides | PDF | rule book |
| Code | Public GitHub repo (private lowers the score); README; no secrets | rule book; submission guide; event page |
| Demo platform and URL | Rule book names Streamlit, Replit or Vercel; interactive URL required. Fit for a GPU-backed app is UNVERIFIED | rule book |
| Working prototype | AMD component part of what judges see | event page |
| IBM Bob report | In the submission guide only; not on the ACT III page; UNVERIFIED for this event | submission guide |
| Late | Manual submission only within 6 h after the deadline, valid reason, prior approval | rule book |

Pitch advice from lablab guides (not rules): lead with the problem, show the product working, then market (TAM/SAM), revenue, competitors and USP, then roadmap; keep slides to 2-3 sentences each; record the video early. Their sample timing is built for a 72 h event; this one is about 144 calendar hours.

## 8. Conduct
Plagiarism, gaming the voting system, unauthorized automation, tampering, fraud: removal or disqualification. Not following submission guidelines: lower score or exclusion. Organizers and mentors who participate are not prize-eligible and cannot judge. The "Mini Hackathon" rules in the rule book (limited mentor support) do not appear to apply to this event.

## 9. Discrepancies and gaps
- Online build end: event page says 12-18 Oct; one live-page line says 12-17 Oct. Submission close 10-18 15:00 UTC is consistent. Plan on 10-18.
- Live page shows Tracks "TBA" and Tech partners "0"; event page lists the tracks. Event page treated as current.
- Event schedule "to be announced": no workshop, mentor or demo-day times.
- Guides are generic and partly stale (72 h pacing, IBM Bob, "Claude, GPT-4, Gemini or Granite" API-only advice). This event expects AMD GPU use; API-only builds risk failing the AMD requirement.
- Rule book silent on eligibility, pre-kickoff preparation, AI-assisted coding, third-party code.
- ACT III vs the separate AMD AI Academy Challenge XP ("participate in an AMD hackathon" +300 in that event's table): UNVERIFIED.
