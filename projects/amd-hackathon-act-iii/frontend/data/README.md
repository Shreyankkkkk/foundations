# frontend/data

What the Streamlit app reads. Run `python scripts/sync_backend_data.py --source fake|real|demo` from `frontend/` to refresh it from the backend.

| File | Written by | What it is |
|---|---|---|
| `sop.json`, `notes.json` | backend | SOP steps and plant notes |
| `flags.json` | backend | Drift flags, each with its verified quote |
| `benchmark.json` | backend | Precision, recall and speed numbers |
| `amd.json` | backend (`publish.py`) | Cost and Evolus figures for the AMD page |
| `decisions.json` | front end | Approve/reject choices. Git-ignored |

Check `benchmark.json` before any demo, slide or submission: `judge_model` and `gpu` must not be null. A null means the numbers come from the pretend model and say nothing about the real one.
