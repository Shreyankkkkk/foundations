# AMD Developer Hackathon: ACT III — Research Analyst Report

**Hackathon dates:** October 12–18, 2026 (online build phase), Oct 17–18 on-site in Rome, Milan, or Imperia, Italy.
**Mandatory constraint:** every project must run a meaningful part of its workload on AMD infrastructure or AMD hardware. Free $100 AMD Developer Cloud credits for new members. Teams of 1–6. Source: [lablab.ai brief](https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii), accessed Oct 10, 2026.

**Report scope:** Maps problems, existing solutions, and competitor gaps across all four tracks; identifies overlooked opportunities; ranks problem areas by evidence, severity, originality, feasibility, and demo value. Does NOT decide the final project.

**Evidence labels:**
- **[Documented]** — stated in the original study/official documentation, fetched and read.
- **[Vendor-reported]** — a vendor/secondary source's own published data; methodology and limits noted.
- **[Analyst hypothesis]** — my interpretation; needs direct user validation.
- **[Unverified]** — supporting evidence missing or not yet fetched.

---

## 1. Verified AMD implementation paths

**[Documented — fetched from official vLLM documentation, Oct 10, 2026:]**

- **vLLM on ROCm:** supported on MI200s (gfx90a), MI300 (gfx942), MI350 (gfx950), Radeon RX 7900 (gfx1100/1101), Radeon RX 9000 (gfx1200/1201), and Ryzen AI MAX / AI 300 (gfx1151/1150). ROCm 6.3+; MI350 requires ROCm 7.0+; Ryzen AI MAX requires ROCm 7.0.2+. **Python 3.12 only for pre-built ROCm wheels** (Python 3.10/3.11 will silently fall back to CUDA wheel and fail with `libcudart.so` errors). Pre-built wheels for ROCm 7.0 (`rocm700`) and 7.2.1 (`rocm721`). Source: [vLLM ROCm installation docs](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html). **[Documented]**
- **Vision-language models in vLLM:** native multimodal support for Qwen-VL, LLaVA, Aria, BLIP-2, Bee, Command-A Vision, Cosmos3, and many other image/video/audio-input model families. Source: [vLLM supported models](https://docs.vllm.ai/en/latest/models/supported_models.html). **[Documented]**
- **AMD Developer Cloud:** instant access to MI300X GPUs — small option 1× MI300X (192 GB), large option 8× MI300X (1,536 GB). ROCm 7 inference uplift (>3.5×) tested May 15, 2025 on Llama 3.1-70B (TP2), Qwen 72B (TP2), DeepSeek-R1 (FP16); training uplift (3×) via Megatron-LM on 8× MI300X. Source: [AMD ROCm 7 blog](https://www.amd.com/en/blogs/2025/enabling-the-future-of-ai-introducing-amd-rocm-7-and-the-amd-developer-cloud.html). **[Documented]**
- **vLLM ROCm attention backend benchmarks:** tested on MI300X (192GB, gfx942), MI325X (256GB, gfx942), MI355X (288GB, gfx950). Models: Qwen3-235B-A22B-FP8 (MHA), DeepSeek-R1-0528 (MLA). ROCM_AITER_FA was the reference backend in the benchmark; ROCM_ATTN was 3.6–4.4× slower than the reference. In one configuration another backend showed a lower relative value than the reference. **No vision-language model was in the benchmark set.** Source: [vLLM ROCm blog (Feb 27, 2026)](https://vllm.ai/blog/2026-02-27-rocm-attention-backend). **[Documented — VLM-specific ROCm throughput NOT measured here]**

**Gaps flagged:**
- **Whisper, speech-to-speech, and TTS on ROCm:** the ROCm inference docs page mentions only Hugging Face Transformers and vLLM generically; no specific speech or TTS pipeline documented there. **[Unverified — speech pipeline on AMD hardware is a candidate path, not confirmed by fetched documentation]**
- **Candidate architecture interpretation:** the brief says a "meaningful part of your workload" must run on AMD — this does NOT require every component (e.g., TTS synthesis) to run on AMD hardware. A VLM or translation model running on AMD Instinct with TTS synthesis running elsewhere is a **candidate architecture consistent with the stated meaningful-workload requirement; eligibility of that specific implementation is not separately confirmed.** **[Analyst interpretation of the fetched brief — not independently verified eligibility]**
- **Generic vLLM ROCm support + generic multimodal model support does NOT confirm each specific model/version combination.** Label specific model integrations as "candidate, untested," not end-to-end documented. **[Analyst note]**
- **Event-week GPU instance availability and quota:** not confirmed by the lablab.ai page. **[Unverified — explicit dependency]**

---

## 2. Track 1 — Intelligent Industry

### Problem 1.1: Unplanned downtime

**Evidence:** Siemens 2022 "True Cost of Downtime": unplanned downtime costs Fortune Global 500 companies **almost $1.5 trillion/year**, 11% of turnover (up from $864B, 8% in 2019–20). Survey Jan 2021–Aug 2022. 56 completed online interviews; Fortune Global 500 extrapolated from plant/employee counts. Source: [Siemens 2022 PDF](https://assets.new.siemens.com/siemens/assets/api/uuid:3d606495-dbe0-43e4-80b1-d04e27ada920/dics-b10153-00-7600truecostofdowntime2022-144.pdf). **[Documented — 56-interview extrapolation, not causal]**

**Current workaround:** Calendar-based preventive maintenance; run-to-failure with on-call repair. **[Analyst hypothesis]**

**Recent technical advance:** Anecdotal claim that predictive-maintenance AI adoption is growing — surfaced via secondary summary, not independently fetched. Source: [IoT Analytics via Stealth Agents](https://stealthagents.com/research/ai-predictive-maintenance-statistics-2026), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**

**Opportunity hypothesis:** Open-source, hardware-agnostic predictive maintenance on standard sensor streams, deployed on AMD Instinct via ROCm. **[Analyst hypothesis]**

### Problem 1.2: Visual quality inspection fatigue

**Evidence:** Anecdotal claim that human inspectors miss defects and accuracy degrades over time — surfaced via a vendor search result, underlying study not independently fetched. Source: [Oxmaint](https://oxmaint.com/industries/steel-plant/computer-vision-vs-manual-inspection-in-manufacturing), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**

**Current alternatives (fetched):** Cognex deep-learning vision — random defect detection and segmentation; positioned for applications "too difficult or time-consuming for rule-based machine-vision" and "too fast for human visual inspection." Platforms: VisionPro Deep Learning, In-Sight smart cameras. **Not specified on the page:** labeled-image training requirements, anomaly-detection vs novel-defect support, edge deployment, or stated limitations. Source: [Cognex Deep Learning Tools](https://www.cognex.com/en-my/products/machine-vision/vision-tools/ai-tools/deep-learning-tools), accessed Oct 10, 2026. **[Documented as stated; specific limitations unverified]**

**Documented remaining difficulty:** None established vs. Cognex from available documentation. **[Unverified — proposed opening vs. incumbent PC-vision is unproven]**

**Recent technical advance:** PLOS ONE (Feb 11, 2026): fine-tuned Qwen2.5-VL-3B (SFT + RFT with GRPO) reached mAP 0.63 on blue nitrile glove defect detection, beating YOLO11-L (0.62) on the same dataset. mAP 0.61 when unified across mixed products. Fine-tuned, NOT zero-shot. Dataset: 23,799 blue nitrile images (27,083 boxes). Source: [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0339867). **[Documented — mAP applies to that paper's dataset/protocol only]**
- 18 VLMs benchmarked zero-shot on sewer defects. Source: [Cambridge Prisms: Water (Mar 25, 2026)](https://discovery.researcher.life/article/multi-class-sewer-defect-detection-with-vision-language-models/da61662e83113110845b51ba9018f4fa). **[Documented — fetched via abstract only]**
- IMDD-1M is a candidate dataset surfaced in search; its contents, availability, and licence have not been independently verified. Source: [CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/papers/Ni_Towards_Open-Vocabulary_Industrial_Defect_Understanding_with_a_Large-Scale_Multimodal_Dataset_CVPR_2026_paper.pdf). **[Primary research paper read only through a search snippet — unverified lead, not numerical evidence]**

**Opportunity hypothesis:** Open-source VLM defect detection with plain-language description, as a lower-cost alternative to commercial PC-vision software. AMD path: Qwen-VL or LLaVA on vLLM ROCm wheels (Python 3.12, ROCm 7.0/7.2.1). **[Analyst hypothesis]**

### Problem 1.3: Technician knowledge and manual search time

**Evidence:** Anecdotal claim that wrench time is a minority of a shift and documentation search is a recoverable time slice — surfaced via vendor search result, underlying work-sampling study not independently fetched. Source: [Oxmaint](https://oxmaint.com/article/smart-maintenance-documents-technician-repairs), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**
- Anecdotal claim of an aging maintenance workforce facing retirement — underlying BLS data not independently fetched. Source: [Oxmaint skills gap](https://oxmaint.com/industries/manufacturing-plant/maintenance-skills-gap-manufacturing-solutions), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**

**Current alternatives:** CMMS platforms (UpKeep, Limble, Fiix) — Limble product features page returned HTTP error when fetched; capability details not independently verified. Static PDF shared drives; tribal knowledge. **[Unverified — CMMS document-search capability not confirmed from official docs]**

**Opportunity hypothesis:** Multimodal RAG over equipment manuals + historical work orders. AMD path: open LLM on vLLM ROCm. **[Analyst hypothesis]**

---

## 3. Track 2 — Health and Wellbeing

### Problem 2.1: Discharge instruction comprehension

**Evidence:** BMJ Open Quality study: at baseline, **none of 50 patients** had complete understanding of ED discharge instructions. Weakest areas: reasons to return to ED, medication frequency/duration. Setting: urban academic ED in Dallas, TX; 168 patients interviewed across baseline and preintervention. Source: [BMJ Open Quality](https://bmjopenquality.bmj.com/content/10/3/e001419). **[Documented]**
- Discharge instructions frequently exceed 6th-grade readability. Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9130361/), accessed Oct 10, 2026. **[Documented — full text not independently fetched]**

**Current workaround (fetched from BMJ study):** Nurses give verbal instructions at discharge; patients receive an "after-visit summary" (AVS) that is typically **6–22 pages long**; important details not necessarily on the first page (e.g., new medications first mentioned on page 5 of one AVS). 58 of 118 patients (~half) did not read their discharge papers; 73% rated standard instructions 10/10 yet median composite understanding score was 4/6. Source: [BMJ Open Quality](https://bmjopenquality.bmj.com/content/10/3/e001419). **[Documented]**

**Existing solution:** The study's intervention was a one-page Simplified Information Page (SIP) — a manual, human-designed template; no AI involved. **[Documented]**

**Vendor comparison (fetched):** Nabla lists a "patient summary" feature but does not describe discharge instructions or patient-facing instruction sheets. Source: [Nabla homepage](https://www.nabla.com), accessed Oct 10, 2026. **[Documented as stated — absence is an inference from the homepage, not a full product audit]**

**Opportunity hypothesis:** Personalized, plain-language discharge instruction simplifier that preserves supplied clinical content (medications, timing, follow-up, return precautions). **[Analyst hypothesis]**

### Problem 2.2: Language barriers in care

**Evidence:** Int J Qual Health Care (published Feb 2, 2007): of 222 classifiable LEP adverse-event reports (from 251 total LEP reports, out of 1,083 total across 6 hospitals, Feb–Aug 2005), 49.1% involved physical harm. Among 109 harm events, 46.8% (51/109) resulted in moderate temporary harm or worse. English-speaker comparison: 29.5%. Source: [Int J Qual Health Care](https://academic.oup.com/intqhc/article/19/2/60/1803865). **[Documented — 2007 pilot study, 6 hospitals, incident-report-based (prone to underreporting), not causal]**
- Multilingual qualitative study (2023, n=71 Spanish/Russian/Mandarin/Cantonese/Korean speakers, semi-structured interviews 2016–2018, northeastern US home health): participants described "knowing there is risk for harm," suboptimal care, translation losses, difficulty understanding consent. Source: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10294089/). **[Documented]**

**Current workaround:** Professional interpreter services (underuse claim from Int J Equity Health abstract only — full text not fetched); family members interpreting (essential but burdensome per PMC 2023 qualitative themes). **[Abstract-only claim — not fully verified; LanguageLine service capabilities page returned HTTP error when fetched; professional interpreter workflow safeguards not independently verified]**

**Recent technical advance:** Meta's Seamless family supports real-time, expressive cross-lingual speech-to-speech translation. Source: [Meta AI blog](https://ai.meta.com/blog/seamless-communication/), accessed Oct 10, 2026. **[Vendor-reported — ROCm compatibility and current status unverified]**

**Opportunity hypothesis:** Real-time multilingual patient-provider communication assistant for scripted, human-reviewed clinical workflow. AMD path: candidate — speech pipeline on AMD hardware is NOT confirmed by fetched documentation (ROCm inference docs do not document Whisper or TTS specifically). **[Analyst hypothesis with explicit AMD dependency]**

### Problem 2.3: Nurse documentation burden

**Evidence:** JAMIA (published 2024): 20 nurses from 5 acute/critical care units at one university hospital. A literature estimate that nurses spend ~35% of their shift documenting is cited in the fetched paper extraction — **not measured in this study.** Source: [JAMIA (abstract only)](https://academic.oup.com/jamia/article-abstract/31/11/2540/7755390). **[Literature estimate cited in the fetched paper extraction; not a study measurement]**

**Current alternatives (fetched):** Nabla — ambient documentation, dictation, coding; "patient summary" listed but not discharge instructions. Source: [Nabla](https://www.nabla.com). **[Documented as stated]**

**Opportunity hypothesis:** Nurse-focused ambient documentation for shift handoff. **[Analyst hypothesis — nurse-specific ambient scribe gap articulated by competitor content but not primary-validated]**

---

## 4. Track 3 — Reinvent Commerce

### Problem 3.1: Ecommerce search and discovery

**Evidence:** Baymard E-Commerce Search benchmark: **344 leading US/European ecommerce sites**; state of search described as "lacking." Search-specific study: users aged 21–56 tested 19 leading sites across 8 verticals; 700+ search-specific usability issues found. 25 rounds / 4,400+ sessions describe Baymard's broader methodology, not the search study alone. Source: [Baymard ecommerce search](https://baymard.com/research/ecommerce-search), accessed Oct 10, 2026. **[Documented]**
- Cart abandonment is widely reported but NOT direct evidence of a search problem — removed as nonessential. Source: [Baymard via Shopify](https://www.shopify.com/ph/blog/conversion-funnel-leaks), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**

**Current alternatives (fetched):**
- **Algolia:** hosted search engine with full-text, numerical, and faceted search; real-time results from first keystroke; powers billions of queries monthly; "Algolia AI" mentioned but specific AI capabilities not detailed on docs page; semantic/visual search not specified; pricing not stated. Source: [Algolia docs](https://www.algolia.com/doc/), accessed Oct 10, 2026. **[Documented as stated]**
- **Klevu:** discovery suite covering search, merchandising, recommendations; personalized recommendations on third-party systems (DotDigital, Shopify); integrations for Magento 2, Shopify, BigCommerce, Salesforce Commerce Cloud. Semantic/visual search specifics not stated on help page. Source: [Klevu help](https://help.klevu.com/), accessed Oct 10, 2026. **[Documented as stated]**

**Documented remaining difficulty:** Neither Algolia's docs nor Klevu's help page specifies visual/image search or semantic search details — but "not specified on the page" is not the same as "not offered." **[Unverified — visual search as a gap is unproven]**

**Opportunity hypothesis:** Open-source semantic + visual product discovery. AMD path: VLM on vLLM ROCm. **[Analyst hypothesis — incumbent space is crowded; originality unproven]**

### Problem 3.2: Inventory distortion

**Evidence:** Pygmalios State of Retail 2026: total inventory distortion $1.77T globally 2023 ($1.2T stockouts + $562B overstocks), sourced from IHL Group via Sensormatic; 2024 update $1.7T. **8.3% out-of-stock rate is the historical GMA 2002 benchmark** (71,000+ consumers, 29 countries), not a current measurement. Source: [Pygmalios PDF](https://www.pygmalios.com/reports/pygmalios-state-of-retail-2026.pdf). **[Documented — Pygmalios is a secondary source for IHL]**
- Netstock 2024 Benchmark Report: **~80% of Netstock-surveyed SMBs** struggle with insufficient forward planning (56%) and overstocking (24%); 72% cited lead-time variability; 23% invested in AI, 26% planned to. Survey: 300+ Netstock users (under $250M revenue); plus anonymized platform data from 2,400+ customers. Source: [Netstock](https://www.netstock.com/lp/2024-inventory-management-report/). **[Documented — vendor survey; population is Netstock's customer base, not all SMBs; the 56%/24% breakdown's source (survey vs platform data) not explicitly stated on the page]**

**Current alternatives (fetched):** Netstock product page: predictive sales forecasting by product/channel/location (accounts for seasonality/trends); flexible demand planning (bottom-up/top-down/middle-out); inventory optimization with SKU classification and safety-stock adjustment; AI-powered replenishment; supplier-risk support. Stated benefits: save up to 70% planning time; improve forecast accuracy up to 50%; reduce inventory holding 25%. **Explainability:** the page does NOT explicitly describe explainable forecasting or provide explanations for individual forecasts, nor name a specific forecasting model. Source: [Netstock products](https://www.netstock.com/products/), accessed Oct 10, 2026. **[Documented as stated — "explainability gap" is an inference from the product page, not a confirmed product limitation]**

**Opportunity hypothesis:** Lightweight, explainable demand forecasting for SMBs combining time-series model + LLM reasoning layer (not LLM-only, per brief). **[Analyst hypothesis]**

### Problem 3.3: Customer support AI resolution gap

**Evidence:** Ada + NewtonX study (March 2026): 2,000 consumers + 500 enterprise decision-makers across North America, Europe, and Asia. Key finding: only 24% of consumers said their most recent AI customer-service interaction was fully resolved by AI alone. Source: [Get Macha (fetched secondary reporting of the Ada/NewtonX study — not the original survey)](https://www.getmacha.com/blog/ai-customer-service-resolution-rate-statistics), accessed Oct 10, 2026. **[Vendor-reported via fetched secondary source — the original Ada/NewtonX survey was not directly fetched; demand evidence, NOT an executable benchmark]**
- Vendor AI resolution rates are reported with high variance across vendors — specific figures not independently verified. Source: [Get Macha](https://www.getmacha.com/blog/customer-service-ai-statistics), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**

**Current alternatives (fetched):** Intercom Fin — CX AI agent; resolves complex queries across channels; trained on knowledge + connected systems; RAG-based; data connectors to external systems; Fin for Ecommerce does personalized recommendations and checkout guidance. Source: [Intercom Fin docs](https://www.intercom.com/help/en/articles/7120684-fin-ai-agent-explained), accessed Oct 10, 2026. **[Documented as stated]**

**Documented remaining difficulty:** None established from fetched documentation. **[Unverified — proposed opening vs. Fin is unproven]**

**Opportunity hypothesis:** Open-source, self-hosted agentic support with full order-context and clean human handoff. AMD path: self-hosted LLM + VLM on vLLM ROCm. **[Analyst hypothesis]**

---

## 5. Track 4 — Create a New Kind of Experience

### Problem 4.1: Audio description gap

**Evidence:** ACB national survey (n=479+): 91% listened to audio description; 75.3% strongly agreed more programming needed; 45% had difficulty finding programs with audio description; 69.7% blind, 21.1% visually impaired. Survey date not stated on page. Source: [ACB](https://www.acb.org/content/acb-survey-finds-need-increased-audio-description), accessed Oct 10, 2026. **[Documented]**
- Anecdotal claim that platform audio-description catalogs differ substantially in size — surfaced via vendor search result, underlying platform data not independently fetched. Source: [Voxbooster](https://voxbooster.com/blog/audio-description-statistics-2026/), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**
- Netflix is actively expanding audio description — specific hours figure not independently verified. Source: [ppc.land](https://ppc.land/netflix-added-13-000-audio-description-hours-in-2025-and-what-else-changed/), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**
- Anecdotal claim that streaming ads largely lack accessibility features — XR Global Accessibility Maturity Index surfaced via search, not independently fetched. Source: [Advanced Television](https://www.advanced-television.com/2025/06/19/research-just-1-of-streaming-ads-include-accessibility-features/) (June 19, 2025). **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**

**Current alternatives (fetched):** 3Play Media AI-enabled audio description: AI scripts and voices descriptions, analyzes the entire video holistically; users can edit AI-generated script in platform or upgrade to human review. Workflow stages: (1) write description script (manual by trained describer, automated, or hybrid AI+human edit), (2) voice the description (professional voice artist or TTS), (3) follow DCMP description-key standards and WCAG 2.1, (4) publish (user-selectable track, separate track, pre-mixed, extended version, WebVTT). No prices stated on page. Source: [3Play Media](https://www.3playmedia.com/blog/what-is-audio-description/), accessed Oct 10, 2026. **[Documented as stated — 3Play Media already offers AI-enabled audio description; the remaining opening is NOT established and catalog expansion alone does not prove a gap]**

**Opportunity hypothesis:** Cloud-hosted, near-real-time audio description generator using open VLMs + TTS synthesis. AMD path: VLM on vLLM ROCm (documented for Qwen-VL/LLaVA families); **TTS synthesis on AMD hardware is unverified — candidate path, not confirmed.** Must demonstrate at least two audience/context inputs per brief. **[Analyst hypothesis]**

### Problem 4.2: Personalized video engagement

**Evidence:** Blings (a personalized-video platform vendor) claims positive case-study results — surfaced via vendor search result, not independently fetched. Source: [Blings](https://www.blings.io/blog/best-practices/personalized-video-statistics-2026-the-data-every-marketer-needs/), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**
- MIT IDE study on AI-generated personalized video ads — surfaced via search result, not independently fetched. Source: [MIT IDE](https://ide.mit.edu/insights/personalized-ai-video-ads/), accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**

**Current alternatives:** Blings, SundaySky, HeyGen, Synthesia. **[Unverified — whether avatar platforms respond to audience/context input requires primary docs]**

**Opportunity hypothesis:** Context-adaptive personalized video that changes based on live audience input. **[Analyst hypothesis]**

### Problem 4.3: Game and content localization cost

**Evidence:** Game localization has documented cost drivers (Keywords Studios, fetched above). Specific per-word price ranges surfaced via search results, not independently fetched. Source: [GameDev Outsourcing](https://www.gamedevoutsourcing.com/blog/game-localization-cost-guide), [Ulatus](https://www.ulatus.com/translation-blog/how-much-does-game-localization-cost/), both accessed Oct 10, 2026. **[Unverified search lead — page not fetched; not used as evidence or in the ranking]**

**Current alternatives (fetched):** Keywords Studios — localization agency; cost drivers: word count, target languages, audio localization (voice recording priced per finished hour — one of the larger line items), QA/LQA hours, simultaneous vs post-launch. Full dubbing is "most resource-intensive." Source: [Keywords Studios](https://www.keywordsstudios.com/en/about-us/news-events/news/a-step-by-step-guide-to-game-localization/). **[Documented as stated]**
- ElevenLabs Dubbing: 90+ languages; voice translation, speaker detection, audio dubbing; replaces original audio with new language preserving original speaker's voice; speaker-similarity adjustable (0–10, default 7); input via video/audio file or URL (YouTube/TikTok); limitations: transcript editing and audio regeneration via API on Enterprise plans only; higher cloning strength prioritizes similarity but may sound less natural across phonetically different languages. Source: [ElevenLabs Dubbing docs](https://elevenlabs.io/docs/product-guides/products/dubbing), accessed Oct 10, 2026. **[Documented]**

**Documented remaining difficulty:** None established vs. ElevenLabs Dubbing. **[Unverified — ElevenLabs already does multilingual voice-preserving dubbing; the proposed "novel" opportunity is reduced, not increased, by this incumbent]**

**Opportunity hypothesis:** Real-time, in-game adaptive localization preserving voice/tone/cultural context — but must differentiate from ElevenLabs Dubbing (which is batch-oriented, not real-time interactive). AMD path: candidate — speech pipeline on AMD hardware unverified. **[Analyst hypothesis — reduced originality given ElevenLabs incumbent]**

---

## 6. Evidence ledger (8 shortlisted areas)

| Area | Pain evidence | Current alternatives (fetched?) | Remaining gap | Technical enabler | Dataset/access | AMD path | Prototype test | Likely payer | Unresolved dependency |
|---|---|---|---|---|---|---|---|---|---|
| 1.2 Defect detection | [Oxmaint miss rate](https://oxmaint.com/industries/steel-plant/computer-vision-vs-manual-inspection-in-manufacturing) [Unverified search lead; magnitude of user pain not established] | [Cognex DL vision](https://www.cognex.com/en-my/products/machine-vision/vision-tools/ai-tools/deep-learning-tools) [Fetched] | None established vs Cognex [Unverified] | [Fine-tuned VLM (PLOS 2026)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0339867) [Documented] | IMDD-1M [Unverified license — search snippet only] | [vLLM ROCm Qwen-VL](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html) [Generic support documented for model family; specific integration candidate, untested] | Compare on same dataset; workflow value may come from descriptions, not accuracy alone | Mid-size manufacturer | Dataset licensing; VLM ROCm throughput unmeasured |
| 1.3 Technician RAG | [Oxmaint wrench time](https://oxmaint.com/article/smart-maintenance-documents-technician-repairs) [Unverified search lead; magnitude of user pain not established] | CMMS (UpKeep, Limble) [Not fetched — Limble returned HTTP error] | Unverified | Open LLM RAG | Public manuals (licensing check) | [vLLM ROCm open LLM](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html) [Generic support documented; specific integration candidate, untested] | Time-to-answer vs keyword search | Plant maintenance budget | Manual corpus acquisition; CMMS capability unverified |
| 2.1 Discharge comprehension | [BMJ 0/50 baseline; AVS 6-22 pages](https://bmjopenquality.bmj.com/content/10/3/e001419) [Documented] | [SIP (manual, 1-page template)](https://bmjopenquality.bmj.com/content/10/3/e001419) [Fetched from study]; [Nabla "patient summary"](https://www.nabla.com) [Fetched] | SIP is manual template, no AI; Nabla doesn't mention discharge instructions [Inference] | Open LLM simplification | Public discharge templates | [vLLM ROCm LLM](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html) [Generic support documented; specific integration candidate, untested] | Readability + content preservation (medications, timing, follow-up, return precautions) | Hospital QI budget | Content preservation verification method |
| 2.2 Language barriers | [Int J Qual Health Care 2007](https://academic.oup.com/intqhc/article/19/2/60/1803865) [Fetched] | Interpreters (underuse claim unverified); LanguageLine [HTTP error] | Underuse of professional interpreters [Abstract-only — full text not fetched] | [Seamless real-time S2ST](https://ai.meta.com/blog/seamless-communication/) [Vendor-reported] | Synthetic clinical dialogue | [Translation/LLM on vLLM ROCm](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html) [Generic support documented; specific integration candidate, untested]; speech components may run elsewhere per brief | Bilingual human review for omissions/meaning preservation; not just latency | Hospital language-services budget | Specific AMD-hosted model integration; end-to-end latency |
| 3.1 Ecommerce search | [Baymard 344-site benchmark](https://baymard.com/research/ecommerce-search) [Fetched] | [Algolia](https://www.algolia.com/doc/) [Fetched — AI mentioned, visual not specified]; [Klevu](https://help.klevu.com/) [Fetched — discovery suite] | Visual/semantic search not specified on docs pages [Unverified as gap] | VLM-based visual query | Public product catalog | [vLLM ROCm VLM](https://docs.vllm.ai/en/latest/models/supported_models.html) [Generic support documented; specific integration candidate, untested] | Search quality vs keyword baseline | Mid-size ecommerce brand | Crowded incumbent space; gap unproven |
| 3.2 SMB forecasting | [Netstock 2024 survey](https://www.netstock.com/lp/2024-inventory-management-report/) [Fetched — vendor] | [Netstock](https://www.netstock.com/products/) [Fetched — full product] | Explainability not explicit on Netstock product page [Inference, not confirmed gap] | Time-series + LLM reasoning | Public retail (M5, Rossmann) | [LLM on vLLM ROCm](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html) [Generic support documented; specific integration candidate, untested]; time-series on CPU | Time-based holdout; WAPE/sMAPE (not MAPE where sales=0) | SMB operator | Public dataset availability; LLM layer value |
| 3.3 Support orchestration | [Ada/NewtonX 24%](https://www.getmacha.com/blog/ai-customer-service-resolution-rate-statistics) [Fetched secondary source] | [Intercom Fin](https://www.intercom.com/help/en/articles/7120684-fin-ai-agent-explained) [Fetched] | None established vs Fin [Unverified] | Self-hosted agentic + order context | Synthetic orders + product images | [vLLM ROCm LLM+VLM](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html) [Generic support documented; specific integration candidate, untested] | Resolution rate on defined test set vs simple baseline | Ecommerce brand | Order-context integration complexity |
| 4.1 Audio description | [ACB survey](https://www.acb.org/content/acb-survey-finds-need-increased-audio-description) [Fetched] | [3Play Media AI-enabled AD](https://www.3playmedia.com/blog/what-is-audio-description/) [Fetched]; Netflix/Amazon expansion [Vendor-reported] | None established vs 3Play Media AI-enabled AD [Unverified — catalog expansion alone does not prove gap] | Open VLM + TTS synthesis | Public sample videos (licensed clip) | [VLM on vLLM ROCm](https://docs.vllm.ai/en/latest/models/supported_models.html) [Generic support documented; specific integration candidate, untested]; TTS may run elsewhere per brief | Two-mode demo (concise vs fuller narration); narration text AND audio synthesis; cost model with missing inputs marked | Streaming platform or accessibility service | Specific AMD-hosted model integration; end-to-end latency; 3Play Media incumbent |

**Note on 4.3 (Adaptive localization):** ElevenLabs Dubbing (fetched, documented) already does multilingual voice-preserving dubbing; this reduces the originality of the proposed opportunity. 4.3 is listed in Track 4 for completeness but is not shortlisted.

---

## 7. Ranked comparison (provisional)

**This ranking is provisional, not a validated project recommendation.** A strong problem study (high evidence score) does not imply a validated competitive opening (high originality). The user should apply their own weighting and validate the top areas against direct user evidence before choosing a project.

Scores are analyst judgments, 1–5. Rubric anchors: 5 = strong primary evidence / severe pain / clearly novel vs. fetched competitors / clearly feasible / high demo value; 3 = moderate; 1 = weak. Equal weights. **All scores are analyst judgments, not measured facts.** Sorted descending.

| Area | Evidence | Severity | Originality | Feasibility | Demo value | Total | Confidence | Blocking dependency |
|---|---:|---:|---:|---:|---:|---:|---|---|
| 2.1 Discharge comprehension | 5 | 4 | 4 | 4 | 4 | 21 | High confidence in pain evidence; differentiation unverified | Content preservation verification |
| 3.2 SMB forecasting | 4 | 5 | 3 | 4 | 4 | 20 | Medium | LLM layer must add real value; dataset |
| 2.2 Language barriers | 5 | 5 | 3 | 3 | 4 | 20 | High confidence in pain evidence; AMD integration untested | Specific AMD-hosted model integration; end-to-end latency |
| 1.2 Defect detection | 3 | 4 | 3 | 4 | 5 | 19 | Low-Medium | Dataset licensing; VLM ROCm throughput unmeasured |
| 3.3 Support orchestration | 4 | 4 | 2 | 4 | 4 | 18 | Medium | Originality reduced by Intercom Fin incumbent |
| 1.3 Technician RAG | 2 | 4 | 3 | 5 | 4 | 18 | Low (evidence) | Manual corpus acquisition; CMMS capability unverified |
| 3.1 Ecommerce search | 4 | 4 | 2 | 4 | 4 | 18 | Medium | Crowded incumbent space; visual-search gap unproven |
| 4.1 Audio description | 4 | 4 | 2 | 3 | 4 | 17 | Medium | Specific AMD-hosted model integration; end-to-end latency; 3Play Media AI-AD incumbent |

**Tiers:** 21 (discharge comprehension) → 20 (SMB forecasting; language barriers) → 19 (defect detection) → 18 (support orchestration; technician RAG; ecommerce search) → 17 (audio description). Ties are presented as tiers; a tie-breaker (e.g., prototype feasibility) would be needed to order within a tier, and the user should apply their own weighting.

**Originality scores now reflect fetched competitor evidence:** Intercom Fin reduces 3.3; ElevenLabs Dubbing reduces (and demotes) 4.3; Cognex DL reduces 1.2; 3Play Media AI-enabled AD reduces 4.1 (2, not 3 — an AI-enabled AD incumbent exists). **For 2.1 (discharge comprehension), the BMJ SIP intervention establishes that a manual, human-designed template is the existing solution — this does NOT establish that LLM-driven personalization is novel or overlooked; Nabla's homepage omission does not establish a gap either. The 4 (not 5) originality score for 2.1 is explicitly provisional and would shift with a fuller competitor audit.** **Unknown originality remains explicitly provisional, not a default score of 3.**

---

## 8. Prototype dossiers — eight ranked areas

### A — Track 1.2: VLM defect detection with explanation
- **Bounded workflow:** Upload part photo → VLM identifies defect class + bounding box → plain-language description → route decision.
- **Dataset:** IMDD-1M or MVTec AD. **Licensing/access unverified.**
- **Baseline:** Train YOLO or similar on the SAME dataset and split — not the PLOS paper's YOLO mAP (different dataset/protocol).
- **Demonstration outcome:** Compare on same dataset; workflow value may come from faster review or useful descriptions, not superior detection accuracy alone.
- **Main risk:** VLM ROCm throughput for vision workloads is unmeasured (the vLLM benchmark set tested text LLMs only); dataset licensing.
- **AMD path:** Qwen-VL or LLaVA on vLLM ROCm wheels (Python 3.12, ROCm 7.0/7.2.1). **Generic support documented; proposed integration candidate, untested; VLM-specific ROCm throughput NOT measured.**
- **Scope exclusions:** Not real-time line-speed; batch demo only.

### B — Track 1.3: Technician manual/knowledge RAG
- **Bounded workflow:** Technician asks "torque spec for compressor X bolt Y" → RAG over manuals + past work orders → cited answer.
- **Dataset:** Public equipment manuals (licensing check) + synthetic work orders.
- **Baseline:** Keyword search over same PDF.
- **Demonstration outcome:** Time-to-answer reduction vs keyword search on same query set.
- **AMD path:** Open LLM on vLLM ROCm. **Documented.**
- **Scope exclusions:** Text-based only.

### C — Track 2.1: Discharge instruction simplification
- **Bounded workflow:** Upload clinician-approved discharge instructions → adapt to 6th-grade reading level + preferred language → preserve all clinical content → flag ambiguity.
- **Dataset:** Public discharge-instruction templates.
- **Baseline:** Original instruction text.
- **Demonstration outcome:** Readability score improvement AND separately verify preservation of medications, timing, follow-up, return precautions.
- **AMD path:** Open LLM on vLLM ROCm. **Documented.**
- **Scope exclusions:** No new clinical advice; human review required.

### D — Track 2.2: Real-time multilingual patient communication
- **Bounded workflow:** Scripted patient-provider dialogue in 2 languages → real-time speech-to-speech translation with transcript + confidence display → escalate to human interpreter.
- **Dataset:** Synthetic clinical dialogue; bilingual human review.
- **Baseline:** Same dialogues translated by bilingual human reviewer; measure omissions and meaning preservation (not interpreter wait time — unmeasured).
- **AMD path:** **Candidate — the translation/LLM component can run on AMD Instinct per vLLM ROCm documentation; the full speech pipeline (ASR+MT+TTS) does not need to be entirely on AMD per the brief's "meaningful part" wording.** Specific model integration is candidate, untested.
- **Scope exclusions:** Not autonomous diagnosis; human-reviewed only.

### E — Track 3.2: SMB demand forecasting
- **Bounded workflow:** Upload sales CSV → time-series model forecast → LLM adds context → explainable inventory action.
- **Dataset:** Public retail (M5, Rossmann) with time-based holdout.
- **Baseline:** Moving average / naive on same holdout.
- **Demonstration outcome:** WAPE/sMAPE (not MAPE where sales=0) + explainability + how forecast produces inventory action.
- **AMD path:** Time-series on CPU, LLM on vLLM ROCm. **Documented.**
- **Scope exclusions:** Not real-time.

### F — Track 3.3: End-to-end agentic support
- **Bounded workflow:** Customer sends order question + product photo → agent pulls order/inventory status + VLM triages photo → recommends or hands off.
- **Dataset:** Synthetic orders + product images; defined test case set.
- **Baseline:** Simple keyword routing on same test set. **Do not use the 24% Ada/NewtonX survey as a benchmark — it is demand evidence only.**
- **AMD path:** LLM + VLM on vLLM ROCm. **Generic support documented; proposed integration candidate, untested; VLM throughput unmeasured.**
- **Scope exclusions:** No payments/refunds execution.

### G — Track 4.1: Cloud-hosted audio description generator
- **Bounded workflow:** Play a short licensed clip → VLM narrates visible scenes in two user-selectable modes: (a) concise, action-focused narration; (b) fuller scene description. Output is both narration text AND synthesized audio.
- **Dataset:** One short, licensed clip (e.g., public-domain or Creative Commons footage) — licensing check required.
- **Baseline:** Pre-generated human audio description on the same clip (for flagship content only).
- **Quality controls:** (1) visible-evidence check — narration must only describe what is visibly on screen; (2) no dialogue overlap — narration must avoid speaking over dialogue; (3) where obtainable, review by a blind/low-vision user.
- **Demonstration outcome:** Two-context demo (mode A vs mode B); narration latency; cost per minute of described video.
- **Conditional cost model (missing inputs marked, not invented):** GPU hourly rate × processing seconds ÷ 3,600 + TTS synthesis usage + serving costs. **GPU hourly rate and processing-time inputs are NOT yet measured — show the calculation and mark missing inputs.**
- **Main risk:** Real-time VLM video inference latency on AMD hardware is unverified; 3Play Media already offers AI-enabled AD (fetched) — the proposed opening vs. their product is NOT established.
- **AMD path:** VLM on vLLM ROCm (documented for Qwen-VL/LLaVA model families; specific model integration is candidate, untested). TTS synthesis may run elsewhere per the brief's "meaningful part" wording — this is NOT a prototype blocker.
- **Scope exclusions:** Short clips only, not feature-length; cloud AMD Instinct deployment assumption, not on-device.

### H — Track 3.1: Semantic + visual ecommerce search
- **Bounded workflow:** Shopper submits a product photo + text query ("find this lamp in a warm tone under $50") → VLM understands the visual product + text intent → returns ranked products with explanation of why each matched.
- **Dataset:** Public product catalog (e.g., Amazon product dataset with images); licensing check required.
- **Baseline:** Keyword search on the same catalog and query set.
- **Demonstration outcome:** Search result quality (precision/recall on defined query set) vs. keyword baseline; demonstration of visual query understanding.
- **Main risk:** Crowded incumbent space (Algolia, Klevu); visual-search gap is UNPROVEN — neither vendor's docs page specifies visual search, but "not specified" is not "not offered."
- **AMD path:** VLM on vLLM ROCm (Qwen-VL or LLaVA families). **Generic support documented; proposed integration candidate, untested; VLM-specific ROCm throughput unmeasured.**
- **Scope exclusions:** Not full ecommerce integration; search-only demo.

**Dossier I (Track 4.3, Adaptive game localization) is NOT shortlisted** due to ElevenLabs Dubbing incumbent (fetched, documented) reducing originality; still listed in Track 4 for completeness.

---

## 9. Sources

### Primary / official (fetched)
- [lablab.ai brief](https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii) (Oct 10, 2026).
- [Siemens True Cost of Downtime 2022 PDF](https://assets.new.siemens.com/siemens/assets/api/uuid:3d606495-dbe0-43e4-80b1-d04e27ada920/dics-b10153-00-7600truecostofdowntime2022-144.pdf).
- [Int J Qual Health Care 2007](https://academic.oup.com/intqhc/article/19/2/60/1803865).
- [PMC multilingual LEP study 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10294089/).
- [BMJ Open Quality discharge study (published 2021)](https://bmjopenquality.bmj.com/content/10/3/e001419).
- [PLOS ONE glove defect VLM 2026](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0339867).
- [Cognex Deep Learning Tools](https://www.cognex.com/en-my/products/machine-vision/vision-tools/ai-tools/deep-learning-tools).
- [Keywords Studios localization guide](https://www.keywordsstudios.com/en/about-us/news-events/news/a-step-by-step-guide-to-game-localization/).
- [Pygmalios State of Retail 2026 PDF](https://www.pygmalios.com/reports/pygmalios-state-of-retail-2026.pdf).
- [Netstock 2024 Benchmark Report](https://www.netstock.com/lp/2024-inventory-management-report/).
- [Baymard ecommerce search](https://baymard.com/research/ecommerce-search).
- [ACB audio description survey](https://www.acb.org/content/acb-survey-finds-need-increased-audio-description).
- [vLLM ROCm installation docs](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html).
- [vLLM supported models (multimodal)](https://docs.vllm.ai/en/latest/models/supported_models.html).
- [vLLM ROCm blog (Feb 27, 2026)](https://vllm.ai/blog/2026-02-27-rocm-attention-backend).
- [AMD ROCm 7 blog](https://www.amd.com/en/blogs/2025/enabling-the-future-of-ai-introducing-amd-rocm-7-and-the-amd-developer-cloud.html).
- [AMD ROCm inference docs](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference/index.html).
- [Intercom Fin docs](https://www.intercom.com/help/en/articles/7120684-fin-ai-agent-explained).
- [ElevenLabs Dubbing docs](https://elevenlabs.io/docs/product-guides/products/dubbing).
- [Nabla homepage](https://www.nabla.com).
- [JAMIA nurse documentation 2024 (abstract only)](https://academic.oup.com/jamia/article-abstract/31/11/2540/7755390).
- [Netstock products page (capabilities)](https://www.netstock.com/products/).
- [3Play Media audio description workflow](https://www.3playmedia.com/blog/what-is-audio-description/).
- [Algolia docs](https://www.algolia.com/doc/).
- [Klevu help](https://help.klevu.com/).

### Excerpt / abstract only (not fully fetched)
- [Cambridge Prisms sewer VLM (Mar 25, 2026)](https://discovery.researcher.life/article/multi-class-sewer-defect-detection-with-vision-language-models/da61662e83113110845b51ba9018f4fa)
- [Springer LNG LVLM (Sept 6, 2026)](https://link.springer.com/article/10.1007/s00170-026-17818-y)
- [Int J Equity Health (2026)](https://link.springer.com/article/10.1186/s12939-026-02895-y)
- [MIT IDE personalized video ads](https://ide.mit.edu/insights/personalized-ai-video-ads/)
- [Advanced Television XR accessibility index (June 19, 2025)](https://www.advanced-television.com/2025/06/19/research-just-1-of-streaming-ads-include-accessibility-features/)
- [PMC discharge readability](https://pmc.ncbi.nlm.nih.gov/articles/PMC9130361/)
- [PMC discharge comprehension older adults](https://pmc.ncbi.nlm.nih.gov/articles/PMC11560540/)
- [PMC EMR time burden](https://pmc.ncbi.nlm.nih.gov/articles/PMC12940217/)

### Secondary / vendor-reported (with caveats)
- [CVPR 2026 IMDD-1M](https://openaccess.thecvf.com/content/CVPR2026/papers/Ni_Towards_Open-Vocabulary_Industrial_Defect_Understanding_with_a_Large-Scale_Multimodal_Dataset_CVPR_2026_paper.pdf) — primary research paper; search excerpt only, not fetched.
- [Fluke downtime](https://www.fluke.com/en-us/learn/blog/condition-monitoring-and-alignment-software/unplanned-downtime-costs-manufacturers-up-to-852m-weekly)
- [Rapid Eye Inspections](https://rapideyeinspections.com/research/manufacturing-downtime-statistics/)
- [Stealth Agents / IoT Analytics](https://stealthagents.com/research/ai-predictive-maintenance-statistics-2026)
- [Oxmaint visual inspection](https://oxmaint.com/industries/steel-plant/computer-vision-vs-manual-inspection-in-manufacturing)
- [Matroid inspection](https://www.matroid.com/visual-quality-inspection/)
- [Oxmaint skills gap](https://oxmaint.com/industries/manufacturing-plant/maintenance-skills-gap-manufacturing-solutions)
- [Oxmaint technician search time](https://oxmaint.com/article/smart-maintenance-documents-technician-search-time)
- [UpKeep knowledge loss](https://upkeep.com/blog/maintenance-knowledge-loss-why-hiring-does-not-replace-a-retiring-technician/)
- [Envive AI ecommerce metrics](https://www.envive.ai/post/on-site-engagement-metrics-statistics)
- [Shopify / Baymard cart abandonment](https://www.shopify.com/ph/blog/conversion-funnel-leaks)
- [Chain Store Age IHL](https://chainstoreage.com/study-global-retail-losses-due-inventory-distortion-hit-177-trillion)
- [STL Today IHL stockouts](https://www.stltoday.com/exclusive/article_a17b908b-aca2-58cb-b17d-b8f51b49ba09.html)
- [Get Macha Ada/NewtonX](https://www.getmacha.com/blog/ai-customer-service-resolution-rate-statistics)
- [eDesk support cost](https://www.edesk.com/blog/how-to-reduce-customer-service-costs-ecommerce/)
- [Ringly support cost](https://www.ringly.io/blog/ecommerce-customer-service-cost-per-contact)
- [SiliconAngle CX orchestration](https://siliconangle.com/2026/10/02/ai-in-customer-experience-has-an-orchestration-problem-not-an-adoption-problem/)
- [Deepcura nurse scribes](https://www.deepcura.com/resources/best-ai-scribe-for-nurses)
- [Voxbooster audio description](https://voxbooster.com/blog/audio-description-statistics-2026/)
- [ppc.land Netflix AD](https://ppc.land/netflix-added-13-000-audio-description-hours-in-2025-and-what-else-changed/)
- [ACB ADP Netflix report 2021 (PDF)](https://adp.acb.org/docs/PosabilityArticleApr2021.pdf) — search-result snippet only, not fetched.
- [Disability Horizons streaming](https://disabilityhorizons.com/2020/06/accessibility-issues-with-online-streaming-services/)
- [Blings personalized video](https://www.blings.io/blog/best-practices/personalized-video-statistics-2026-the-data-every-marketer-needs/)
- [GameDev Outsourcing localization](https://www.gamedevoutsourcing.com/blog/game-localization-cost-guide)
- [Ulatus localization](https://www.ulatus.com/translation-blog/how-much-does-game-localization-cost/)
- [Voxbooster game localization](https://voxbooster.com/blog/game-localization-statistics-2026/)
- [Fora Soft multimedia cost](https://www.forasoft.com/blog/article/ai-powered-multimedia-solutions-introduction-benefits-applications)
- [Meta AI Seamless blog](https://ai.meta.com/blog/seamless-communication/)
- [PMC discharge readability](https://pmc.ncbi.nlm.nih.gov/articles/PMC9130361/) — excerpt only
- [PMC discharge comprehension older adults](https://pmc.ncbi.nlm.nih.gov/articles/PMC11560540/) — excerpt only
- [PMC EMR time burden](https://pmc.ncbi.nlm.nih.gov/articles/PMC12940217/) — excerpt only

---

*Report generated October 10, 2026. All claims marked [Unverified] or [Analyst hypothesis] require primary-source verification before building. This report does not choose the final project.*

---

## 10. Unanswered questions

**Discriminating questions:**
1. Which specific users still struggle despite existing products, and why?
2. Which remaining gap is documented (primary source) vs. assumed (vendor marketing)?
3. What data can legally be obtained during the event week?
4. What result could a small benchmark demonstrate against today's workaround?
5. Which dependencies block the prototype vs. merely limit production?

**Per-opportunity:**
6. **1.2:** Is IMDD-1M/MVTec AD licensed for hackathon use? What is VLM-specific ROCm throughput (unmeasured)?
7. **2.2:** What is full speech-to-speech (ASR+MT+TTS) latency on AMD Instinct? What is FDA classification (do not assume)?
8. **2.1:** How is content preservation verified in the demo?
9. **3.2:** Which public dataset has enough history for a time-based holdout?
10. **1.3:** Are there public, licensed equipment-manual corpora?
11. **4.1:** What is real-time VLM video narration latency and TTS quality on AMD? Cost per minute (show calculation, not invented estimate)?
12. **Cross-cutting:** What are exact AMD Developer Cloud GPU instances, quotas, and access timing? Setup time for ROCm vLLM for a team new to ROCm?
13. **Cross-cutting:** For each idea, what is the hardest implementation risk, and the fallback plan?

---
