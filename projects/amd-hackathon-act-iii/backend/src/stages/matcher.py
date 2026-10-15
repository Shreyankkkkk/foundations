"""matcher.py: for one note, picks the 3 most likely SOP steps by shared-word scoring (plain Python, no model).
Input: a note and all SOP steps. Output: top 3 steps that judge.py will see.

Status: empty skeleton, code comes in the build stage listed in STATE.md.
"""
"""matcher.py: for one note, picks the SOP steps most likely to be about it.

Plain Python, no AI. It exists so the judge model only reads 3 steps
instead of all 32, which is faster and gives it fewer chances to get confused.

How it scores: every word the note and a step share earns points.
A word found in many steps (like "the") earns few points; a word found in
only one step (like "isolator") earns many. So rare shared words decide.
    points for one shared word = 1 / (number of steps containing that word)
This weighting is computed from the data itself, so there is no typed-in
list of "unimportant words".
"""

import re

from src import config


def _words(text):
    """Lowercase text -> the set of words in it. 'Lock, tag!' -> {'lock', 'tag'}."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def pick_candidate_steps(note, steps, top_n=None):
    """Return the top_n steps that best match the note, best first.

    Steps that share no word with the note are never returned, so the
    result can be shorter than top_n, or empty.
    """
    top_n = top_n or config.TOP_STEPS_PER_NOTE

    # Words of each step (title + text), in the same order as `steps`.
    step_words = [_words(step["title"] + " " + step["text"]) for step in steps]

    # For each word: in how many steps does it appear?
    steps_with_word = {}
    for words in step_words:
        for word in words:
            steps_with_word[word] = steps_with_word.get(word, 0) + 1

    note_words = _words(note["text"])

    scored = []
    for step, words in zip(steps, step_words):
        score = sum(1 / steps_with_word[word] for word in note_words & words)
        if score > 0:
            scored.append((score, step))

    # sorted() keeps file order when scores tie.
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [step for score, step in scored[:top_n]]