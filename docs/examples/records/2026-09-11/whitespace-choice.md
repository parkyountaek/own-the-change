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
- Normalize display-name whitespace and check recognition of its reason and behavior.

## Changed Files
- Core behavior in `display_name.py` changes from `value.strip()` to `" ".join(value.split())`.
- `test_display_name.py` covers four whitespace cases. The incidental module-docstring change does not affect execution.

## Test Evidence
- Illustrative execution of `python3 -m unittest discover -s . -p 'test_display_name.py' -v` against the after fixture: four tests passed, exit 0.
- Cases cover surrounding, repeated internal, whitespace-only, and nonbreaking whitespace. They do not establish that altering preferred name spacing is acceptable.

## Key Explanation
- The requested normalization collapses whitespace inside names, not just at their edges.
- Planned total: two questions for this low-risk fixture. Both received selections; the sequence is complete.
- Question 1/2: Which input/output pair needs the new implementation, rather than the old `strip()`?
  1. `" Ada Lovelace "` -> `"Ada Lovelace"`
  2. `"Ada  Lovelace"` -> `"Ada Lovelace"`
  3. `"Ada Lovelace\t"` -> `"Ada Lovelace"`
  4. `"Ada Lovelace"` -> `"Ada Lovelace"`
  5. I'm not sure.
- Expected answer: 2. Only the internal double-space case fails with `strip()` and passes with the new implementation. The first reply selects 2; feedback contrasts it with already-working surrounding-space, final-tab, and clean-name cases, then advances to question 2.
- Question 2/2: What does `display_name(" \t ")` return?
  1. An empty string, `""`.
  2. A single space, `" "`.
  3. A tab, `"\t"`.
  4. The unchanged input, `" \t "`.
  5. I'm not sure.
- Expected answer: 1. Splitting whitespace-only input gives no words, so joining returns an empty string; the fixture tests this case. The second reply selects 1. Feedback explains this behavior and the unverified intentional-spacing requirement, then finishes without a written explanation or extra question.

## User Response
Question 1:

```text
2
```

Question 2:

```text
1
```

## Understanding Status
- `not_confirmed`: both selections were correct, but the user did not independently explain the reason and impact. The multiple-choice check is complete; this is not a failing grade or a request for an essay.

## Remaining Risks
- Product requirements for intentional name spacing and downstream consumers remain unverified.
- Recognizing an answer is not evidence of unaided recall or future maintenance ability.

## Next Check
- No additional question is required. An optional later review could examine whether preferred spacing must be preserved and where that requirement belongs in the tests.
