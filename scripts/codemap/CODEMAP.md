# CODEMAP (auto-generated, do not edit) | L<n> = line number, may lag behind edits | 78 files listed, 20 without functions/classes omitted
learning/programming/data-analysis/exercises/pandas_basics_exercise.py
  list_functions(module) L3
learning/programming/python/data-structure-algorithm/LinkedList.py
  class LinkedList L6
    __init__(self) L18
    __str__(self) L28
    is_empty(self) L44
    size(self) L48
    search(self, value) L56
    get(self, index) L70
    index(self, value) L82
    add(self, data) L100
    prepend(self, data) L112
    remove(self, data) L128
    pop(self) L163
    pop_first(self) L170
    clear(self) L177
    reverse(self) L188
learning/programming/python/exercises/adjacency_list_to_matrix.py
  adjacency_list_to_matrix(adjacent_list: dict) L44
learning/programming/python/exercises/bisection_method.py
  square_root_bisection(number, tolerance=0.01, operations=25) L27
learning/programming/python/exercises/budget_app.py
  class Category L79
    __init__(self, name) L80
    deposit(self, amount, description='') L84
    withdraw(self, amount, description='') L91
    get_balance(self) L102
    transfer(self, amount, category) L108
    check_funds(self, amount) L115
    __str__(self) L121
  create_spend_chart(categories: list) L157
learning/programming/python/exercises/depth_first_search.py
  dfs(adjacency_matrix: list, nodes_start: int) L28
learning/programming/python/exercises/email_simulator.py
  class Email L18
    __init__(self, sender, receiver, subject, body) L19
    mark_as_read(self) L27
    display_full_email(self) L30
    __str__(self) L40
  class User L44
    __init__(self, name) L45
    send_email(self, receiver, subject, body) L49
    check_inbox(self) L54
    read_email(self, index) L58
    delete_email(self, index) L61
  class Inbox L64
    __init__(self) L65
    receive_email(self, email) L68
    list_emails(self) L71
    read_email(self, index) L79
    delete_email(self, index) L89
learning/programming/python/exercises/game_character.py
  class GameCharacter L61
    __init__(self, name) L62
    __str__(self) L68
    name(self) L72
    health(self) L76
    health(self, new_health) L80
    mana(self) L89
    mana(self, new_mana) L93
    level(self) L102
    level_up(self) L105
learning/programming/python/exercises/hash_table.py
  class HashTable L41
    __init__(self) L42
    hash(self, string: str) L45
    add(self, key, value) L48
    remove(self, key) L57
    lookup(self, key) L70
learning/programming/python/exercises/luhn_algorithm.py
  check_digits(number_string) L37
  verify_card_number(number_string) L44
learning/programming/python/exercises/n_queens.py
  dfs_n_queens(n) L33
learning/programming/python/exercises/nth_fibonacci.py
  fibonacci(number) L15
learning/programming/python/exercises/planet_class.py
  class Planet L2
    __init__(self, name, planet_type, star) L3
    __str__(self) L16
    orbit(self) L19
learning/programming/python/exercises/player_interface.py
  class Player L4
    __init__(self) L5
    make_move(self) L10
    level_up(self) L18
  class Pawn L21
    __init__(self) L22
    level_up(self) L31
learning/programming/python/exercises/polygon_area_calculator.py
  class Rectangle L78
    __init__(self, width: int, height: int) L79
    __str__(self) L83
    set_width(self, width: int) L86
    set_height(self, height: int) L88
    get_area(self) L91
    get_perimeter(self) L93
    get_diagonal(self) L95
    get_picture(self) L97
    get_amount_inside(self, shape) L106
  class Square L111
    __init__(self, side) L112
    __str__(self) L115
    set_side(self, side) L118
    set_width(self, side) L121
    set_height(self, side) L123
learning/programming/python/exercises/quick_sort.py
  quick_sort(array: list) L19
learning/programming/python/exercises/selection_sort.py
  selection_sort(array) L22
learning/programming/python/exercises/tower_of_hanoi.py
  disks(number_of_disks, rods=3) L32
  hanoi_solver(number_of_disks: int, rods=3, start=0, end=2, history=None, rods_list=None) L42
learning/programming/python/exercises/user_configuration_manager.py
  add_setting(settings: dict, setting: tuple) L55
  update_setting(settings: dict, setting: tuple) L64
  delete_setting(settings: dict, key) L73
  view_settings(settings: dict) L81
learning/programming/python/notes/graphs_and_trees_notes.py
  list_functions(module) L192
learning/programming/python/notes/inheritance_polymorphism_abstraction_notes.py
  class Animal L19
    __init__(self, name, age) L20
  class Dog L24
    __init__(self, name, age, breed) L25
  class Parent L42
    __init__(self) L43
  class Child L46
    __init__(self) L47
learning/programming/python/notes/oop_pillars_notes_and_demos.py
  class Wallet L52
    __init__(self) L53
    __validate(self, amount) L56
    deposit(self, amount) L60
    withdraw(self, amount) L64
    get_balance(self) L70
  class Circle L108
    __init__(self, radius) L109
    radius(self) L113
    area(self) L117
    radius(self, value) L121
    radius(self) L127
playground/EURUSD_graph_test.py
  plot_chart(interval) L7
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
projects/amd-hackathon-act-iii/backend/tests/test_benchmark.py
  flag(flag_id, note_id, sop_id='SOP-01', step_id=1, drift_type='skipped_step', quote='skipped lockout') L35
  run(flags, stats=STATS, gpu=None) L44
  test_all_found_gives_perfect_scores() L48
  test_benchmark_has_exactly_the_contract_fields_in_order() L56
  test_one_drift_missed() L61
  test_no_flags_gives_none_precision_and_zero_recall() L68
  test_flag_on_trap_note_is_a_false_alarm_with_the_trap_reason() L75
  test_flag_on_clean_note_is_a_false_alarm() L84
  test_wrong_drift_type_on_a_drift_note_is_false_alarm_and_a_miss() L90
  test_wrong_step_on_a_drift_note_is_false_alarm() L100
  test_second_flag_for_the_same_drift_is_a_duplicate_false_alarm() L107
  test_quote_verified_rate_comes_from_run_stats() L114
  test_missing_stats_give_none_fields() L121
  test_zero_proposals_in_stats_gives_none_rate_not_a_crash() L128
  test_gpu_and_matcher_fields() L133
  test_by_drift_type_counts() L139
  test_flag_with_quote_not_in_its_note_is_reported() L146
  test_good_flags_have_no_bad_quotes() L152
  write(path, data) L157
  test_main_writes_benchmark_and_details_files(monkeypatch, tmp_path) L161
  test_quote_verified_rate_uses_quotes_verified_when_the_run_stats_have_it() L182
  test_main_without_flags_file_stops_with_a_clear_message(monkeypatch, tmp_path) L188
  setup_real_run(monkeypatch, tmp_path, stats) L196
  test_real_run_without_gpu_is_refused(monkeypatch, tmp_path) L209
  test_real_run_records_the_gpu(monkeypatch, tmp_path) L217
  test_real_run_with_pretend_run_stats_is_refused(monkeypatch, tmp_path) L226
  test_real_run_problem_cases() L235
projects/amd-hackathon-act-iii/backend/tests/test_fake_model.py
  make_note(text) L15
  find_note_text(wanted, start_text, limit=2000) L19
  test_reads_note_and_first_step_back_out_of_the_prompt() L28
  test_find_trigger_picks_the_sentence_with_the_trigger_word() L35
  test_find_trigger_none_for_a_clean_note() L41
  test_clean_note_gives_no_flags() L45
  test_drift_note_gives_a_valid_flag_with_a_real_quote() L51
  test_same_prompt_gives_same_reply() L59
  test_misbehaving_model_invents_a_quote_the_quote_check_rejects() L65
  test_misbehaving_model_sometimes_wraps_reply_in_a_fence_and_parse_reply_copes() L74
  test_prompt_without_steps_or_note_gives_empty_list() L81
projects/amd-hackathon-act-iii/backend/tests/test_judge.py
  good_item(**changes) L33
  class StubModel L46
    __init__(self, reply) L49
    ask(self, prompt) L53
  test_drift_types_match_the_contract() L60
  test_prompt_contains_note_and_every_step() L72
  test_prompt_lists_every_drift_type_and_the_empty_reply_rule() L81
  test_parse_plain_list() L90
  test_parse_empty_list() L94
  test_parse_list_inside_code_fence() L98
  test_parse_list_with_words_around_it() L103
  test_parse_reply_without_a_list_raises() L108
  test_parse_brackets_in_wrong_order_raises() L113
  test_parse_broken_json_raises() L118
  test_parse_skips_brackets_in_the_words_before_the_list() L123
  test_parse_skips_a_broken_bracket_before_the_list() L128
  test_parse_prefers_the_list_of_objects_over_a_list_of_numbers() L132
  test_parse_still_returns_a_list_that_has_no_objects() L136
  test_parse_treats_one_bare_object_as_a_list_of_one() L140
  test_parse_finds_a_bare_object_after_words() L144
  test_good_item_is_valid() L150
  test_extra_fields_are_allowed() L154
  test_missing_field_is_invalid(missing) L159
  test_non_dict_is_invalid(bad) L166
  test_step_not_shown_to_the_model_is_invalid() L170
  test_step_from_the_wrong_sop_is_invalid() L174
  test_step_id_as_text_is_invalid() L179
  test_unknown_drift_type_is_invalid() L184
  test_bad_quote_is_invalid(quote) L189
  test_confidence_inside_0_to_1_is_valid(confidence) L194
  test_bad_confidence_is_invalid(confidence) L199
  test_judge_note_returns_valid_proposals() L205
  test_judge_note_sends_the_note_text_to_the_model() L212
  test_judge_note_empty_reply_means_no_flags() L219
  test_judge_note_drops_invalid_items_and_keeps_valid_ones() L223
  test_judge_note_without_candidates_does_not_call_the_model() L234
  test_judge_note_reply_without_a_list_raises() L240
  class FakeResponse L247
    __init__(self, status_code=200, retry_after=None) L248
    raise_for_status(self) L252
    json(self) L256
  class FakeRequests L260
    __init__(self, fail) L272
    post(self, url, headers, json, timeout) L276
  real_model_with(monkeypatch, fail, **settings) L283
  test_real_model_retries_a_connection_failure_then_succeeds(monkeypatch) L291
  test_real_model_gives_up_when_the_retries_run_out(monkeypatch) L297
  test_real_model_does_not_retry_by_default(monkeypatch) L304
  test_real_model_passes_the_timeout_on(monkeypatch) L311
  scripted_model(monkeypatch, responses, retries) L319
  test_real_model_waits_for_retry_after_on_429_then_succeeds(monkeypatch) L336
  test_real_model_gives_up_on_429_when_retries_run_out(monkeypatch) L343
  test_real_model_does_not_retry_429_when_retries_is_zero(monkeypatch) L351
  test_real_model_never_retries_a_400(monkeypatch) L358
  test_judge_limits_read_the_environment_values(monkeypatch) L367
  test_judge_limits_when_nothing_is_set(monkeypatch) L374
  test_judge_limits_reject_bad_values(monkeypatch, timeout, retries) L382
projects/amd-hackathon-act-iii/backend/tests/test_loader.py
  count_in_file(path) L13
  test_loads_every_step() L19
  test_loads_every_note() L23
  test_note_ids_are_unique() L27
  test_missing_field_gives_clear_error(tmp_path) L32
  test_item_that_is_not_an_object_gives_clear_error(tmp_path) L39
projects/amd-hackathon-act-iii/backend/tests/test_matcher.py
  make_step(step_id, text) L9
  test_picks_the_step_that_shares_words() L13
  test_rare_word_beats_common_word() L19
  test_never_returns_more_than_the_limit() L29
  test_no_shared_words_returns_empty_list() L35
projects/amd-hackathon-act-iii/backend/tests/test_pipeline.py
  make_note(note_id, text, shift='Day') L23
  class StubModel L39
    ask(self, prompt) L42
  class ReplyModel L48
    __init__(self, *proposals) L51
    ask(self, prompt) L54
  small_data(monkeypatch) L59
  test_build_flag_has_exactly_the_contract_fields() L68
  test_build_flag_values() L73
  test_flag_id_depends_only_on_note_step_and_drift_type() L86
  test_process_note_keeps_flag_whose_quote_is_in_the_note(small_data) L95
  test_process_note_drops_flag_whose_quote_is_not_in_the_note(small_data) L101
  test_process_note_lets_model_errors_through_for_run_to_handle(small_data) L107
  test_process_note_replaces_the_models_quote_with_the_notes_own_words(small_data) L112
  test_process_note_keeps_punctuation_that_belongs_to_the_notes_words(small_data) L118
  test_process_note_gives_whole_number_step_ids(small_data) L125
  test_run_counts_kept_dropped_and_failed(small_data) L133
  test_run_keeps_going_after_a_failed_note(small_data) L146
  test_run_flag_ids_are_stable_and_follow_note_order(small_data, monkeypatch) L152
  test_run_merges_identical_flags_and_keeps_the_more_confident_one(small_data) L162
  test_run_limit_only_processes_the_first_notes(small_data) L170
  test_run_stats_has_timing_fields(small_data) L177
  test_run_with_the_fake_model_gives_flags_with_real_quotes_only(small_data, monkeypatch) L184
  test_save_json_round_trip_keeps_text_as_is(tmp_path) L205
  test_main_fake_mode_writes_flags_and_stats_to_the_fake_folder(small_data, monkeypatch, tmp_path) L213
  test_run_records_the_slowest_note_time(small_data) L228
  test_run_refuses_an_empty_sop(monkeypatch) L233
  test_main_stops_and_writes_nothing_when_every_note_failed(small_data, monkeypatch, tmp_path) L239
  test_run_with_several_workers_gives_the_same_flags_in_the_same_order(small_data, monkeypatch) L255
  test_run_with_several_workers_still_survives_a_failed_note(small_data) L266
  test_run_refuses_fewer_than_one_worker(small_data, workers) L274
projects/amd-hackathon-act-iii/backend/tests/test_publish.py
  problems(sop=SOP, notes=NOTES, flags=FLAGS, bench=BENCH) L31
  with_flag(**changes) L35
  test_good_files_have_no_contract_problems() L41
  test_a_quote_that_is_not_in_the_note_is_a_problem() L45
  test_a_flag_on_an_unknown_step_or_note_is_a_problem() L50
  test_bad_confidence_status_and_drift_type_are_problems() L55
  test_an_extra_or_missing_flag_field_is_a_problem() L62
  test_duplicate_flag_ids_are_a_problem() L69
  test_flag_date_or_shift_that_differs_from_its_note_is_a_problem() L73
  test_null_benchmark_numbers_are_problems_because_this_is_the_real_run() L77
  test_a_false_alarm_that_is_not_a_flag_is_a_problem() L84
  test_bad_sop_and_note_rows_are_problems() L90
  real_problems(stats=STATS, bench=BENCH, details=DETAILS, flags=FLAGS, notes=NOTES) L98
  test_a_finished_real_run_has_no_problems() L102
  test_the_pretend_model_is_refused() L106
  test_run_with_failed_notes_or_missing_notes_is_refused() L110
  test_benchmark_from_other_flags_or_other_model_is_refused() L115
  test_cost_per_1000_notes_comes_from_price_and_speed() L123
  test_without_a_price_nothing_is_invented() L129
  write(path, data) L137
  setup(monkeypatch, tmp_path, stats=STATS) L141
  test_main_copies_five_files_to_demo_and_front_end(monkeypatch, tmp_path) L160
  test_main_refuses_the_pretend_model_and_copies_nothing(monkeypatch, tmp_path) L178
  test_check_only_copies_nothing(monkeypatch, tmp_path) L188
  test_main_stops_with_a_clear_message_when_the_benchmark_has_not_run(monkeypatch, tmp_path) L196
  test_main_without_a_front_end_folder_still_writes_the_demo_copy(monkeypatch, tmp_path) L205
projects/amd-hackathon-act-iii/backend/tests/test_quote_check.py
  test_exact_quote_passes() L12
  test_capitals_are_ignored() L16
  test_extra_spaces_and_line_breaks_are_ignored() L20
  test_whole_note_as_quote_passes() L25
  test_invented_words_fail() L29
  test_changed_word_order_fails() L33
  test_words_with_something_in_between_fail() L37
  test_partial_word_fails() L42
  test_quote_longer_than_note_fails() L47
  test_empty_or_blank_quote_fails() L51
  test_empty_note_fails() L56
  test_non_text_input_fails_instead_of_crashing() L60
  test_dropped_trailing_full_stop_passes() L65
  test_quote_marks_and_ellipsis_around_quote_pass() L69
  test_curly_and_straight_apostrophes_match() L74
  test_punctuation_inside_a_word_must_match() L78
  test_changed_word_still_fails_with_punctuation_ignored() L84
  test_punctuation_only_quote_fails() L88
  test_find_quote_gives_positions_in_the_original_note() L93
  test_exact_quote_returns_the_notes_own_wording() L99
  test_exact_quote_keeps_punctuation_attached_to_the_notes_words() L104
  test_exact_quote_is_always_a_piece_of_the_note() L109
  test_exact_quote_is_none_when_the_quote_is_not_there_or_not_text() L115
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
projects/amd-hackathon-act-iii/frontend/tests/test_analytics.py
  flag(flag_id, date, step_id=1) L9
  test_weeks_stay_in_order_across_new_year() L15
  test_flag_for_a_step_missing_from_the_sop_still_gets_a_label() L20
  test_week_label_shows_the_monday_of_that_week() L26
projects/amd-hackathon-act-iii/frontend/tests/test_data_loader.py
  decisions(tmp_path, monkeypatch) L11
  test_missing_decisions_file_means_no_decisions(decisions) L18
  test_damaged_decisions_file_means_no_decisions(decisions) L22
  test_decisions_file_that_is_not_an_object_means_no_decisions(decisions) L27
  test_save_decision_keeps_earlier_decisions(decisions) L32
  test_save_decision_replaces_a_damaged_file(decisions) L39
  test_amd_file_is_optional(tmp_path, monkeypatch) L45
  test_other_missing_file_names_the_file(tmp_path, monkeypatch) L51
  test_file_that_is_not_json_names_the_file(tmp_path, monkeypatch) L57
projects/amd-hackathon-act-iii/frontend/tests/test_ingest.py
  test_numbered_steps_and_titles() L5
  test_no_numbering_falls_back_to_paragraphs() L10
  test_dated_log_becomes_notes_with_shift_and_type() L13
  test_csv_columns_are_matched_by_alias() L18
  test_validate_catches_problems_and_accepts_good_data() L23
  test_quote_rule_ignores_case_spaces_and_curly_quotes() L30
projects/monte-carlo-simulation/archive/monte_carlo_chatgpt_v6.0.0.py
  generate_monthly_split(trades) L162
  generate_weekly_split(trades) L182
  calculate_max_drawdown(equity_curve) L200
  calculate_time_under_water(equity_curve) L219
  calculate_sharpe_ratio(equity_curve) L240
  calculate_sortino_ratio(equity_curve) L254
  generate_rr_ratios(n, lower_limit, upper_limit) L273
  vectorized_trade_simulation(n_trades, account_size, risk_levels, win_rate_base, lower_rr, upper_rr, commission, be_percent, max_dd_threshold, is_prop_firm) L283
projects/monte-carlo-simulation/archive/monte_carlo_claude_v6.0.0.py
  generate_monthly_split(trades) L162
  generate_weekly_split(trades) L182
  calculate_max_drawdown(equity_curve) L200
  calculate_time_under_water(equity_curve) L219
  calculate_sharpe_ratio(equity_curve) L240
  calculate_sortino_ratio(equity_curve) L254
  generate_rr_ratios(n, lower_limit, upper_limit) L273
  vectorized_trade_simulation(n_trades, account_size, risk_levels, win_rate_base, lower_rr, upper_rr, commission, be_percent, max_dd_threshold, is_prop_firm) L283
projects/monte-carlo-simulation/archive/monte_carlo_claude_v6.1.0.py
  class SimulationError L22
  class DatabaseError L26
  class InputValidationError L30
  class NumericalError L34
  safe_database_connection(host, user, passwd, database) L39
  safe_int_input(prompt, min_val=None, max_val=None, default=None) L68
  safe_float_input(prompt, min_val=None, max_val=None, default=None) L94
  validate_risk_levels(risk_levels) L120
  safe_array_operation(func, *args, **kwargs) L130
  generate_monthly_split(trades) L347
  generate_weekly_split(trades) L365
  calculate_max_drawdown(equity_curve) L383
  calculate_time_under_water(equity_curve) L402
  calculate_sharpe_ratio(equity_curve) L423
  calculate_sortino_ratio(equity_curve) L437
  generate_rr_ratios(n, lower_limit, upper_limit) L456
  vectorized_trade_simulation(n_trades, account_size, risk_levels, win_rate_base, lower_rr, upper_rr, commission, be_percent, max_dd_threshold, is_prop_firm) L466
  plot_equity_curves_optimized() L833
  plot_rr_distribution_optimized() L973
projects/monte-carlo-simulation/archive/monte_carlo_claude_v6.2.0.py
  class SimulationError L22
  class DatabaseError L26
  class InputValidationError L30
  class NumericalError L34
  safe_database_connection(host, user, passwd, database) L39
  safe_int_input(prompt, min_val=None, max_val=None, default=None) L68
  safe_float_input(prompt, min_val=None, max_val=None, default=None) L94
  validate_risk_levels(risk_levels) L120
  safe_array_operation(func, *args, **kwargs) L130
  generate_monthly_split(trades) L357
  generate_weekly_split(trades) L375
  calculate_max_drawdown(equity_curve) L393
  calculate_time_under_water(equity_curve) L412
  calculate_sharpe_ratio(equity_curve) L433
  calculate_sortino_ratio(equity_curve) L447
  generate_rr_ratios(n, lower_limit, upper_limit) L466
  generate_regime_sequence(n_trades, avg_regime_length=20) L476
  vectorized_trade_simulation(n_trades, account_size, risk_levels, win_rate_base, lower_rr, upper_rr, commission, be_percent, max_dd_threshold, is_prop_firm, missed_trade_pct) L512
  plot_equity_curves_optimized() L906
  plot_rr_distribution_optimized() L1046
projects/monte-carlo-simulation/archive/monte_carlo_v1.0.0.py
  random_number_of_trades() L20
  random_monthly_split(trades) L73
  split_trades_week(trades) L92
  news_event() L103
  month() L111
  counter() L115
  max_draw(equity_curve) L120
  sharpe_ratio(equity_curve) L130
  sortino_ratio(equity_curve) L139
  calmar_ratio(equity_curve) L150
  drawdown_duration(equity_curve) L159
  time_under_water(equity_curve) L178
  htf_align() L192
  sweep() L200
  risk_to_reward() L208
  function_control(account_size, number_of_trades) L212
projects/monte-carlo-simulation/archive/monte_carlo_v2.0.0.py
  random_monthly_split(trades) L159
  split_trades_week(trades) L170
  news_event() L181
  month() L190
  counter() L194
  max_draw(equity_curve) L199
  sharpe_ratio(equity_curve) L209
  sortino_ratio(equity_curve) L218
  calmar_ratio(equity_curve) L228
  drawdown_duration(equity_curve) L236
  time_under_water(equity_curve) L255
  htf_align() L269
  sweep() L277
  risk_to_reward() L285
  run_single_simulation(account_size, number_of_trades) L292
projects/monte-carlo-simulation/archive/monte_carlo_v3.0.0.py
  random_monthly_split(trades) L172
  split_trades_week(trades) L183
  news_event() L194
  month() L203
  counter() L207
  max_draw(equity_curve) L212
  sharpe_ratio(equity_curve) L222
  sortino_ratio(equity_curve) L231
  calmar_ratio(equity_curve) L241
  drawdown_duration(equity_curve) L249
  time_under_water(equity_curve) L268
  htf_align() L282
  sweep() L290
  risk_to_reward() L298
  run_single_simulation(account_size, number_of_trades) L305
projects/monte-carlo-simulation/archive/monte_carlo_v4.0.0.py
  random_monthly_split(trades) L173
  split_trades_week(trades) L184
  news_event() L195
  month() L204
  counter() L208
  max_draw(equity_curve) L213
  sharpe_ratio(equity_curve) L223
  sortino_ratio(equity_curve) L232
  calmar_ratio(equity_curve) L242
  drawdown_duration(equity_curve) L250
  time_under_water(equity_curve) L269
  htf_align() L283
  sweep() L291
  risk_to_reward() L299
  run_single_simulation(account_size, number_of_trades) L306
projects/monte-carlo-simulation/archive/monte_carlo_v5.0.0.py
  random_monthly_split(trades) L182
  split_trades_week(trades) L193
  news_event() L204
  month() L213
  counter() L217
  max_draw(equity_curve) L222
  sharpe_ratio(equity_curve) L232
  sortino_ratio(equity_curve) L241
  calmar_ratio(equity_curve) L251
  drawdown_duration(equity_curve) L259
  time_under_water(equity_curve) L278
  htf_align() L292
  sweep() L300
  risk_to_reward() L308
  run_single_simulation(account_size, number_of_trades) L315
projects/monte-carlo-simulation/archive/monte_carlo_v6.0.0.py
  random_monthly_split(trades) L190
  split_trades_week(trades) L201
  break_even_check() L212
  news_event() L225
  month() L234
  counter() L238
  max_draw(equity_curve) L243
  sharpe_ratio(equity_curve) L253
  sortino_ratio(equity_curve) L262
  calmar_ratio(equity_curve) L272
  drawdown_duration(equity_curve) L280
  time_under_water(equity_curve) L299
  htf_align() L313
  sweep() L321
  risk_to_reward() L329
  run_single_simulation(account_size, number_of_trades) L336
projects/monte-carlo-simulation/current/config.py
  class InputValidationError L17
  _prompt_int(prompt, lo=None, hi=None, default=None) L21
  _prompt_float(prompt, lo=None, hi=None, default=None) L42
  _prompt_yn(prompt, default='n') L63
  _realism_settings(p) L70
  collect_params(mode='new', prev_params=None) L136
  params_to_db_dict(p: dict) L208
projects/monte-carlo-simulation/current/database.py
  class DatabaseError L18
  _connect(host, user, passwd, database, timeout=10) L23
  save_run(host, user, passwd, database, params: dict) L45
  load_run(host, user, passwd, database, run_id: int) L71
projects/monte-carlo-simulation/current/main.py
  _line(char='─') L25
  _header(title) L28
  _row(label, value, value_colour=ENDC, width=38) L33
  _print_results(agg, params, portfolio_m, dd_m, streak_m, ratio_m, rr_m) L38
  main() L139
projects/monte-carlo-simulation/current/metrics.py
  monthly_percentile_table(monthly_curves, account_size, n_months, start_year=2027) L12
  percentile_curves(all_curves, max_len, sample_n=5000, percentiles=(0, 5, 25, 50, 75, 95, 100)) L135
  compute_curve_metrics(all_curves, chunk_size=10000) L151
  time_under_water_batch(all_curves, chunk_size=10000) L203
  portfolio_metrics(final_balances, account_size) L237
  rr_stats(rr_array) L257
  streak_stats(win_streaks, loss_streaks, be_streaks) L274
  drawdown_stats(mdd_array, tuw_array) L285
  ratio_stats(sharpes, sortinos, calmars) L297
projects/monte-carlo-simulation/current/orchestrator.py
  _single_worker(params, worker_seed) L10
  run_parallel(params: dict, n_jobs: int=-1, verbose: int=0) L61
  aggregate_results(all_results, params) L70
projects/monte-carlo-simulation/current/plotting.py
  _apply_dark(fig, axes) L41
  _dollar_fmt(x, _) L55
  _pct_fmt(x, _) L63
  plot_equity_curves(pct_curves, all_equity_curves, account_size, n_sims, block=False) L71
  plot_dashboard(final_balances, max_dds, sharpes, sortinos, win_streaks, loss_streaks, rr_ratios, account_size, metrics_dict, block=False) L123
  plot_regime_waterfall(pct_curves, account_size, block=False) L237
  _val_colour(v) L322
  _fmt_pct(v) L328
  _fmt_money(v, compact=True) L332
  _draw_header(ax, stats, accent, label) L347
  _draw_year(ax, year_data, pct_key, usd_key, bal_key, accent, accent_dark, account_size) L395
  plot_monthly_breakdown(monthly_table, account_size, extra_stats=None, block=False) L485
projects/monte-carlo-simulation/current/simulation_core.py
  _generate_rr(n, lo, hi) L39
  _regime_sequence(n, trades_per_month=16) L54
  _garch_vol_path(n, omega=1e-05, alpha=0.09, beta=0.9) L109
  _edge_decay_path(n_trades, decay_start=150, decay_every=175, wr_drop_per_event=1.5, rr_squeeze_per_event=0.04, max_wr_decay=8.0, max_rr_decay=0.2) L134
  _session_modifier(trade_idx, trades_per_day=3) L184
  _kelly_fraction(win_prob, avg_rr, fraction=0.25) L205
  simulate_one(n_trades, account_size, risk_levels, win_rate_base, lower_rr, upper_rr, commission, be_percent, max_dd_threshold, is_prop, missed_trade_pct, use_kelly, kelly_fraction, ar1_rho, psych_dd_threshold, psych_reduction, partial_at_rr, partial_fraction, trades_per_month, n_months, edge_decay_on, decay_start, decay_every) L236
  max_drawdown(curve) L582
  time_under_water(curve) L599
  sharpe_ratio(curve) L616
  sortino_ratio(curve) L625
  calmar_ratio(curve, periods_per_year=252) L637
projects/monte-carlo-simulation/current/test_metrics.py
  test_max_drawdown_flat() L19
  test_max_drawdown_50pct() L25
  test_max_drawdown_recovery() L31
  test_max_drawdown_monotone_rise() L38
  test_time_under_water_zero() L44
  test_time_under_water_basic() L50
  test_sharpe_zero_std() L57
  test_sharpe_positive() L63
  test_sortino_no_downside() L71
  test_calmar_zero_drawdown() L77
  test_kelly_positive_edge() L86
  test_kelly_negative_edge() L93
  test_kelly_caps_at_2() L100
  test_portfolio_metrics_basic() L109
  test_rr_stats_empty() L120
  test_rr_stats_values() L126
  test_drawdown_stats() L134
  test_streak_stats() L143
  test_simulate_one_runs() L152
  test_simulate_one_prop_firm() L171
  test_simulate_one_kelly() L188
projects/sumo-robot/design/parametric/main_deck_PARAMETRIC_SOURCE.py
  box(cx, cy, z0, z1, w, l) L87
  cyl_z(cx, cy, z0, z1, d) L95
  cyl_y(cx, y0, y1, cz, d) L100
  cyl_x(x0, x1, cy, cz, d) L110
  add_bulkhead(deck, side, y0, y1) L141
  post(cx, cy, z0, z1, d, hole_d) L178
  add_driver_standoffs(deck, center) L197
scripts/build_portable.py
  repo_slug() L23
  read(path) L41
  context_sections() L45
  log_tail(project) L62
  file_list(project) L66
  build(project) L79
  body(text) L96
  main() L100
scripts/codemap/codemap.py
  find_py_files() L34
  git_names(*options) L46
  publishable_py_files() L59
  signature(node) L73
  describe_file(path) L79
  build_map() L101
  write_if_changed(text) L117
  snapshot() L130
  watch(cpu_budget) L142
  main() L166
scripts/mcp_helper/helper_server.py
  debug(message) L56
  logged(function) L66
  git_names(*options) L84
  publishable_files() L97
  read_text(path) L110
  search_code(query: str, glob: str='') L123
  read_lines(path: str, start: int, end: int) L167
scripts/mcp_helper/selftest.py
  async step(label, coroutine) L25
  async call(session, name, **arguments) L39
  async main() L44
scripts/repo_health.py
  git_names(*options) L38
  tokens(path) L48
  check_tracked_ignored(tracked_ignored) L54
  check_codemap(tracked_ignored) L67
  check_sizes() L90
  main() L123
scripts/token_tools/token_tools.py
  count_tokens(text, encoding_name=DEFAULT_ENCODING) L33
  run_count(args) L47
  log_call(label, model, input_tokens, output_tokens, log_path=DEFAULT_LOG) L71
  run_log(args) L89
  read_log(log_path) L98
  percentile(values, pct) L111
  run_report(args) L118
  build_parser() L151
  main() L177
