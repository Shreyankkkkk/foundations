"""Processing stages for Procedure Drift Finder.

Reference: "Procedure Drift Finder | Repository Review" (Procedure_Drift_Finder_GitHub_Review.pdf,
October 15, 2026), Sections 2, 3 and 5.

Stages, run in sequence by ``src/pipeline.py``:

    loader.py       load_sop_steps(), load_notes()       reads and validates the JSON data
    matcher.py      pick_candidate_steps()               top SOP steps per note (no AI)
    judge.py        judge_note(), make_real_model()      asks the model, validates replies
    quote_check.py  quote_in_note()                      rejects quotes not found in the note

Orchestration lives in ``pipeline.py``; this file only exposes the stage
functions so they can be imported as ``from src.stages import judge_note``.

Open work (review, Section 7):
    - judge.py:   P0 - request timeout, retries, robust errors (currently placeholders).
    - matcher.py: P1 - measure whether the correct SOP step is in the top three.
"""

from .loader import load_notes, load_sop_steps
from .matcher import pick_candidate_steps
from .judge import judge_note, make_real_model
from .quote_check import quote_in_note

__all__ = [
    "load_sop_steps",
    "load_notes",
    "pick_candidate_steps",
    "judge_note",
    "make_real_model",
    "quote_in_note",
]