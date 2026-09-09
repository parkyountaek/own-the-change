---
name: own-the-change
description: Run a local-first Plan Check, Change Debrief, or Understanding Check for AI-made code changes. Use only actual local diff and test evidence; never score a user, auto-approve understanding, auto-edit code, or send data externally.
---

Read `docs/protocol/understanding-protocol.md` before this workflow. It is the only common learning-rule source.

When explicitly invoked, ask which checkpoint the user wants: Plan Check, Change Debrief, or Understanding Check. Follow the linked protocol exactly. Use `templates/understanding-record.md` for a record at `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`, then run `python3 scripts/validate_record.py <record>`.

A Change Debrief must be grounded in the current local `git diff` and actual test output. Do not claim tests ran when they did not. Keep unavailable execution metadata as `unknown`. Never use `confirmed` if the user has not answered in their own words.
