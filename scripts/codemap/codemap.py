"""
codemap.py - writes a short map of every function and class in the repo's Python files,
so an AI can find code by reading the map instead of opening many files.

    python scripts/codemap/codemap.py            # build the map once
    python scripts/codemap/codemap.py --watch    # keep it up to date automatically

Output: scripts/codemap/CODEMAP.md (committed, so any AI can read it from GitHub; rewritten only
when something changed). Only files git would publish are listed, so gitignored private folders
(coursework, _local, ...) never appear in it.

Watch mode checks file timestamps on a timer. The wait between checks is not a guess:
    interval = (time one check takes) / cpu_budget
so the watcher uses about cpu_budget of one CPU core (default 1%, a deliberate choice).
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# <repo>/scripts/codemap/codemap.py -> repo root is 2 folders up.
REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().with_name("CODEMAP.md")
# Folders never scanned: git data, caches, virtual environments, and _local (books, vendor files).
SKIP_DIRS = {
    ".git",
    "__pycache__",
    "_local",
    ".venv",
    "venv",
    "node_modules",
    "exercises",
    "tests",
}
DEFAULT_CPU_BUDGET = 0.01

# Non-Python source files indexed through Universal ctags, and the tag kinds worth listing.
CTAGS_EXTENSIONS = {
    ".ino",
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".cc",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".go",
    ".rs",
}
CTAGS_KINDS = {"function", "method", "class", "struct", "interface", "enum"}
PINE_EXTENSIONS = {".pine"}
# Pine definitions start at column 0: `name(args) =>`, `method name(...) =>`, `type Name`, and the
# indicator/strategy/library declaration. Indented `=>` lines are switch arms, so they are ignored.
PINE_DEF = re.compile(
    r"^(?:export\s+)?(?:(method)\s+)?([A-Za-z_]\w*)\s*\(([^)]*)\)\s*=>"
)
PINE_TYPE = re.compile(r"^(?:export\s+)?type\s+([A-Za-z_]\w*)")
PINE_DECL = re.compile(
    r"^(indicator|strategy|library)\s*\(\s*(?:title\s*=\s*)?[\"']([^\"']+)"
)

# ---------- finding and reading files ----------


def find_source_files():
    """All Python and ctags-supported files under the repo, skipping SKIP_DIRS, sorted."""
    wanted = tuple({".py"} | CTAGS_EXTENSIONS | PINE_EXTENSIONS)
    found = []
    for folder, subfolders, filenames in os.walk(REPO_ROOT):
        subfolders[:] = [name for name in subfolders if name not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(wanted):
                found.append(Path(folder) / filename)
    return sorted(found, key=lambda path: path.relative_to(REPO_ROOT).as_posix())


def git_names(*options):
    """Names printed by git ls-files with the given options (null-separated, so any name splits correctly)."""
    result = subprocess.run(
        ["git", "ls-files", *options, "--exclude-standard", "-z"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        # Windows only: stops a console window flashing each time the hidden watcher calls git.
        # The flag does not exist on other systems, so getattr falls back to 0 (no flag).
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    if result.returncode != 0:
        raise OSError(f"git ls-files failed: {result.stderr.strip()}")
    return set(result.stdout.split("\0")) - {""}


def publishable_files(extensions):
    """Files git would publish with one of the given extensions (same leak protection as before)."""
    names = git_names("--cached", "--others") - git_names("--cached", "--ignored")
    paths = []
    for name in names:
        if name.endswith(tuple(extensions)) and not SKIP_DIRS.intersection(
            Path(name).parts
        ):
            path = REPO_ROOT / name
            if path.is_file():
                paths.append(path)
    return sorted(paths, key=lambda path: path.relative_to(REPO_ROOT).as_posix())


def signature(node):
    """One line like: 'deposit(self, amount, note=None) L9'."""
    prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
    return f"{prefix}{node.name}({ast.unparse(node.args)}) L{node.lineno}"


def describe_file(path):
    """Lines describing the functions/classes in one file. Empty list = nothing to list."""
    try:
        # utf-8-sig drops the invisible BOM mark some editors put at the start of a file.
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    except (SyntaxError, UnicodeDecodeError, ValueError) as error:
        return [f"  (could not read: {type(error).__name__})"]
    functions = (ast.FunctionDef, ast.AsyncFunctionDef)
    lines = []
    for node in tree.body:  # only top-level statements
        if isinstance(node, functions):
            lines.append(f"  {signature(node)}")
        elif isinstance(node, ast.ClassDef):
            lines.append(f"  class {node.name} L{node.lineno}")
            for child in node.body:
                if isinstance(child, functions):
                    lines.append(f"    {signature(child)}")
    return lines


# ---------- building and writing the map ----------


def group_of(rel):
    """Map name for a file: projects/<name>/... -> <name>, otherwise its top-level folder."""
    parts = rel.split("/")
    if len(parts) == 1:
        return "root"
    return parts[1] if parts[0] == "projects" and len(parts) > 2 else parts[0]


def describe_pine_file(path):
    """Declaration, types and functions of one Pine Script file, with line numbers."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (UnicodeDecodeError, OSError) as error:
        return [f"  (could not read: {type(error).__name__})"]
    lines = []
    for number, line in enumerate(text.splitlines(), 1):
        if m := PINE_DECL.match(line):
            lines.append(f'  {m[1]} "{m[2]}" L{number}')
        elif m := PINE_TYPE.match(line):
            lines.append(f"  type {m[1]} L{number}")
        elif m := PINE_DEF.match(line):
            lines.append(
                f"  {'method ' if m[1] else ''}{m[2]}({m[3].strip()}) L{number}"
            )
    return lines


def build_map():
    py_files = publishable_files({".py"})
    pine_files = publishable_files(PINE_EXTENSIONS)
    sections = {}
    for path in py_files:
        lines = describe_file(path)
        if lines:
            sections[path.relative_to(REPO_ROOT).as_posix()] = lines
    for path in pine_files:
        lines = describe_pine_file(path)
        if lines:
            sections[path.relative_to(REPO_ROOT).as_posix()] = lines
    other, other_total, warning = describe_ctags_files()
    sections.update(other)
    omitted = len(py_files) + len(pine_files) + other_total - len(sections)
    groups = {}
    for name in sorted(sections):
        groups.setdefault(group_of(name), []).append(name)
    index = [
        f"# CODEMAP INDEX (auto-generated) | read only the map for your task | L<n> = line number, "
        f"may lag behind edits | {len(sections)} files listed, {omitted} omitted"
        + (f" | WARNING: {warning}" if warning else "")
    ]
    outputs = {}
    for group, names in sorted(groups.items()):
        fname = f"CODEMAP-{group.replace(' ', '-')}.md"
        body = [f"# CODEMAP {group} (auto-generated) | L<n> = line number"]
        for name in names:
            body.append(name)
            body.extend(sections[name])
        outputs[fname] = "\n".join(body) + "\n"
        index.append(f"{fname} | {len(names)} files")
    outputs["CODEMAP.md"] = "\n".join(index) + "\n"
    return outputs


def write_if_changed(outputs):
    """Write each map file only if it differs, and delete maps for groups that no longer exist."""
    changed = False
    for fname, text in outputs.items():
        target = OUTPUT.with_name(fname)
        if target.exists() and target.read_text(encoding="utf-8") == text:
            continue
        temp = target.with_suffix(".tmp")
        temp.write_text(text, encoding="utf-8")
        os.replace(temp, target)
        changed = True
    for stale in OUTPUT.parent.glob("CODEMAP-*.md"):
        if stale.name not in outputs:
            stale.unlink()
            changed = True
    return changed


# ---------- watch mode ----------


def snapshot():
    """{file: (last-modified time, size)} for every .py file. Changes when any file changes."""
    state = {}
    for path in find_source_files():
        try:
            info = path.stat()
        except FileNotFoundError:  # deleted between listing and checking
            continue
        state[str(path)] = (info.st_mtime_ns, info.st_size)
    return state


def watch(cpu_budget):
    last = None
    announced = False
    while True:
        started = time.perf_counter()
        current = (
            snapshot()
        )  # taken BEFORE building, so an edit during the build is caught next round
        scan_seconds = time.perf_counter() - started
        interval = scan_seconds / cpu_budget
        if not announced:
            print(
                f"One check takes {scan_seconds * 1000:.1f} ms, so checking every {interval:.2f} s "
                f"(about {cpu_budget * 100:g}% of one CPU core). Ctrl+C to stop."
            )
            announced = True
        if current != last:
            try:
                if write_if_changed(build_map()):
                    print(f"{time.strftime('%H:%M:%S')} map updated")
                last = current
            except OSError as error:  # e.g. file locked; try again next round
                print(f"Could not update map: {error}")
        time.sleep(interval)


def describe_ctags_files():
    """(lines per file, files scanned, warning) for non-Python sources, via Universal ctags."""
    names = [
        p.relative_to(REPO_ROOT).as_posix() for p in publishable_files(CTAGS_EXTENSIONS)
    ]
    if not names:
        return {}, 0, None
    try:
        result = subprocess.run(
            [
                "ctags",
                "--output-format=json",
                "--fields=+nS",
                "--sort=no",
                "--langmap=C++:+.ino",
                "-f",
                "-",
                "-L",
                "-",
            ],
            input="\n".join(names),
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except FileNotFoundError:
        return {}, len(names), "ctags not installed, non-Python files not listed"

    if result.returncode != 0:
        return {}, len(names), f"ctags failed: {result.stderr.strip()[:100]}"

    by_file = {}
    for line in result.stdout.splitlines():
        try:
            tag = json.loads(line)
        except ValueError:
            continue
        if tag.get("_type") != "tag" or tag.get("kind") not in CTAGS_KINDS:
            continue
        scope = f"{tag['scope']}::" if tag.get("scope") else ""
        by_file.setdefault(tag["path"], []).append(
            f"  {scope}{tag['name']}{tag.get('signature', '')} L{tag.get('line', '?')}"
        )
    return by_file, len(names), None


# ---------- command line ----------


def main():
    parser = argparse.ArgumentParser(
        description="Build a map of functions and classes."
    )
    parser.add_argument("--watch", action="store_true", help="keep the map up to date")
    parser.add_argument(
        "--cpu-budget",
        type=float,
        default=DEFAULT_CPU_BUDGET,
        help="share of one CPU core the watcher may use, e.g. 0.01 = 1%%",
    )
    args = parser.parse_args()
    if not 0 < args.cpu_budget <= 1:
        sys.exit("--cpu-budget must be above 0 and at most 1.")

    if args.watch:
        try:
            watch(args.cpu_budget)
        except KeyboardInterrupt:
            print("Stopped.")
    else:
        try:
            changed = write_if_changed(build_map())
        except OSError as error:
            sys.exit(f"Could not build the map: {error}")
        print(f"{'Wrote' if changed else 'Already up to date:'} {OUTPUT}")


if __name__ == "__main__":
    main()
