"""tests/test_loader.py: tests for loader.py, run with the fake model.

Status: empty skeleton, code comes in the build stage listed in STATE.md.
"""
import json

import pytest

from src import config
from src.stages.loader import load_notes, load_sop_steps


def count_in_file(path):
    """Count items by reading the file directly, so the test needs no typed-in number."""
    with open(path, encoding="utf-8") as file:
        return len(json.load(file))


def test_loads_every_step():
    assert len(load_sop_steps()) == count_in_file(config.SOP_FILE)


def test_loads_every_note():
    assert len(load_notes()) == count_in_file(config.NOTES_FILE)


def test_note_ids_are_unique():
    ids = [note["note_id"] for note in load_notes()]
    assert len(ids) == len(set(ids))


def test_missing_field_gives_clear_error(tmp_path):
    bad_file = tmp_path / "bad_notes.json"
    bad_file.write_text('[{"note_id": "N1"}]', encoding="utf-8")
    with pytest.raises(ValueError):
        load_notes(bad_file)


def test_item_that_is_not_an_object_gives_clear_error(tmp_path):
    bad_file = tmp_path / "bad_notes.json"
    bad_file.write_text('["just text"]', encoding="utf-8")
    with pytest.raises(ValueError):
        load_notes(bad_file)