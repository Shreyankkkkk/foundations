"""fake_model.py: a pretend model, so everything can be tested without the AMD GPU.

It has the same one method as the real model, ask(prompt) -> reply text, and
answers in the same fixed format judge.py expects (a JSON list).

How it "thinks": it reads the note and the first listed step out of the prompt,
looks for trigger words in the note's sentences, and flags the first step with
that sentence as the quote. Same note in, same reply out (no randomness).

To exercise the other stages it misbehaves on purpose, on fixed notes picked by
a checksum of the note text:
  - about 1 note in 5 gets an extra proposal with an INVENTED quote
    (quote_check must drop it)
  - about 1 note in 7 gets its reply wrapped in a ```json fence
    (parse_reply must cope)

Numbers from fake runs say nothing about the real model. Never put them in
the demo, slides or submission.
"""

import json
import re
import zlib

# (trigger words in a sentence, drift type). First match in this order wins.
TRIGGERS = [
    (("out of order", "afterwards", "before we"), "reordered_steps"),
    (("instead", "workaround", "borrowed", "used a"), "workaround_substitution"),
    (("outdated", "no longer", "impractical", "can't be done"), "sop_outdated_or_impractical"),
    (("unclear", "not sure", "confusing"), "sop_unclear"),
    (("skipped", "didn't", "did not", "without", "forgot", "no one"), "skipped_step"),
]

# One step line in the prompt: - sop_id "X", step_id 3 (title): text
STEP_LINE = re.compile(r'- sop_id "(.+?)", step_id (\d+) \(')

# Sentence ends at . ! or ? followed by whitespace
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def read_first_step(prompt):
    """Return (sop_id, step_id) of the first step listed in the prompt, or None."""
    match = STEP_LINE.search(prompt)
    if not match:
        return None
    return match.group(1), int(match.group(2))


def read_note_text(prompt):
    """Return the note text from the prompt (between 'Note:' and 'Reply with ONLY')."""
    start = prompt.find("\nNote:\n")
    end = prompt.find("\n\nReply with ONLY")
    if start == -1 or end == -1 or end < start:
        return ""
    return prompt[start + len("\nNote:\n") : end]


def find_trigger(note_text):
    """Return (drift_type, sentence) for the first trigger found, or None."""
    for sentence in SENTENCE_SPLIT.split(note_text.strip()):
        lowered = sentence.lower()
        for words, drift_type in TRIGGERS:
            if any(word in lowered for word in words):
                return drift_type, sentence.strip()
    return None


class FakeModel:
    def __init__(self, misbehave=True):
        # misbehave=False gives clean replies only (for tests that need them)
        self.misbehave = misbehave

    def ask(self, prompt):
        step = read_first_step(prompt)
        note_text = read_note_text(prompt)
        if step is None or not note_text:
            return "[]"
        sop_id, step_id = step

        proposals = []
        found = find_trigger(note_text)
        if found:
            drift_type, sentence = found
            proposals.append({
                "sop_id": sop_id,
                "step_id": step_id,
                "drift_type": drift_type,
                "quote": sentence,
                "confidence": 0.8,
            })

        # crc32 is the same on every run (Python's hash() is not), so runs repeat exactly.
        checksum = zlib.crc32(note_text.encode("utf-8"))
        if self.misbehave and checksum % 5 == 0:
            proposals.append({
                "sop_id": sop_id,
                "step_id": step_id,
                "drift_type": "skipped_step",
                "quote": "the crew deliberately ignored every safety rule",  # not in any note
                "confidence": 0.95,
            })

        reply = json.dumps(proposals)
        if self.misbehave and checksum % 7 == 0:
            reply = "```json\n" + reply + "\n```"
        return reply