#!/usr/bin/env python3
"""Build projects/<slug>/PORTABLE.md for every project that has a STATE.md.

PORTABLE.md = rules for AI + STATE.md + last LOG lines + file list with raw URLs.
One self-contained file an AI on any platform can open by raw URL (no directory
crawling). Costs zero AI tokens: this is plain text assembly.

Run:  python scripts/build_portable.py
Also runs automatically from the git pre-commit hook.
Never edit PORTABLE.md by hand; edit STATE.md / LOG.md / AI-CONTEXT.md instead.
"""
from datetime import date
from pathlib import Path

import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
CONTEXT = ROOT / "AI-CONTEXT.md"

def repo_slug():
    """owner/name from the origin remote, so a repo rename can never break the links."""
    url = subprocess.run(["git", "config", "--get", "remote.origin.url"],
                         cwd=ROOT, capture_output=True, text=True).stdout.strip()
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    if not m:
        raise SystemExit("build_portable: cannot read the GitHub repo from remote.origin.url")
    return m.group(1)

REPO = repo_slug()  # read from .git/config, not typed in BRANCH = "main"
BRANCH = "main"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"
LOG_TAIL = 10
KEEP_SECTIONS = ("Who", "Rules for AI", "How to log")  # sections copied from AI-CONTEXT.md
LIST_DIRS = ("docs", "notes")
LIST_EXT = {".md", ".txt"}


def read(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


def context_sections():
    """Return the chosen '## ' sections of AI-CONTEXT.md, in file order."""
    out, keep, buf = [], False, []
    for line in read(CONTEXT).splitlines():
        if line.startswith("## "):
            if keep:
                out.append("\n".join(buf).rstrip())
            title = line[3:].strip()
            keep = title.startswith(KEEP_SECTIONS)
            buf = [line]
        elif keep:
            buf.append(line)
    if keep:
        out.append("\n".join(buf).rstrip())
    return "\n\n".join(out)


def log_tail(project):
    entries = [l for l in read(project / "LOG.md").splitlines() if l[:2] == "20"]
    return "\n".join(entries[-LOG_TAIL:]) or "(no entries yet)"


def file_list(project):
    rows = []
    for d in LIST_DIRS:
        base = project / d
        if base.exists():
            for f in sorted(base.rglob("*")):
                if f.is_file() and f.suffix.lower() in LIST_EXT:
                    rel = f.relative_to(ROOT).as_posix().replace(" ", "%20")
                    rows.append(f"- {RAW}/{rel}")
    return "\n".join(rows) or "(none)"


def build(project):
    slug = project.name
    state = read(project / "STATE.md").strip()
    return (
        f"# PORTABLE CONTEXT: {slug}\n"
        f"Generated {date.today().isoformat()} by scripts/build_portable.py. "
        f"Read-only copy; the source of truth is STATE.md / LOG.md in the repo.\n"
        f"Rule: if you cannot open a link below, say so and ask me to paste it. "
        f"Never claim to have read what you could not open.\n"
        f"If you cannot write files, give me log lines and STATE edits as text to paste.\n\n"
        f"{context_sections()}\n\n"
        f"---\n\n## STATE ({slug})\n\n{state}\n\n"
        f"---\n\n## LOG (last {LOG_TAIL} entries)\n\n{log_tail(project)}\n\n"
        f"---\n\n## Other files (open only if the task needs them)\n\n"
        f"{file_list(project)}\n"
    )

def body(text):
    """Text without the 'Generated <date>' line, so a new day alone never rewrites the file."""
    return "\n".join(l for l in text.splitlines() if not l.startswith("Generated "))

def main():
    for project in sorted(p for p in PROJECTS.iterdir() if p.is_dir()):
        if not (project / "STATE.md").exists():
            continue
        target = project / "PORTABLE.md"
        text = build(project)
        if body(read(target)) == body(text):
            print(f"unchanged  {target.relative_to(ROOT)}")
            continue
        with open(target, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"written    {target.relative_to(ROOT)}  ~{len(text) // 4} tokens")


if __name__ == "__main__":
    main()
