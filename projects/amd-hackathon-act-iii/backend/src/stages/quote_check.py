"""quote_check.py: plain-code check that the model's quote is really in the note.

This is what stops the model from inventing evidence (stage F5, never cut).
No AI here, just string handling.

Rule: the quote must appear in the note with the same words in the same order,
with nothing in between. Ignored: capitals, extra spaces and line breaks, curly
vs straight quotes, and punctuation at the edges of a word (a dropped full stop,
quote marks around the quote, a trailing "..."). NOT ignored: the words
themselves, their order, whole-word matching ("valve" is not "valves"), and
punctuation inside a word ("don't" is not "dont", "3.5" is not "35").

Three names for other files:
    quote_in_note(quote, note_text)  -> True or False
    find_quote(quote, note_text)     -> (start, end) character positions in the note, or None
    exact_quote(quote, note_text)    -> the note's own text for that span, or None

The pipeline stores exact_quote() as the flag's quote, so what the person reads
is the note's wording, not the model's copy of it. The front end (src/quote.py
there) uses the same rule to highlight it; keep both in sync.
"""

import re
import string

# Curly quotes and apostrophes become straight ones, so they compare equal.
CURLY_TO_STRAIGHT = str.maketrans(
    {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"'}
)

# Characters stripped from the start and end of each word:
# normal punctuation plus ellipsis, en dash and em dash.
EDGE_CHARS = string.punctuation + "\u2026\u2013\u2014"


def _tokens(text):
    """(normalised word, start, end) for every word. Positions refer to the ORIGINAL text."""
    tokens = []
    for match in re.finditer(r"\S+", text):
        word = match.group().translate(CURLY_TO_STRAIGHT).lower().strip(EDGE_CHARS)
        if word:  # a lone "-" or "..." becomes empty and is skipped
            tokens.append((word, match.start(), match.end()))
    return tokens


def words_of(text):
    """Lowercase the text, split on any whitespace, strip edge punctuation from each word."""
    return [word for word, _, _ in _tokens(text)]


def find_quote(quote, note_text):
    """(start, end) of the quote inside the note, or None if it is not there."""
    if not isinstance(quote, str) or not isinstance(note_text, str):
        return None
    quote_words = words_of(quote)
    if not quote_words:
        return None  # an empty or punctuation-only quote proves nothing

    note_tokens = _tokens(note_text)
    size = len(quote_words)
    # Slide a window of the quote's length over the note's words.
    for first in range(len(note_tokens) - size + 1):
        window = note_tokens[first : first + size]
        if [word for word, _, _ in window] == quote_words:
            return window[0][1], window[-1][2]
    return None


def quote_in_note(quote, note_text):
    """True if the quote's words appear in the note, in order, with nothing in between."""
    return find_quote(quote, note_text) is not None


def exact_quote(quote, note_text):
    """The note's own wording for the quote (punctuation attached to its words included), or None."""
    span = find_quote(quote, note_text)
    if span is None:
        return None
    start, end = span
    return note_text[start:end]
