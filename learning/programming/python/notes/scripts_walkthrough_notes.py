'''
HOW THE REPO SCRIPTS ARE BUILT (walkthrough of everything in scripts/)

Read this file to learn: what each script does inside, which function does what, which standard
module is used where, and how the scripts depend on each other. L<n> = line number taken from
scripts/codemap/CODEMAP.md (may lag behind edits; find the real line with search_code "def name").

Files covered:
    scripts/build_portable.py            builds projects/*/PORTABLE.md
    scripts/codemap/codemap.py           builds scripts/codemap/CODEMAP.md (function/class index)
    scripts/mcp_helper/helper_server.py  the foundations-helper MCP server (search_code, read_lines)
    scripts/mcp_helper/selftest.py       tests the server without Claude Desktop
    scripts/token_tools/token_tools.py   counts tokens, logs usage, suggests a max_tokens cap
Concept notes for the techniques used here: files_cli_and_scripts_notes.py (same folder).
'''

'''
1. THE BIG PICTURE: how the five scripts connect

Every script finds the repo root the same way, from its own location:
    REPO_ROOT = Path(__file__).resolve().parents[2]    # scripts/<folder>/<file>.py -> 2 folders up
    (build_portable.py sits directly in scripts/, so it uses .parent.parent: also 2 levels up)

Three of them ask git which files are "publishable":
    git ls-files --cached --others --exclude-standard -z
    codemap.py and helper_server.py both do this, so private folders are never indexed or readable.

Data flow:
    AI-CONTEXT.md + projects/X/STATE.md + projects/X/LOG.md --build_portable.py--> projects/X/PORTABLE.md
    every .py file in the repo ------------------------------codemap.py---------> scripts/codemap/CODEMAP.md
    AI reads CODEMAP.md (rule 1 of AI-CONTEXT.md) -> knows the file + line -> calls read_lines (helper_server.py)
    token_tools.py measured AI-CONTEXT.md (4439 chars = 1153 tokens) -> that ratio became CHARS_PER_TOKEN in helper_server.py
    selftest.py starts helper_server.py as a child process and calls its tools -> proves the server works

When something breaks, the order to look: CODEMAP.md (which file/function) -> read_lines (that function only).
'''

'''
2. WHERE DO I FIX X? (fast index)

Symptom / change wanted                              File and function
PORTABLE.md has wrong/missing AI rules               build_portable.py  context_sections (+ KEEP_SECTIONS at the top)
PORTABLE.md raw links are wrong                      build_portable.py  repo_slug (reads .git config) and file_list (builds URL)
PORTABLE.md shows too many/few log lines             build_portable.py  LOG_TAIL constant, log_tail
PORTABLE.md rewrites itself every day                build_portable.py  body (strips the 'Generated' line before comparing)
CODEMAP lists a file it should not                   codemap.py  publishable_py_files, SKIP_DIRS
CODEMAP misses a method / nested function            codemap.py  describe_file (only top level + one class level)
CODEMAP not updating by itself                       codemap.py  watch / snapshot (and the pythonw startup shortcut)
Watcher uses too much CPU                            codemap.py  DEFAULT_CPU_BUDGET or --cpu-budget
search_code result too long/short                    helper_server.py  RESULT_BUDGET_TOKENS, MIN_MATCHES_SHOWN (top of file)
a file is readable that should be private            helper_server.py  publishable_files (and .gitignore, see section 8)
read_lines refuses a valid path                      helper_server.py  read_lines (the resolve/relative_to check)
server hangs in Claude Desktop                       helper_server.py  debug/logged -> read _local/helper_debug.log; run selftest.py
token numbers look wrong                             token_tools.py  count_tokens, DEFAULT_ENCODING
report suggests a bad max_tokens                     token_tools.py  percentile, run_report
CSV log has wrong columns                            token_tools.py  FIELDS, log_call
'''

'''
3. build_portable.py  (builds projects/<slug>/PORTABLE.md)

Purpose: one self-contained file an AI on any platform can open by raw URL, instead of crawling
directories. It is plain text assembly: no AI, no tokens. Triggered by hand (python scripts/build_portable.py)
or by the git pre-commit hook (per the file's docstring), so PORTABLE.md is always fresh at commit time.

Modules and what each does here:
    pathlib.Path    every path; ROOT / "projects" joins; read_text; rglob; relative_to
    subprocess      one call: git config --get remote.origin.url
    re              pull "owner/name" out of the remote URL
    datetime.date   date.today().isoformat() for the "Generated <date>" line

Module-level constants (top of file):
    ROOT, PROJECTS, CONTEXT      folder/file locations
    REPO = repo_slug()           runs git when the file is imported, not only when run (so importing it needs git + a remote)
    RAW = https://raw.githubusercontent.com/<REPO>/main      base of every link in PORTABLE.md
    LOG_TAIL = 10                how many LOG lines to include
    KEEP_SECTIONS = ("Who", "Rules for AI", "How to log")    which '## ' sections of AI-CONTEXT.md are copied
    LIST_DIRS = ("docs", "notes"), LIST_EXT = {".md", ".txt"}    which project files get listed as links

Functions, in the order they run:
    repo_slug() L22
        subprocess.run(["git","config","--get","remote.origin.url"], cwd=ROOT, capture_output=True, text=True).stdout
        regex (written in the file as a raw string r"..."): github, an escaped dot, com, then [:/] (.+?) (?: dot-git )? and $
            [:/]        matches both https://github.com/owner/name and git@github.com:owner/name
            (.+?)       lazy group = owner/name, stops as early as the next part allows
            (?: .git )? optional ".git" that is matched but NOT captured, so it is dropped
            the file uses r"..." (raw string) so Python does not treat the backslash-dot as its own escape
        m.group(1) = owner/name. No match -> SystemExit with a message (the script stops, no traceback).
        Why: the repo can be renamed without breaking links, nothing is typed in by hand.
    read(path) L40
        text of a file, or "" if it does not exist (so a missing LOG.md never crashes the build).
    context_sections() L44
        a small state machine over AI-CONTEXT.md lines:
            line starts with "## "  -> the previous section (if we were keeping it) is saved; title = line[3:];
                                       keep = title.startswith(KEEP_SECTIONS)   # startswith accepts a tuple of prefixes
            any other line          -> added to buf if keep is True
        the last section is saved after the loop ends (there is no following "## " to trigger the save).
        Returns the kept sections joined by blank lines, in file order. Prefix match: "Who" also matches "Whose ...".
    log_tail(project) L61
        keeps only LOG.md lines starting with "20" (the dated entries: 2026-...), returns the last LOG_TAIL.
        Empty -> "(no entries yet)".  "or" returns the right side when the left is an empty string.
    file_list(project) L66
        for docs/ and notes/ in the project: base.rglob("*") sorted, keep files with allowed suffix,
        rel = f.relative_to(ROOT).as_posix().replace(" ", "%20")  -> a URL-safe path, one "- RAW/rel" line each.
    build(project) L78
        one big f-string: header, 3 rules for the AI, context_sections(), "## STATE", state, "## LOG", log_tail, file_list.
        Returns text only; writing happens in main().
    body(text) L95
        the text minus any line starting with "Generated ". Used only to compare old vs new.
        Without it the date line changes daily and the file would be rewritten (and show in git) every day.
    main() L99
        for each folder in projects/ that has a STATE.md (sorted, so output order is stable):
            text = build(project); if body(old) == body(text): print "unchanged" and continue
            else open(target, "w", encoding="utf-8", newline="\n") and write, print "written ... ~N tokens"
        newline="\n" forces Unix line endings even on Windows so git does not see phantom changes.
        ~N tokens = len(text)//4 (rough 4 chars per token; helper_server uses the measured 3.85 instead).

To add a new section to PORTABLE.md: add its heading text to KEEP_SECTIONS (if it lives in AI-CONTEXT.md)
or add a new block inside the f-string in build().
'''

'''
4. codemap.py  (builds scripts/codemap/CODEMAP.md)

Purpose: a one-line-per-function index of every Python file git would publish, so an AI reads one
file and knows which file and line to open. Rewrites only when the content changed.

Modules and what each does here:
    ast             parses Python source into a tree WITHOUT running it (the heart of the script)
    os              os.walk (folder walking), os.replace (atomic swap of the output file)
    subprocess      git ls-files
    time            time.perf_counter (stopwatch), time.sleep, time.strftime
    argparse, sys   the command line (--watch, --cpu-budget) and sys.exit with an error message
    pathlib.Path    paths; Path(__file__).resolve().with_name("CODEMAP.md") = same folder, new name

Constants: REPO_ROOT (parents[2]), OUTPUT (the CODEMAP.md path), SKIP_DIRS (set of folder names never
scanned), DEFAULT_CPU_BUDGET = 0.01 (1% of one core, a stated choice).

Functions:
    find_py_files() L34          used ONLY by snapshot()
        os.walk(REPO_ROOT); subfolders[:] = [...] edits the list in place, which makes os.walk skip those folders.
        Not git-aware: it sees ignored .py files too (it only skips SKIP_DIRS).
    publishable_py_files() L46   used ONLY by build_map()
        git ls-files --cached --others --exclude-standard -z, output split on the NUL character.
        Keeps names ending .py, not inside SKIP_DIRS (SKIP_DIRS.intersection(Path(name).parts) is empty),
        and path.is_file() (skips files deleted but not yet committed).
        --cached = tracked files, --others = new untracked files, --exclude-standard = apply .gitignore to the "others".
    signature(node) L66
        "deposit(self, amount, note=None) L9": node.name, ast.unparse(node.args) rebuilds the parameter text,
        node.lineno is the line number. isinstance(node, ast.AsyncFunctionDef) adds the "async " prefix.
    describe_file(path) L72
        ast.parse(path.read_text(encoding="utf-8-sig")) -> tree. Errors (SyntaxError, UnicodeDecodeError,
        ValueError) are caught and reported as one line "(could not read: SyntaxError)" instead of crashing.
        Loops tree.body = top-level statements only:
            a function -> one line;  a class -> "class Name L<n>" then each method one level deeper.
        NOT listed: functions nested inside functions, classes nested in classes, module-level variables.
    build_map() L94
        for each publishable file: lines = describe_file(); if empty, count it as omitted (no functions = no value);
        header line shows "N files listed, M omitted"; returns the whole text.
    write_if_changed(text) L110
        if OUTPUT exists and equals text -> return False (nothing written).
        else write OUTPUT.with_suffix(".tmp") then os.replace(temp, OUTPUT): the swap is atomic, so an AI reading
        CODEMAP.md never sees a half-written file. (CODEMAP.tmp is in .gitignore for this reason.)
    snapshot() L123
        {path: (st_mtime_ns, st_size)} for every .py file. Two snapshots differ if any file was edited, added or deleted.
        FileNotFoundError is caught: a file can vanish between listing and stat().
    watch(cpu_budget) L135
        loop forever: time the snapshot (scan_seconds), interval = scan_seconds / cpu_budget, print it once,
        if snapshot != last: rebuild the map, then last = snapshot; sleep(interval).
        Snapshot is taken BEFORE building, so an edit made during the build is seen next round.
        OSError (file locked) -> message and retry next round (last is not updated).
    main() L159
        argparse: --watch (store_true flag), --cpu-budget (float). Validates 0 < budget <= 1.
        watch mode: wrapped in try/except KeyboardInterrupt so Ctrl+C prints "Stopped." Otherwise build once.

Runs unattended via pythonw (no console window) from the Startup folder; see files_cli_and_scripts_notes.py.
'''

'''
5. helper_server.py  (the foundations-helper MCP server)

Purpose: two read-only tools for Claude Desktop:
    search_code(query, glob)       case-insensitive text search over publishable files -> "path:line: text"
    read_lines(path, start, end)   only those lines of one file
They exist because the filesystem MCP can only read whole files. Claude Desktop launches this program
itself and talks over stdin/stdout, so the file must NEVER print(); logging goes to a file instead.

Modules and what each does here:
    mcp.server.MCPServer / FastMCP   the server framework (try/except import supports SDK 2.x and 1.x)
    fnmatch      glob matching on the path string (fnmatch.fnmatch(rel, "*.py"))
    functools    functools.wraps inside the logged decorator
    subprocess   git ls-files
    time, os, sys, shutil   timestamps and startup diagnostics (sys.executable, os.getcwd(), shutil.which("git"))

Constants and WHERE EACH NUMBER COMES FROM (rule: no invented constants):
    CHARS_PER_TOKEN = 4439/1153 = 3.85     measured with token_tools.py on AI-CONTEXT.md (estimate only: tiktoken is OpenAI's)
    RESULT_BUDGET_TOKENS = 1000            a choice: max cost of one tool result
    RESULT_BUDGET_CHARS = int(1000 * 3.85) = 3849
    MIN_MATCHES_SHOWN = 20                 a choice: at least 20 matches should fit
    LINE_CHARS = 3849 // 20 = 192          longest line shown per match so one huge line cannot eat the budget
    BINARY_CHECK_BYTES = 8000              same rule git uses: a NUL byte in the first 8000 bytes = binary
    server = MCPServer("foundations-helper")   the object the decorators register tools on
    DEBUG_LOG = _local/helper_debug.log    gitignored, so never published (temporary, for the Desktop hang)

Functions:
    debug(message) L56
        appends "HH:MM:SS message" to DEBUG_LOG; OSError is swallowed because logging must never break a tool call.
    logged(function) L66   (a decorator)
        returns wrapper() that logs "received", times the call with perf_counter, logs "returning N chars after X s",
        or logs the exception and re-raises it. @functools.wraps(function) copies the name, docstring and type hints
        onto wrapper: MCP builds the tool description and input schema from them, so without wraps the tool
        would be called "wrapper" with no description.
    publishable_files() L84
        returns {"scripts/x.py": Path(...)} for every publishable file. Same git command as codemap, plus
        stdin=subprocess.DEVNULL: git must not inherit the server's stdin (that is the pipe to Claude Desktop).
    read_text(path) L102
        opens in binary, returns None if b"\0" in the first 8000 bytes (binary), else decodes utf-8-sig with errors="replace".
    search_code(query, glob="") L115
        1 reject empty query  2 files = publishable_files()  3 needle = query.lower()
        4 for each file (sorted) matching glob: read_text, skip None/unreadable, enumerate(text.splitlines(), start=1),
          keep (path, line number, stripped line) where needle is in line.lower()
        5 no matches -> message  6 build rows "path:line: text[:192]" until the 3849-char budget is reached
          (always shows at least one), header says "N matches in M files (showing K; narrow with glob ...)".
        Cost note: it re-runs git and re-reads EVERY publishable file on every call (no cache).
    read_lines(path, start, end) L159
        safety first: target = (REPO_ROOT / path).resolve(); rel = target.relative_to(REPO_ROOT.resolve()).as_posix()
        -> ValueError means outside the repo -> refused. Then rel must be in publishable_files() (ignored/private = refused).
        Then checks 1 <= start <= end, binary, start within file length. last = min(end, len(lines)).
        Adds lines until the budget is reached, header "path lines a-b of N (stopped at the size cap; call again with start=b+1)".
    bottom: if __name__ == "__main__": debug("started: ..."); server.run()   # stdio transport

How a call flows:  Claude Desktop -> stdin -> MCP framework finds the tool by name -> logged wrapper
-> search_code/read_lines -> string returned -> stdout -> Claude. Setup and config: scripts/mcp_helper/README.md.
'''

'''
6. selftest.py  (tests helper_server.py without Claude Desktop)

Purpose: decide whether a problem is in the server or in the Desktop connection. It starts the server as a
child process and speaks MCP to it the way Desktop does.

Modules: asyncio (async/await, wait_for, run), mcp (ClientSession, StdioServerParameters, stdio_client), sys, time, pathlib.

Async basics used here:
    async def f(): ...        a coroutine function; calling it does not run it, it returns a coroutine
    await x                   run it and wait for the result, letting other things run meanwhile
    asyncio.run(main())       the one entry point that starts the event loop
    async with a as b:        like with, but setting up/closing needs await (opening/closing a connection)

Functions:
    step(label, coroutine) L25
        asyncio.wait_for(coroutine, 60) -> on asyncio.TimeoutError print "TIMEOUT" and return None (so a hang is
        reported, not waited on forever). Otherwise prints label, seconds, and the FIRST line of the result (110 chars max).
    call(session, name, **arguments) L39
        session.call_tool(name, arguments); result.content is a list of parts; joins the .text of the ones that have text.
    main() L44
        StdioServerParameters(command=sys.executable, args=[SERVER]) = "run this Python on helper_server.py"
        async with stdio_client(parameters) as (read_stream, write_stream): launches the child, gives two pipes
        async with ClientSession(read_stream, write_stream) as session: the MCP conversation
        steps: 1 initialize (connect, stops the test if it fails) 2 list_tools 3 search_code 4 read_lines 5 read_lines "../AI-CONTEXT.md"
Caveat: step 5 is meant to be refused, but step() prints "OK" whenever the call returns. Check that the printed
first line says "Error: path is outside the repo", not just OK.
'''

'''
7. token_tools.py  (measure tokens before optimizing)

Three subcommands, like git add / git commit:
    count   token_tools.py count AI-CONTEXT.md README.md   |  count --text "..."  |  --encoding
    log     token_tools.py log --label research --model gemini --input 1200 --output 800
    report  token_tools.py report [--percentile 95]
Setup: pip install tiktoken (OpenAI's tokenizer: exact for OpenAI models, an estimate for Claude/Gemini).

Modules: argparse (commands), csv (log file), math (ceil for percentile), collections.defaultdict (grouping),
datetime (timestamps), sys (sys.exit), pathlib, tiktoken (imported inside the function).

Constants: DEFAULT_LOG = _local/token_log.csv (gitignored), FIELDS = the 5 CSV column names,
DEFAULT_ENCODING = "o200k_base" (a choice, changeable with --encoding).

Functions:
    count_tokens(text, encoding_name) L33
        import tiktoken INSIDE a try so a missing install gives one friendly message (sys.exit) instead of a traceback;
        tiktoken.get_encoding (ValueError -> unknown encoding); len(encoding.encode(text, disallowed_special=())),
        and disallowed_special=() makes "<|endoftext|>" count as ordinary text instead of raising.
    run_count(args) L47
        builds items = [(name, text)] from files and/or --text, prints tokens | chars | words | chars/token for each
        (chars/token computed from that text), and a TOTAL when there is more than one item.
    log_call(label, model, input_tokens, output_tokens, log_path) L71
        creates the folder, remembers if the file is new, appends one row with csv.DictWriter (writes the header only
        for a new file). Written as a function so later API code can import it and call it after each request.
    run_log(args) L89            validates non-negative numbers, calls log_call, prints where it logged.
    read_log(log_path) L98       csv.DictReader -> list of dict rows; converts the two token columns to int; exits if no file/rows.
    percentile(values, pct) L111 nearest-rank: sorted, rank = ceil(pct/100 * n), value = ordered[rank - 1].
    run_report(args) L118
        totals and input/output split; token sinks = defaultdict(lambda: {"calls": 0, "total": 0}) grouped by label,
        printed biggest first with sorted(..., key=lambda item: item[1]["total"], reverse=True);
        max_tokens suggestion = percentile of the output_tokens, plus how many logged replies it would have cut off.
    build_parser() L151
        argparse.ArgumentParser + add_subparsers(dest="command", required=True); each add_parser(...) gets its own
        arguments and .set_defaults(func=run_xxx). Note dest="input_tokens" on --input so args.input_tokens works.
    main() L177
        args = build_parser().parse_args(); args.func(args)   # runs whichever run_xxx the command selected
'''

'''
8. ISSUES FOUND WHILE READING (check these)

1. PRIVACY: CODEMAP.md lists files under coursework/school/..., but .gitignore ignores coursework/school/.
   git ls-files --cached includes files that are already tracked even if .gitignore now matches them, so those
   files were almost certainly committed before the ignore rule was added. Consequence: they may be in the public
   repo, and helper_server.py can read them. Check with: git ls-files coursework
   Fix (you run it, then commit): git rm -r --cached coursework/school   (keeps the files on disk, stops tracking them).
   Note: they stay visible in older commits' history. The "(could not read: SyntaxError)" lines in CODEMAP disappear too.
2. codemap.py watch(): snapshot() uses find_py_files (not git-aware) but the map uses publishable_py_files, so editing an
   ignored .py triggers a rebuild that writes nothing. Harmless, only wasted work.
3. selftest.py: "OK" means the call returned, not that the result was right (see section 6 caveat).
4. build_portable.py: REPO = repo_slug() runs git at import time; the trailing comment on that line contains a
   stray fragment (BRANCH = "main") that is just comment text, safe but confusing.
5. token_tools.py run_report: if every logged row has 0 tokens, grand_total is 0 and the percent lines divide by zero.
6. helper_server.py search_code: no caching, so cost per call grows with repo size (fine now; watch it if the repo gets large).
'''
