"""
repo_health.py - automatic repo audit. The git pre-commit hook runs it on every commit, so you
never have to run it yourself. It only warns; it never blocks a commit (exit code 0) unless you
run it by hand with --strict.

Checks:
  1. Tracked files that .gitignore now matches. They are inside git, so they can be public
     even though .gitignore says "never published".
  2. scripts/codemap/CODEMAP.md is current and lists no ignored path.
  3. Size of the files AI chats load every time, against budgets.

Manual run, if ever wanted:  python scripts/repo_health.py
"""
import argparse
import importlib.util
import subprocess
import sys
from collections import Counter
from pathlib import Path

# <repo>/scripts/repo_health.py -> repo root is 1 folder up.
REPO_ROOT = Path(__file__).resolve().parents[1]
CODEMAP_PY = REPO_ROOT / "scripts" / "codemap" / "codemap.py"

# Measured with scripts/token_tools on AI-CONTEXT.md: 4439 characters = 1153 tokens.
# An estimate: tiktoken is OpenAI's tokenizer, other models count differently.
CHARS_PER_TOKEN = 4439 / 1153  # = 3.85
# Budgets are choices, not measurements. Each is about 30% above what was measured on 2026-10-09,
# so normal growth passes quietly and a real jump gets flagged.
AI_CONTEXT_BUDGET_TOKENS = 1500   # measured 1,153 (x 1.3 = 1,499)
PORTABLE_BUDGET_TOKENS = 4000     # largest measured ~3,101, printed by build_portable.py (x 1.3 = 4,031)
# From AI-CONTEXT.md rule 12: "STATE.md stays under about 150 lines".
STATE_MAX_LINES = 150
# How many lines of a long list to show before summarising.
GROUPS_SHOWN = 4


def git_names(*options):
    """Names printed by git ls-files with the given options (null-separated, so any name splits correctly)."""
    result = subprocess.run(
        ["git", "ls-files", *options, "--exclude-standard", "-z"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise OSError(f"git ls-files failed: {result.stderr.strip()}")
    return set(result.stdout.split("\0")) - {""}


def tokens(path):
    return round(len(path.read_text(encoding="utf-8", errors="replace")) / CHARS_PER_TOKEN)


# ---------- the three checks; each returns (warnings, ok_lines) ----------

def check_tracked_ignored(tracked_ignored):
    if not tracked_ignored:
        return [], ["no tracked file matches .gitignore"]
    # Group by the first two folders, so 85 files read as one line.
    groups = Counter("/".join(Path(name).parts[:2]) for name in tracked_ignored)
    shown = ", ".join(f"{folder} ({count})" for folder, count in groups.most_common(GROUPS_SHOWN))
    more = len(groups) - GROUPS_SHOWN
    if more > 0:
        shown += f", and {more} more"
    return [f"{len(tracked_ignored)} tracked file(s) match .gitignore, so they are in git and can be public: "
            f"{shown}. To stop tracking (files stay on your disk): git rm -r --cached <folder>"], []


def check_codemap(tracked_ignored):
    if not CODEMAP_PY.is_file():
        return [], ["code map not installed (scripts/codemap/codemap.py missing)"]
    # Load codemap.py as a module so its own build_map() gives the expected text.
    spec = importlib.util.spec_from_file_location("codemap", CODEMAP_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not module.OUTPUT.is_file():
        return ["CODEMAP.md does not exist yet. Run: python scripts/codemap/codemap.py"], []
    actual = module.OUTPUT.read_text(encoding="utf-8")
    warnings, ok = [], []
    # In the map, lines that start without a space are file paths.
    leaked = sorted(line for line in actual.splitlines() if line in tracked_ignored)
    if leaked:
        warnings.append(f"CODEMAP.md lists {len(leaked)} ignored paths (first: {leaked[0]}). "
                        f"Re-run: python scripts/codemap/codemap.py")
    if actual != module.build_map():
        warnings.append("CODEMAP.md is out of date. Re-run: python scripts/codemap/codemap.py")
    if not warnings:
        ok.append("CODEMAP.md is current and lists no ignored path")
    return warnings, ok


def check_sizes():
    warnings, parts = [], []
    context = REPO_ROOT / "AI-CONTEXT.md"
    if context.is_file():
        size = tokens(context)
        parts.append(f"AI-CONTEXT.md ~{size:,}/{AI_CONTEXT_BUDGET_TOKENS:,} tokens")
        if size > AI_CONTEXT_BUDGET_TOKENS:
            warnings.append(f"AI-CONTEXT.md is ~{size:,} tokens, over its {AI_CONTEXT_BUDGET_TOKENS:,} budget. "
                            f"It is loaded in every chat: trim it.")
    portables = sorted((REPO_ROOT / "projects").glob("*/PORTABLE.md"))
    if portables:
        sizes = {path.parent.name: tokens(path) for path in portables}
        biggest = max(sizes, key=sizes.get)
        parts.append(f"largest PORTABLE.md ~{sizes[biggest]:,}/{PORTABLE_BUDGET_TOKENS:,} tokens")
        for name, size in sizes.items():
            if size > PORTABLE_BUDGET_TOKENS:
                warnings.append(f"projects/{name}/PORTABLE.md is ~{size:,} tokens, over its "
                                f"{PORTABLE_BUDGET_TOKENS:,} budget. Shorten that project's STATE.md.")
    states = sorted((REPO_ROOT / "projects").glob("*/STATE.md"))
    if states:
        lines = {path.parent.name: len(path.read_text(encoding="utf-8", errors="replace").splitlines())
                 for path in states}
        longest = max(lines, key=lines.get)
        parts.append(f"longest STATE.md {lines[longest]}/{STATE_MAX_LINES} lines")
        for name, count in lines.items():
            if count > STATE_MAX_LINES:
                warnings.append(f"projects/{name}/STATE.md has {count} lines (rule: about {STATE_MAX_LINES}). "
                                f"Move history to LOG.md.")
    return warnings, ["sizes: " + "; ".join(parts)] if parts else []


# ---------- run ----------

def main():
    parser = argparse.ArgumentParser(description="Audit the repo for privacy and token-size problems.")
    parser.add_argument("--strict", action="store_true", help="exit with code 1 if there are warnings")
    args = parser.parse_args()

    try:
        tracked_ignored = git_names("--cached", "--ignored")
    except OSError as error:
        print(f"repo_health: skipped ({error})")
        return 0  # a broken check must never stop a commit

    warnings, ok = [], []
    for check in (lambda: check_tracked_ignored(tracked_ignored),
                  lambda: check_codemap(tracked_ignored),
                  check_sizes):
        try:
            found_warnings, found_ok = check()
        except Exception as error:  # one failing check must not hide the others
            found_warnings, found_ok = [f"a check crashed: {type(error).__name__}: {error}"], []
        warnings += found_warnings
        ok += found_ok

    print(f"repo_health: {len(warnings)} warning(s)" if warnings else "repo_health: all clear")
    for line in warnings:
        print(f"  ! {line}")
    for line in ok:
        # The sizes line is information, not a pass, because its numbers may be over budget.
        print(f"  {'info' if line.startswith('sizes:') else 'ok'} {line}")
    return 1 if (warnings and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
