"""quote_check.py: plain-code check that the model's quote is really in the note.

This is what stops the model from inventing evidence (stage F5, never cut).
No AI here, just string handling.

Rule: the quote must appear in the note with the same words in the same order,
with nothing in between. Ignored: capitals, extra spaces and line breaks, curly
vs straight quotes, and punctuation at the edges of a word (a dropped full stop,
quote marks around the quote, a trailing "..."). NOT ignored: the words
themselves, their order, whole-word matching ("valve" is not "valves"), and
punctuation inside a word ("don't" is not "dont", "3.5" is not "35").
"""

import string

# Curly quotes and apostrophes become straight ones, so they compare equal.
CURLY_TO_STRAIGHT = str.maketrans(
    {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"'}
)

# Characters stripped from the start and end of each word:
# normal punctuation plus ellipsis, en dash and em dash.
EDGE_CHARS = string.punctuation + "\u2026\u2013\u2014"


def words_of(text):
    """Lowercase the text, split on any whitespace, strip edge punctuation from each word."""
    words = []
    for raw in text.translate(CURLY_TO_STRAIGHT).lower().split():
        word = raw.strip(EDGE_CHARS)
        if word:  # a lone "-" or "..." becomes empty and is skipped
            words.append(word)
    return words


def quote_in_note(quote, note_text):
    """True if the quote's words appear in the note, in order, with nothing in between."""
    if not isinstance(quote, str) or not isinstance(note_text, str):
        return False
    quote_words = words_of(quote)
    if not quote_words:
        return False  # an empty or punctuation-only quote proves nothing

    note_words = words_of(note_text)
    size = len(quote_words)
    # Slide a window of the quote's length over the note's words.
    for start in range(len(note_words) - size + 1):
        if note_words[start : start + size] == quote_words:
            return True
    return False