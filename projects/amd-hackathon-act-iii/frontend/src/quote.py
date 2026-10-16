"""quote.py: finds a flag's quote inside its note, using the SAME rule as backend/src/stages/quote_check.py.
Rule: same words in the same order; capitals, extra spaces, curly quotes and edge punctuation are ignored.
Unlike the backend it also says WHERE the quote is, so the screen can highlight it. Keep both rules in sync."""
import re, string

CURLY = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"'})
EDGE = string.punctuation + "\u2026\u2013\u2014"

def _tokens(text):
    """(normalised word, start, end) for each word. Words that are only punctuation are skipped."""
    out = []
    for m in re.finditer(r"\S+", text):
        w = m.group().translate(CURLY).lower().strip(EDGE)
        if w:
            out.append((w, m.start(), m.end()))
    return out

def quote_span(note_text, quote):
    """(start, end) character positions of the quote in the note, or None if it is not there."""
    if not isinstance(note_text, str) or not isinstance(quote, str):
        return None
    q = [w for w, _, _ in _tokens(quote)]
    if not q:
        return None
    t = _tokens(note_text)
    for i in range(len(t) - len(q) + 1):
        if [w for w, _, _ in t[i:i + len(q)]] == q:
            return t[i][1], t[i + len(q) - 1][2]
    return None
