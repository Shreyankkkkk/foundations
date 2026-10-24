# CODEMAP scripts (auto-generated) | L<n> = line number
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
  find_source_files() L74
  git_names(*options) L86
  publishable_files(extensions) L104
  signature(node) L118
  describe_file(path) L124
  group_of(rel) L147
  describe_pine_file(path) L155
  build_map() L174
  write_if_changed(outputs) L210
  snapshot() L231
  watch(cpu_budget) L243
  describe_ctags_files() L269
  main() L321
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
