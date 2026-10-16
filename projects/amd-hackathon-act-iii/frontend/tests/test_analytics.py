"""Tests for the data handling in src/views/analytics.py (no screen is drawn). Run from frontend/."""
import pandas as pd

from views import analytics

SOP = [{"sop_id": "SOP-1", "step_id": 1, "title": "Lock out", "text": "Lock the machine."}]


def flag(flag_id, date, step_id=1):
    return {"flag_id": flag_id, "sop_id": "SOP-1", "step_id": step_id, "note_id": "N1", "date": date,
            "shift": "Day", "drift_type": "skipped_step", "quote": "q", "confidence": 0.9,
            "status": "pending", "suggested_fix": None}


def test_weeks_stay_in_order_across_new_year():
    f, _ = analytics._frame({"sop": SOP, "flags": [flag("a", "2026-12-28"), flag("b", "2027-01-11")]})
    assert list(f.week.diff().dropna()) == [2]  # 28 Dec and 11 Jan are two calendar weeks apart


def test_flag_for_a_step_missing_from_the_sop_still_gets_a_label():
    f, _ = analytics._frame({"sop": SOP, "flags": [flag("a", "2026-09-01", step_id=9)]})
    assert f.label.iloc[0] == "Unknown step"
    assert f.text.iloc[0] == ""


def test_week_label_shows_the_monday_of_that_week():
    thursday = pd.Period("2026-09-03", freq="W").ordinal
    assert analytics._week_label(thursday) == "w/c 31 Aug"
