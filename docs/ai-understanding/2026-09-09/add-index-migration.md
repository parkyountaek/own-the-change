---
task_id: add-index-migration
date: 2026-09-09
understanding_status: confirmed
risk_level: high
follow_up_at: 2026-09-10, 2026-09-16 - explain database migration rollback and impact again
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
---

# Understanding record: add-index-migration

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
- "Reads may become faster, but adding or updating an order now has index maintenance cost. If it causes a problem, a rollback migration should remove the index."

## Understanding Status
- `confirmed`: the user explained the reason, write cost, and rollback risk in their own words, and that explanation matches the change.

## Remaining Risks
- Performance has not been measured against production-sized data.

## Next Check
- On the next day and one week later, explain when to roll back the index and in what deployment order.
