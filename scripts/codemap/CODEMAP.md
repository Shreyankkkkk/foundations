# CODEMAP (auto-generated, do not edit) | L<n> = line number, may lag behind edits | 48 files listed, 11 without functions/classes omitted
learning/programming/data-analysis/exercises/pandas_basics_excercise.py
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
  repo_slug() L22
  read(path) L40
  context_sections() L44
  log_tail(project) L61
  file_list(project) L66
  build(project) L78
  body(text) L95
  main() L99
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
