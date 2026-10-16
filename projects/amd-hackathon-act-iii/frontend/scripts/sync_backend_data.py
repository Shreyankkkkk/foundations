"""sync_backend_data.py: copies the backend's data and results into frontend/data so the app shows real pipeline output.
Run from frontend/:
    python scripts/sync_backend_data.py --source fake    results of the pretend-model run (backend/output/fake/)
    python scripts/sync_backend_data.py --source real    results of the real run (backend/output/)
    python scripts/sync_backend_data.py --source demo    saved results (backend/data/demo/)
It copies sop.json and notes.json (inputs) plus flags.json and benchmark.json (results). amd.json is left alone."""
import argparse, shutil, sys
from pathlib import Path

FRONT = Path(__file__).resolve().parent.parent
BACK = FRONT.parent / "backend"
RESULTS = {"fake": BACK / "output" / "fake", "real": BACK / "output", "demo": BACK / "data" / "demo"}

def main():
    p = argparse.ArgumentParser(description="Copy backend data and results into frontend/data.")
    p.add_argument("--source", choices=RESULTS, default="fake", help="which results to copy (default: fake)")
    p.add_argument("--keep-decisions", action="store_true", help="keep data/decisions.json (flag ids restart each run, so old decisions usually no longer match)")
    a = p.parse_args()
    jobs = [(BACK / "data" / n, FRONT / "data" / n) for n in ("sop.json", "notes.json")] + [(RESULTS[a.source] / n, FRONT / "data" / n) for n in ("flags.json", "benchmark.json")]
    missing = [str(s) for s, _ in jobs if not s.exists()]
    if missing:
        sys.exit("Missing files, nothing copied:\n  " + "\n  ".join(missing) + "\nRun the backend pipeline first (see backend/README.md).")
    for s, t in jobs:
        shutil.copyfile(s, t); print(f"copied {s.relative_to(FRONT.parent)} -> {t.relative_to(FRONT.parent)}")
    dec = FRONT / "data" / "decisions.json"
    if dec.exists() and not a.keep_decisions:
        dec.rename(dec.with_name("decisions.backup.json")); print("old decisions saved as decisions.backup.json")

if __name__ == "__main__":
    main()
