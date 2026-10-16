"""Tests for src/data_loader.py: damaged decision files, saving, and missing data files. Run from frontend/."""
import json
from types import SimpleNamespace

import pytest

import data_loader


@pytest.fixture
def decisions(tmp_path, monkeypatch):
    path = tmp_path / "decisions.json"
    monkeypatch.setattr(data_loader, "DECISIONS", path)
    monkeypatch.setattr(data_loader, "get_data", SimpleNamespace(clear=lambda: None))  # the screen cache is not needed here
    return path


def test_missing_decisions_file_means_no_decisions(decisions):
    assert data_loader.read_decisions() == {}


def test_damaged_decisions_file_means_no_decisions(decisions):
    decisions.write_text("{not json", encoding="utf-8")
    assert data_loader.read_decisions() == {}


def test_decisions_file_that_is_not_an_object_means_no_decisions(decisions):
    decisions.write_text("[1, 2]", encoding="utf-8")
    assert data_loader.read_decisions() == {}


def test_save_decision_keeps_earlier_decisions(decisions):
    data_loader.save_decision("F1", "approved")
    data_loader.save_decision(2, "rejected")
    assert json.loads(decisions.read_text(encoding="utf-8")) == {"F1": "approved", "2": "rejected"}
    assert not decisions.with_suffix(".tmp").exists()  # the temp file was swapped in


def test_save_decision_replaces_a_damaged_file(decisions):
    decisions.write_text("{not json", encoding="utf-8")
    data_loader.save_decision("F1", "approved")
    assert json.loads(decisions.read_text(encoding="utf-8")) == {"F1": "approved"}


def test_amd_file_is_optional(tmp_path, monkeypatch):
    monkeypatch.setattr(data_loader, "D", tmp_path)
    amd = data_loader._read("amd")
    assert amd["cost_per_1000_notes"] is None and amd["evolus_blocks"] == []


def test_other_missing_file_names_the_file(tmp_path, monkeypatch):
    monkeypatch.setattr(data_loader, "D", tmp_path)
    with pytest.raises(data_loader.DataError, match="flags.json"):
        data_loader._read("flags")


def test_file_that_is_not_json_names_the_file(tmp_path, monkeypatch):
    (tmp_path / "notes.json").write_text("{oops", encoding="utf-8")
    monkeypatch.setattr(data_loader, "D", tmp_path)
    with pytest.raises(data_loader.DataError, match="notes.json"):
        data_loader._read("notes")
