---
task_id: authorization-guard
date: 2026-09-09
understanding_status: needs_follow_up
risk_level: high
follow_up_at: 2026-09-10, 2026-09-16 - explain the authorization boundary again
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
---

# Understanding record: authorization-guard

## Goal
- Allow only administrators to change settings.

## Changed Files
- `src/authz.py`
- `tests/test_authz.py`

## Test Evidence
- Ran `python3 -m unittest tests/test_authz.py -v`; it passed.

## Key Explanation
- Added a role check before a settings change. The request is rejected when the user is not an administrator.

## User Response
- "It stops non-administrators from changing settings."

## Understanding Status
- `needs_follow_up`: the user did not explain why hiding a button is insufficient or why the server must enforce the rule.

## Remaining Risks
- The unit test does not cover a real login token that contains an incorrect role.

## Next Check
- On the next day and one week later, explain the difference between interface protection and server protection without reading the code.
