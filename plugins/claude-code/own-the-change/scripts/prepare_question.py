#!/usr/bin/env python3
"""Order four evidence-authored choices by number (--order) or JSON stdin; never save a question."""

import argparse
import json
import random
import sys
import unicodedata


def prepare_order(previous, rng=None):
    """Return display order for authored choices 1 to 4, where choice 1 is the answer."""
    if (not isinstance(previous, list) or len(previous) > 4
            or any(type(value) is not int or value not in range(1, 5) for value in previous)):
        raise ValueError("Provide up to four previous answer positions, each from 1 to 4")
    rng = rng if rng is not None else random.SystemRandom()
    positions = [position for position in range(1, 5) if not previous or position != previous[-1]]
    position = rng.choice(positions)
    show = [2, 3, 4]
    rng.shuffle(show)
    show.insert(position - 1, 1)
    return {"show": show, "answer_position": position}


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
    order = prepare_order(payload["previous_positions"], rng)
    authored = [answer, *(choice for choice in choices if choice != answer)]
    return {"choices": [*(authored[number - 1] for number in order["show"]), unsure],
            "answer_position": order["answer_position"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    # Numbers only keep question text out of the command, so no host flags it.
    parser.add_argument("--order", action="store_true", help="order authored choices 1-4 (1 is the answer)")
    parser.add_argument("--previous", action="append", type=int, choices=range(1, 5), default=[],
                        help="an earlier correct-answer position in this checkpoint (repeatable)")
    args = parser.parse_args()
    if args.order:
        print(json.dumps(prepare_order(args.previous)))
        return 0
    if args.previous:
        parser.error("--previous requires --order")
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
