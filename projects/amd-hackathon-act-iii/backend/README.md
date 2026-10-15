# Backend: Procedure Drift Finder

The backend reads a plant's written procedures (SOPs) and the notes its shifts write (handover, near-miss, maintenance). It finds notes where what happened differs from the procedure, and proves it with the exact quote from the note. The front end shows the results.

The data in this repo is **synthetic** (made up for the hackathon, no real plant data).

## How it works

```
sop.json + notes.json
        |
     loader          reads both files
        |
     matcher         for each note, picks the 3 most likely SOP steps (shared words, no AI)
        |
      judge          asks the AI model (open model on an AMD GPU via vLLM): does the note drift from these steps?
        |
   quote_check       plain code: is the model's quote really in the note? If not, the flag is dropped
        |
    flags.json  ---> front end shows it, a human approves or rejects
        |
    benchmark        compares flags with the answer key -> benchmark.json (accuracy numbers)
```

Drift types: `skipped_step`, `reordered_steps`, `workaround_substitution`, `sop_outdated_or_impractical`, `sop_unclear`.

## Folder map

Status: **DONE** = written and checked. **EMPTY** = placeholder file, code comes next.

```
backend/
├── README.md                  this file
├── requirements.txt           Python packages needed (EMPTY)
├── src/                       the program itself
│   ├── config.py              all constants in one place: model name, endpoint, limits (EMPTY)
│   ├── pipeline.py            the one command that runs every stage and writes flags.json (EMPTY)
│   ├── stages/                the steps a note passes through, in order
│   │   ├── loader.py          reads sop.json and notes.json (EMPTY)
│   │   ├── matcher.py         picks the 3 most likely SOP steps per note (EMPTY)
│   │   ├── judge.py           builds the prompt, calls the model, reads its reply (EMPTY)
│   │   └── quote_check.py     drops flags whose quote is not in the note (EMPTY)
│   ├── models/
│   │   └── fake_model.py      pretend model so everything can be tested without a GPU (EMPTY)
│   └── evaluation/
│       └── benchmark.py       accuracy test against the answer key (EMPTY)
├── scripts/                   tools you run by hand, not part of the pipeline
│   ├── build_data.py          generates the three data files from the note text inside it (DONE)
│   └── check_data.py          checks the data: counts, ids, quotes (DONE)
├── data/
│   ├── sop.json               3 SOPs, 32 steps (DONE)
│   ├── notes.json             200 shift notes: 25 with planted drift, 30 traps, 145 clean (DONE)
│   ├── answer_key.json        which note has which planted drift; only benchmark.py reads it (DONE)
│   └── demo/                  saved real results so the front end works without a GPU (filled Oct 15)
├── output/                    results of a run (flags.json, benchmark.json, log); not stored in git
├── tests/                     one test file per stage, named test_<stage>.py (EMPTY)
└── docs/
    └── amd-runbook.md         copy-paste commands for the AMD machine (EMPTY)
```

Rule of thumb: **`src/` is what runs, `scripts/` is what you run by hand, `data/` is what goes in, `output/` is what comes out, `tests/` proves it works.**

## File formats (agreed with the front end, do not change without asking)

| File | Fields |
|---|---|
| `sop.json` | `sop_id`, `step_id`, `title`, `text` |
| `notes.json` | `note_id`, `date`, `shift`, `source` (handover, near-miss or maintenance), `text` |
| `flags.json` | `flag_id`, `sop_id`, `step_id`, `note_id`, `date`, `shift`, `drift_type`, `quote`, `confidence` (0 to 1), `status` (pending, approved or rejected), `suggested_fix` (text or null) |
| `benchmark.json` | `precision`, `recall`, `quote_verified_rate`, `notes_per_minute`, `matcher_model`, `judge_model`, `gpu`, `false_alarms` (list) |

`answer_key.json` is internal and is not part of the front-end contract.

## Rules the code must follow

- Flag only what a note actually says. Silence is not evidence.
- Report on steps and shifts, never on people.
- Every flag carries an exact quote that appears word for word in the note (same words, same order, capitals and extra spaces ignored). Otherwise the flag is dropped.
- A human approves or rejects every flag. This tool is not a safety control.
- No API keys or server addresses in the repo.

## Working on it

**To change the data:** edit the text in `scripts/build_data.py`, run it, then run `check_data.py`. Do not edit the three JSON files by hand.

**To add or send a file:** use exactly the file name and folder from the map above (lowercase, words joined with underscores, for example `quote_check.py`). Send it in the team group with one line saying what it does. It gets placed in the right folder and committed.

**Good places for a second backend person to start**, because they don't need the AMD GPU:
- `src/evaluation/benchmark.py` and `tests/test_benchmark.py`: compare `flags.json` to `data/answer_key.json` and compute precision, recall and false alarms.
- Hand-written notes: realistic notes in the same format as `data/notes.json`, with a note of which SOP step each one drifts from (if any).

## Running it

Coming once the code is written and tested. This section will have the exact commands for a clean machine.

## Words used here

- **SOP**: standard operating procedure, the written steps for a job.
- **Drift**: what people actually do slowly moving away from the SOP.
- **Trap note**: a note that sounds like drift but is not, used to catch false alarms.
- **Matcher**: plain code that narrows each note down to 3 candidate SOP steps.
- **Judge**: the AI model that decides whether a note drifts from those steps.
- **vLLM**: the program that loads the model onto the AMD GPU and answers requests.
- **Endpoint**: the web address where the model answers.
- **Flag**: one detected drift: a note, an SOP step, a drift type and a quote.
- **Benchmark**: the accuracy test, our flags compared with the answer key.
