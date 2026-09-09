# Record schema

Store each record at `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`. Use the actual work date in `YYYY-MM-DD` form.

The opening YAML must contain every key below.

```yaml
task_id: short-kebab-case-id
date: YYYY-MM-DD
understanding_status: not_confirmed
risk_level: low
follow_up_at: none
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
```

Change `provider`, `model`, `turn`, `token`, or `cost` only when the execution tool supplied that value reliably. Keep any unavailable value as `unknown`. Do not infer past execution values from the current configuration or account-wide usage.

The body must include these headings:

- `## Goal`
- `## Changed Files`
- `## Test Evidence`
- `## Key Explanation`
- `## User Response`
- `## Understanding Status`
- `## Remaining Risks`
- `## Next Check`

Use `follow_up_at` only for important work. Include readable dates and a reason, for example: `2026-09-10, 2026-09-16 - explain the authorization boundary again`. Use `none` otherwise.
