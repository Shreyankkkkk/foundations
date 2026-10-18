# backend/scripts

Tools you run by hand from `backend/`. They are not part of the pipeline.

| File | What it does |
|---|---|
| `build_data.py` | Generates the synthetic SOPs, notes and answer key into `data/` |
| `check_data.py` | Checks that the data files are consistent with each other |

    python scripts/build_data.py
    python scripts/check_data.py
