---
task_id: whitespace-choice
date: 2026-09-11
record_kind: example
understanding_status: not_confirmed
risk_level: low
user_response_status: answered
response_mode: multiple_choice
evidence_status: available
diff_scope: Fictional before/after display_name fixture, not a user's project
follow_up_at: []
follow_up_reason: none
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
---

# Understanding record: whitespace-choice

Fictional example. All execution results and user replies below illustrate a scenario; they are not evidence of a real user's participation.

## Goal
- Normalize display-name whitespace and check recognition of the changed behavior.

## Changed Files
- Core behavior in `display_name.py` changes from `value.strip()` to `" ".join(value.split())`.
- `test_display_name.py` covers four whitespace cases; no incidental changes are in scope.

## Test Evidence
- Illustrative execution of `python3 -m unittest discover -s . -p 'test_display_name.py' -v` against the after fixture: four tests passed, exit 0.
- Cases cover surrounding, repeated internal, whitespace-only, and nonbreaking whitespace. They do not establish that altering preferred name spacing is acceptable.

## Key Explanation
- The requested normalization collapses whitespace inside names, not just at their edges.
- Question 1: What does `display_name("Ada   Lovelace")` return after this change?
  1. `"Ada   Lovelace"`, preserving the internal spaces.
  2. `"Ada Lovelace"`, with one internal space.
  3. `"AdaLovelace"`, without an internal space.
  4. I'm not sure.
- Expected answer: 2, because `split()` separates the words and `join()` inserts one space.
- The reply below selects option 2 for question 1. Feedback acknowledges the correct selection and explains the intentional-spacing risk, then ends the check without asking for a written reason or another answer.

## User Response
2

## Understanding Status
- `not_confirmed`: the choice was correct, but the user did not independently explain the reason and impact. The multiple-choice check is complete; this is not a failing grade or a request for an essay.

## Remaining Risks
- Product requirements for intentional name spacing and downstream consumers remain unverified.
- Recognizing an answer is not evidence of unaided recall or future maintenance ability.

## Next Check
- No additional question is required. An optional later review could examine whether preferred spacing must be preserved and where that requirement belongs in the tests.
