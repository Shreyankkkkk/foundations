# backend/data

Input data for the pipeline. All of it is synthetic.

| File | What it is |
|---|---|
| `sop.json` | 3 SOPs, 32 steps (`sop_id, step_id, title, text`) |
| `notes.json` | About 200 notes: 25 with planted drift, 30 traps, the rest clean |
| `answer_key.json` | Which note has which planted drift; the benchmark scores against it |
| `demo/` | Saved copy of a run's output, used by the front end's Demo mode |

`scripts/build_data.py` generates these files and `scripts/check_data.py` checks them. Do not edit them by hand.
