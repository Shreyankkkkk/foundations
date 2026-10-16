"""Central settings. Every other file imports from here, so nothing is typed twice."""

import os
from pathlib import Path

# --- Folders -----------------------------------------------------------
# This file is backend/src/config.py.
# .parent = backend/src, .parent.parent = backend. So paths work on any computer.
BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BACKEND_DIR / "data"
DEMO_DIR = DATA_DIR / "demo"
OUTPUT_DIR = BACKEND_DIR / "output"
# The front end sits next to backend/ in Foundations and in the team repo.
FRONTEND_DATA_DIR = BACKEND_DIR.parent / "frontend" / "data"

# --- Input files (made by scripts/build_data.py) -----------------------
SOP_FILE = DATA_DIR / "sop.json"
NOTES_FILE = DATA_DIR / "notes.json"
ANSWER_KEY_FILE = DATA_DIR / "answer_key.json"

# --- Output files (names fixed by the data contract) -------------------
FLAGS_FILE = OUTPUT_DIR / "flags.json"
BENCHMARK_FILE = OUTPUT_DIR / "benchmark.json"

RUN_STATS_FILE = OUTPUT_DIR / "run_stats.json"
AMD_FILE = OUTPUT_DIR / "amd.json"  # made by src/evaluation/publish.py, read by the front end's AMD page
FAKE_OUTPUT_DIR = OUTPUT_DIR / "fake"

# --- Fixed numbers, each with its source -------------------------------
# Candidate steps the matcher keeps per note. Source: Team Playbook (F3).
TOP_STEPS_PER_NOTE = 3
# Randomness of the judge model; 0 = same answer every run.
# Source: backend plan decision, 2026-10-13.
TEMPERATURE = 0

# --- Settings that depend on the machine (environment variables) ------
# An environment variable is a named value stored in your terminal session,
# outside the code. We use them so addresses and keys never reach GitHub.
#   JUDGE_BASE_URL : address of the model server, e.g. our vLLM on the AMD machine
#   JUDGE_MODEL    : name of the model on that server
#   JUDGE_API_KEY  : key, only if the server needs one
# No default values on purpose: the model name is not chosen until the
# model page is checked, and the address is unknown until the AMD machine exists.
JUDGE_BASE_URL = os.environ.get("JUDGE_BASE_URL")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL")
JUDGE_API_KEY = os.environ.get("JUDGE_API_KEY")

# Not set yet (PLACEHOLDER): retry limit and request timeout.
# They come from measured run times on the AMD machine; add them here then.


def require_judge_settings():
    """Stop with a clear message if the model address or name is missing."""
    missing = [
        name
        for name, value in (
            ("JUDGE_BASE_URL", JUDGE_BASE_URL),
            ("JUDGE_MODEL", JUDGE_MODEL),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing environment variable(s): " + ", ".join(missing)
        )