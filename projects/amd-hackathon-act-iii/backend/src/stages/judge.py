"""judge.py: asks the AI model whether a note drifts from the SOP steps shown to it.

Same job as motors.cpp in the sumo robot: this is the one file that talks to
the outside thing (here the AI model, there the motors). Everything else
calls it through two names:

    judge_note(note, candidates, model)  -> list of proposed flags
    make_real_model()                    -> the model that talks to vLLM

A "model" here is any object with one method:   model.ask(prompt) -> reply text
The real model (RealModel below) and the pretend model (fake_model.py) both
have it, so this file works with either one and does not know which.
"""

import json

from src import config

# The only drift types allowed. Source: Team Playbook / data contract (STATE.md).
DRIFT_TYPES = [
    "skipped_step",
    "reordered_steps",
    "workaround_substitution",
    "sop_outdated_or_impractical",
    "sop_unclear",
]


def build_prompt(note, candidates):
    """Write the question the model will read: rules, the steps, the note, the reply format."""
    step_lines = []
    for step in candidates:
        step_lines.append(
            f'- sop_id "{step["sop_id"]}", step_id {step["step_id"]} '
            f'({step["title"]}): {step["text"]}'
        )
    steps_text = "\n".join(step_lines)

    return (
        "You compare one shift note from a factory against written procedure steps (SOP steps).\n"
        "Find where the note shows the procedure was NOT followed, or shows the procedure itself is wrong.\n"
        "\n"
        "Drift types:\n"
        "- skipped_step: a step was not done\n"
        "- reordered_steps: steps were done in a different order\n"
        "- workaround_substitution: something else was done instead of the step\n"
        "- sop_outdated_or_impractical: the step no longer fits reality or cannot be done as written\n"
        "- sop_unclear: the note shows the step is confusing or read in different ways\n"
        "\n"
        "Rules:\n"
        "- Only flag what the note actually says. If the note does not mention a step, that is NOT evidence.\n"
        "- If the note describes the work done correctly, flag nothing.\n"
        "- Talk about steps and shifts, never about blaming people.\n"
        '- The "quote" must be copied from the note exactly, word for word, with no changes.\n'
        "\n"
        f"SOP steps:\n{steps_text}\n"
        "\n"
        f"Note:\n{note['text']}\n"
        "\n"
        "Reply with ONLY a JSON list, no other text. Each item looks like:\n"
        '{"sop_id": "...", "step_id": 1, "drift_type": "...", "quote": "...", "confidence": 0.0}\n'
        "confidence is a number from 0 to 1. If there is no drift, reply with exactly: []"
    )


def parse_reply(reply_text):
    """Turn the model's reply text into a Python list. Raises ValueError if it is not a JSON list."""
    # Models sometimes add words or ```json fences around the list.
    # Keep only the part from the first '[' to the last ']'.
    start = reply_text.find("[")
    end = reply_text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"no JSON list in model reply: {reply_text[:200]!r}")
    return json.loads(reply_text[start : end + 1])


def is_valid_proposal(item, candidates):
    """True only if the item has every field, in the right form, and points at a step we showed."""
    if not isinstance(item, dict):
        return False
    needed = ["sop_id", "step_id", "drift_type", "quote", "confidence"]
    if any(name not in item for name in needed):
        return False
    shown = {(step["sop_id"], step["step_id"]) for step in candidates}
    if (item["sop_id"], item["step_id"]) not in shown:
        return False
    if item["drift_type"] not in DRIFT_TYPES:
        return False
    if not isinstance(item["quote"], str) or not item["quote"].strip():
        return False
    confidence = item["confidence"]
    # bool is a kind of int in Python, so rule it out explicitly.
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        return False
    return 0 <= confidence <= 1


def judge_note(note, candidates, model):
    """Ask the model about one note. Returns a list of proposed flags (can be empty).

    Invalid items are dropped here. A reply that is not a JSON list at all raises
    an error; pipeline.py catches it, records the note as failed and moves on.
    """
    if not candidates:
        return []  # nothing to compare the note against, so no call to the model
    reply_text = model.ask(build_prompt(note, candidates))
    items = parse_reply(reply_text)
    return [item for item in items if is_valid_proposal(item, candidates)]


class RealModel:
    """Talks to a vLLM server (or any server with the same OpenAI-style address)."""

    def __init__(self, base_url, model_name, api_key=None):
        # base_url normally ends in /v1, e.g. http://<machine-address>:8000/v1
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.api_key = api_key

    def ask(self, prompt):
        import requests  # imported here so fake-model runs do not need it installed

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        body = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config.TEMPERATURE,
        }
        # No timeout and no retry yet: both are PLACEHOLDERS until we have
        # measured how long one request takes on the AMD machine.
        response = requests.post(
            f"{self.base_url}/chat/completions", headers=headers, json=body
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def make_real_model():
    """Build the real model from the environment variables in config.py."""
    config.require_judge_settings()
    return RealModel(config.JUDGE_BASE_URL, config.JUDGE_MODEL, config.JUDGE_API_KEY)