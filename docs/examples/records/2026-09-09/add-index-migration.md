---
task_id: add-index-migration
date: 2026-09-09
record_kind: example
understanding_status: confirmed
risk_level: high
user_response_status: answered
evidence_status: available
diff_scope: Fictional migration change; no real Git diff was inspected
follow_up_at:
  - 2026-09-10
  - 2026-09-16
follow_up_reason: Review the index's effect on writes and how to roll it back
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
---

# Understanding record: add-index-migration

Fictional example. All source paths, execution results, and user quotations below are illustrative, not actual evidence.

## Goal
- Add an index to speed up frequent order-number lookups.

## Changed Files
- `migrations/20260909_add_order_index.sql`
- `tests/test_migration.sql`

## Test Evidence
- Ran `./scripts/test-migration.sh`; it exited with code 0.

## Key Explanation
- Added an index so the database does not need to scan every row for an order number. Inserts and updates must also maintain that index.

## User Response
- "Lookups should be faster, but adding or updating an order takes more work because the database has to update the index too. If it causes problems, we can remove the index with a rollback migration."

## Understanding Status
- `confirmed`: the user explained the reason, write cost, and rollback risk in their own words, and that explanation matches the change.

## Remaining Risks
- Performance has not been measured against production-sized data.

## Next Check
- Tomorrow and a week from now, explain when you would remove the index and how you would order the rollback steps.
