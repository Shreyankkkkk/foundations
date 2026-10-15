"""loader.py: reads data/sop.json and data/notes.json into Python lists and checks the fields.
Input: the two JSON files. Output: SOP steps and notes for matcher.py and pipeline.py.

Status: empty skeleton, code comes in the build stage listed in STATE.md.
"""

"""loader.py: reads sop.json and notes.json and checks they are in the right shape.

Same job as sensors.cpp in the sumo robot: raw values come in, clean values go out.
Every later stage can trust that each step and note has the fields it needs.
"""

import json

from src import config

# Fields every item must have. Source: the data contract (STATE.md).
STEP_FIELDS = ["sop_id", "step_id", "title", "text"]
NOTE_FIELDS = ["note_id", "date", "shift", "source", "text"]


def _read_json_list(path):
    """Open a JSON file and return its content, which must be a list."""
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"{path} should contain a list, got {type(data).__name__}")
    return data


def _check_fields(items, required, label, path):
    """Raise a clear error if any item is missing a required field."""
    for position, item in enumerate(items):
        missing = [name for name in required if name not in item]
        if missing:
            raise ValueError(
                f"{path}: {label} number {position + 1} is missing {missing}"
            )


def load_sop_steps(path=None):
    """Return the list of SOP steps (one dict per step)."""
    path = path or config.SOP_FILE
    steps = _read_json_list(path)
    _check_fields(steps, STEP_FIELDS, "step", path)
    return steps


def load_notes(path=None):
    """Return the list of shift notes (one dict per note)."""
    path = path or config.NOTES_FILE
    notes = _read_json_list(path)
    _check_fields(notes, NOTE_FIELDS, "note", path)
    return notes