#!/usr/bin/env python3
"""Shuffle four evidence-authored choices from JSON stdin; never save a question."""

import json
import random
import sys
import unicodedata


def prepare_question(payload, rng=None):
    required = {"choices", "answer", "unsure", "previous_positions"}
    if not isinstance(payload, dict) or set(payload) != required:
        raise ValueError("Provide choices, answer, unsure, and previous_positions only")
    choices, answer, unsure = payload["choices"], payload["answer"], payload["unsure"]
    if not isinstance(choices, list) or len(choices) != 4:
        raise ValueError("Provide exactly four content choices")
    if any(not isinstance(value, str) or not value.strip() for value in [*choices, answer, unsure]):
        raise ValueError("Choices, answer, and unsure must be nonempty strings")
    normalized = [unicodedata.normalize("NFKC", value).strip().casefold() for value in [*choices, unsure]]
    if len(set(normalized)) != 5:
        raise ValueError("Content choices and unsure must be distinct")
    if answer not in choices:
        raise ValueError("Answer must exactly match one content choice")
    previous = payload["previous_positions"]
    if (not isinstance(previous, list) or len(previous) > 4
            or any(type(value) is not int or value not in range(1, 5) for value in previous)):
        raise ValueError("Provide up to four previous answer positions, each from 1 to 4")
    rng = rng if rng is not None else random.SystemRandom()
    positions = [position for position in range(1, 5) if not previous or position != previous[-1]]
    position = rng.choice(positions)
    distractors = [choice for choice in choices if choice != answer]
    rng.shuffle(distractors)
    distractors.insert(position - 1, answer)
    return {"choices": [*distractors, unsure], "answer_position": position}


def main():
    try:
        raw = sys.stdin.read(32769)
        if len(raw) > 32768:
            raise ValueError("Question input is too large")
        result = prepare_question(json.loads(raw))
    except (ValueError, TypeError):
        # Do not echo potentially private question text in diagnostics.
        print("Invalid question JSON; check the prepare_question input contract", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
