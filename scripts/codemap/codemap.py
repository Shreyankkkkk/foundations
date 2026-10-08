"""
codemap.py - writes a short map of every function and class in the repo's Python files,
so an AI can find code by reading the map instead of opening many files.

    python scripts/codemap/codemap.py            # build the map once
    python scripts/codemap/codemap.py --watch    # keep it up to date automatically

Output: scripts/codemap/CODEMAP.md (gitignored, rebuilt only when something changed).

Watch mode checks file timestamps on a timer. The wait between checks is not a guess:
    interval = (time one check takes) / cpu_budget
so the watcher uses about cpu_budget of one CPU core (default 1%, a deliberate choice).
"""
import argparse
import ast
import os
import sys
import time
from pathlib import Path

# <repo>/scripts/codemap/codemap.py -> repo root is 2 folders up.
REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().with_name("CODEMAP.md")
# Folders never scanned: git data, caches, virtual environments, and _local (books, vendor files).
SKIP_DIRS = {".git", "__pycache__", "_local", ".venv", "venv", "node_modules"}
DEFAULT_CPU_BUDGET = 0.01


# ---------- finding and reading files ----------

def find_py_files():
    """All .py files under the repo, skipping SKIP_DIRS, sorted so the output is stable."""
    found = []
    for folder, subfolders, filenames in os.walk(REPO_ROOT):
        # Editing subfolders in place tells os.walk not to enter those folders.
        subfolders[:] = [name for name in subfolders if name not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".py"):
                found.append(Path(folder) / filename)
    return sorted(found, key=lambda path: path.relative_to(REPO_ROOT).as_posix())


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

def build_map():
    files = find_py_files()
    body = []
    omitted = 0
    for path in files:
        lines = describe_file(path)
        if not lines:
            omitted += 1  # no functions/classes: listing it would only cost tokens
            continue
        body.append(path.relative_to(REPO_ROOT).as_posix())
        body.extend(lines)
    header = (f"# CODEMAP (auto-generated, do not edit) | L<n> = line number, may lag behind edits | "
              f"{len(files) - omitted} files listed, {omitted} without functions/classes omitted")
    return "\n".join([header] + body) + "\n"


def write_if_changed(text):
    """Write the map only if it differs. Returns True if it wrote."""
    if OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") == text:
        return False
    # Write a temp file, then swap it in, so a reader never sees a half-written map.
    temp = OUTPUT.with_suffix(".tmp")
    temp.write_text(text, encoding="utf-8")
    os.replace(temp, OUTPUT)
    return True


# ---------- watch mode ----------

def snapshot():
    """{file: (last-modified time, size)} for every .py file. Changes when any file changes."""
    state = {}
    for path in find_py_files():
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
        current = snapshot()  # taken BEFORE building, so an edit during the build is caught next round
        scan_seconds = time.perf_counter() - started
        interval = scan_seconds / cpu_budget
        if not announced:
            print(f"One check takes {scan_seconds * 1000:.1f} ms, so checking every {interval:.2f} s "
                  f"(about {cpu_budget * 100:g}% of one CPU core). Ctrl+C to stop.")
            announced = True
        if current != last:
            try:
                if write_if_changed(build_map()):
                    print(f"{time.strftime('%H:%M:%S')} map updated")
                last = current
            except OSError as error:  # e.g. file locked; try again next round
                print(f"Could not update map: {error}")
        time.sleep(interval)


# ---------- command line ----------

def main():
    parser = argparse.ArgumentParser(description="Build a map of functions and classes.")
    parser.add_argument("--watch", action="store_true", help="keep the map up to date")
    parser.add_argument("--cpu-budget", type=float, default=DEFAULT_CPU_BUDGET,
                        help="share of one CPU core the watcher may use, e.g. 0.01 = 1%%")
    args = parser.parse_args()
    if not 0 < args.cpu_budget <= 1:
        sys.exit("--cpu-budget must be above 0 and at most 1.")

    if args.watch:
        try:
            watch(args.cpu_budget)
        except KeyboardInterrupt:
            print("Stopped.")
    else:
        changed = write_if_changed(build_map())
        print(f"{'Wrote' if changed else 'Already up to date:'} {OUTPUT}")


if __name__ == "__main__":
    main()
