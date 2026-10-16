"""tests/test_quote_check.py: tests for quote_check.py, run with the fake model.

Status: empty skeleton, code comes in the build stage listed in STATE.md.
"""
"""Tests for src/stages/quote_check.py. Run from backend/:  pytest tests/test_quote_check.py"""

from src.stages.quote_check import exact_quote, find_quote, quote_in_note

NOTE = "Night shift: skipped the lockout step because the key was missing.\nUsed the spare key instead."


def test_exact_quote_passes():
    assert quote_in_note("skipped the lockout step", NOTE)


def test_capitals_are_ignored():
    assert quote_in_note("SKIPPED The Lockout STEP", NOTE)


def test_extra_spaces_and_line_breaks_are_ignored():
    assert quote_in_note("  skipped   the\nlockout step ", NOTE)
    assert quote_in_note("missing. Used the spare key", NOTE)  # crosses the line break


def test_whole_note_as_quote_passes():
    assert quote_in_note(NOTE, NOTE)


def test_invented_words_fail():
    assert not quote_in_note("skipped the lockout procedure", NOTE)


def test_changed_word_order_fails():
    assert not quote_in_note("lockout the skipped step", NOTE)


def test_words_with_something_in_between_fail():
    # "skipped" and "lockout" are both in the note, but not next to each other
    assert not quote_in_note("skipped lockout", NOTE)


def test_partial_word_fails():
    assert not quote_in_note("skip the lockout", NOTE)
    assert not quote_in_note("spare ke", NOTE)


def test_quote_longer_than_note_fails():
    assert not quote_in_note(NOTE + " and more words", NOTE)


def test_empty_or_blank_quote_fails():
    assert not quote_in_note("", NOTE)
    assert not quote_in_note("   \n ", NOTE)


def test_empty_note_fails():
    assert not quote_in_note("skipped", "")


def test_non_text_input_fails_instead_of_crashing():
    assert not quote_in_note(None, NOTE)
    assert not quote_in_note("skipped", None)
    assert not quote_in_note(123, NOTE)

def test_dropped_trailing_full_stop_passes():
    assert quote_in_note("the key was missing", NOTE)  # note says "missing."


def test_quote_marks_and_ellipsis_around_quote_pass():
    assert quote_in_note('"skipped the lockout step"', NOTE)
    assert quote_in_note("...skipped the lockout step...", NOTE)


def test_curly_and_straight_apostrophes_match():
    assert quote_in_note("the operator's note", "Checked the operator\u2019s note today.")


def test_punctuation_inside_a_word_must_match():
    assert not quote_in_note("did not", "The crew didn't do it.")  # "didn't" is one word
    assert not quote_in_note("set to 35", "Valve set to 3.5 bar.")
    assert not quote_in_note("the A12 pump", "Restarted the A-12 pump.")


def test_changed_word_still_fails_with_punctuation_ignored():
    assert not quote_in_note("skipped the lockout procedure.", NOTE)


def test_punctuation_only_quote_fails():
    assert not quote_in_note("...", NOTE)
    assert not quote_in_note("- , .", NOTE)


def test_find_quote_gives_positions_in_the_original_note():
    start, end = find_quote("SKIPPED the lockout STEP", NOTE)
    assert NOTE[start:end] == "skipped the lockout step"
    assert find_quote("skipped the lockout procedure", NOTE) is None


def test_exact_quote_returns_the_notes_own_wording():
    assert exact_quote("SKIPPED the   lockout step", NOTE) == "skipped the lockout step"
    assert exact_quote("operator's note", "Checked the operator\u2019s note today.") == "operator\u2019s note"


def test_exact_quote_keeps_punctuation_attached_to_the_notes_words():
    assert exact_quote("the key was missing", NOTE) == "the key was missing."
    assert exact_quote('"skipped the lockout step"', NOTE) == "skipped the lockout step"


def test_exact_quote_is_always_a_piece_of_the_note():
    quote = exact_quote("missing. Used the spare key", NOTE)  # crosses the line break
    assert quote == "missing.\nUsed the spare key"
    assert quote in NOTE


def test_exact_quote_is_none_when_the_quote_is_not_there_or_not_text():
    assert exact_quote("invented words", NOTE) is None
    assert exact_quote("", NOTE) is None
    assert exact_quote(None, NOTE) is None
    assert exact_quote("skipped", None) is None