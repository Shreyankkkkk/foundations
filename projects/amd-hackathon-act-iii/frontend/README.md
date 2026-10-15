# Frontend: Procedure Drift Finder

The front end shows what the backend finds: which SOP steps drift, the exact quote behind each flag, and a review queue where a human approves or rejects. It is a Streamlit app. All data is synthetic.

## How it works

```
data/*.json  (saved results)   or   backend endpoint (DRIFT_API_URL)
        |
   data_loader      Live if the endpoint answers, otherwise Demo; merges data/decisions.json
        |
      app            sidebar menu, Live/Demo banner, error handling
        |
      views          one function per screen, all styled by theme
        |
 decisions.json  <--- Review Queue saves approve / reject here
```

## Folder map

```
frontend/
├── README.md                  this file
├── requirements.txt           Python packages needed
├── Dockerfile                 linux/amd64 image, runs src/app.py
├── .streamlit/
│   └── config.toml            Streamlit settings
├── src/                       the program itself
│   ├── app.py                 entry point: sidebar menu, Live/Demo banner, error handling
│   ├── config.py              all constants in one place: paths, data keys, endpoint variable name
│   ├── theme.py               colours, font and shared styling (edit together)
│   ├── data_loader.py         Live endpoint or saved JSON, merges data/decisions.json
│   └── views/                 one file per group of screens
│       ├── analytics.py       Overview, Heat Strip, Benchmark, AMD and Evolus
│       └── review.py          Review Queue, Evidence Viewer, DRAFT SOP-fix box
├── scripts/                   tools you run by hand, not part of the app
│   └── make_fake_data.py      writes fake data in the agreed format into data/
├── data/                      what goes in: sop, notes, flags, benchmark, amd (.json), decisions.json
├── tests/                     one test file per module, named test_<module>.py (EMPTY)
└── docs/                      notes and guides (EMPTY)
```

Rule of thumb: **`src/` is what runs, `scripts/` is what you run by hand, `data/` is what goes in, `tests/` proves it works.**

## Run it

Run every command from the `frontend/` folder.

    python -m venv .venv
    .venv\Scripts\activate        (Mac/Linux: source .venv/bin/activate)
    pip install -r requirements.txt
    python scripts/make_fake_data.py      (only if data/ is empty)
    streamlit run src/app.py

## Run it in Docker (linux/amd64)

    docker build --platform linux/amd64 -t drift-finder .
    docker run --platform linux/amd64 -p 8501:8501 drift-finder

Open http://localhost:8501. Live mode reads the environment variable `DRIFT_API_URL` (never commit it).

## File formats

Same as the backend README. The front end reads `sop.json`, `notes.json`, `flags.json`, `benchmark.json`, plus `amd.json` (`endpoint_status`, `cost_per_1000_notes`, `evolus_api_calls`, `evolus_blocks`). `decisions.json` is written by the front end: `{"flag_id": "approved" | "rejected" | "pending"}`.

## Adding a screen

Write a function `def my_screen(d):` in a file under `src/views/`, then add its name to `PAGES` in `src/app.py` (or in that file's own `PAGES` dict, as `review.py` does). File names are lowercase with underscores.
