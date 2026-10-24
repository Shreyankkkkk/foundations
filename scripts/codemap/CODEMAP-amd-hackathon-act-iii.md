# CODEMAP amd-hackathon-act-iii (auto-generated) | L<n> = line number
projects/amd-hackathon-act-iii/backend/scripts/build_data.py
  build() L373
projects/amd-hackathon-act-iii/backend/scripts/check_data.py
  check(ok, label, detail='') L21
  norm(s) L27
  load(name) L32
projects/amd-hackathon-act-iii/backend/src/config.py
  judge_limits() L57
  require_judge_settings() L69
projects/amd-hackathon-act-iii/backend/src/evaluation/benchmark.py
  load_json(path) L30
  save_json(path, data) L35
  drift_key(item) L42
  score_flags(flags, answer_key) L47
  build_results(flags, answer_key, notes, stats, gpu=None) L87
  real_run_problem(stats) L152
  main() L165
projects/amd-hackathon-act-iii/backend/src/evaluation/publish.py
  _is_number(value) L42
  _is_whole(value) L46
  _is_text(value) L50
  _is_date(value) L54
  _is_share(value) L61
  _wrong_fields(item, expected) L65
  check_contract(sop, notes, flags, bench) L75
  check_real_run(stats, bench, details, flags, notes, allowed_failed=0) L157
  build_amd(stats, price_per_hour=None) L184
  main() L201
projects/amd-hackathon-act-iii/backend/src/models/fake_model.py
  read_first_step(prompt) L41
  read_note_text(prompt) L49
  find_trigger(note_text) L58
  class FakeModel L68
    __init__(self, misbehave=True) L69
    ask(self, prompt) L73
projects/amd-hackathon-act-iii/backend/src/pipeline.py
  flag_id_for(note_id, sop_id, step_id, drift_type) L32
  build_flag(note, proposal) L41
  process_note(note, steps, model) L58
  run(model, limit=None, workers=1) L81
  save_json(path, data) L158
  main() L165
projects/amd-hackathon-act-iii/backend/src/stages/judge.py
  build_prompt(note, candidates) L29
  parse_reply(reply_text) L66
  is_valid_proposal(item, candidates) L102
  judge_note(note, candidates, model) L123
  class RealModel L136
    __init__(self, base_url, model_name, api_key=None, timeout=None, retries=0) L139
    ask(self, prompt) L149
  make_real_model() L180
projects/amd-hackathon-act-iii/backend/src/stages/loader.py
  _read_json_list(path) L16
  _check_fields(items, required, label, path) L25
  load_sop_steps(path=None) L37
  load_notes(path=None) L45
projects/amd-hackathon-act-iii/backend/src/stages/matcher.py
  _words(text) L19
  pick_candidate_steps(note, steps, top_n=None) L24
projects/amd-hackathon-act-iii/backend/src/stages/quote_check.py
  _tokens(text) L36
  words_of(text) L46
  find_quote(quote, note_text) L51
  quote_in_note(quote, note_text) L69
  exact_quote(quote, note_text) L74
projects/amd-hackathon-act-iii/frontend/scripts/sync_backend_data.py
  main() L14
projects/amd-hackathon-act-iii/frontend/src/data_loader.py
  class DataError L11
  _read(k) L14
  _live(k) L24
  read_decisions() L31
  save_decision(flag_id, status) L39
  get_data(want_demo) L48
projects/amd-hackathon-act-iii/frontend/src/ingest.py
  _ext(name) L17
  read_text(name, data) L20
  read_rows(name, data) L37
  make_title(text) L51
  split_sop_steps(text) L57
  parse_sop_file(name, data, sop_id) L72
  to_iso(s) L82
  norm_source(s) L92
  split_notes_text(text) L96
  parse_notes_file(name, data) L121
  finish_notes(raw, defaults) L131
  _clean(v) L142
  clean_steps(rows) L145
  clean_notes(rows) L158
  validate(steps, notes) L166
  to_json(items) L188
projects/amd-hackathon-act-iii/frontend/src/quote.py
  _tokens(text) L9
  quote_span(note_text, quote) L18
projects/amd-hackathon-act-iii/frontend/src/theme.py
  title(question, sub) L59
  big(value, label) L62
  banner(mode) L67
projects/amd-hackathon-act-iii/frontend/src/views/analytics.py
  _frame(d) L9
  _week_label(w) L21
  _pct(x) L24
  _npm(b) L27
  _show(x) L30
  _run_line(b) L33
  _trend(f, label) L38
  overview(d) L46
  heat_strip(d) L66
  benchmark(d) L109
  amd(d) L135
projects/amd-hackathon-act-iii/frontend/src/views/review.py
  _save(fid, status) L8
  _goto(fid) L11
  _note(r, notes) L14
  _chips(r) L22
  _fix(r) L27
  review_queue(d) L32
  evidence_viewer(d) L66
projects/amd-hackathon-act-iii/frontend/src/views/upload.py
  _plate(n, text) L12
  _safe(f, parse) L15
  _sig(*parts) L24
  add_documents(d) L27
