---
name: own-the-change
description: Run a local-first Plan Check, Change Debrief, or Understanding Check for AI-made code changes. Use actual local diff and test evidence only. Do not auto-edit code, score the user, approve a PR, or send repository data externally.
---

Read `docs/protocol/understanding-protocol.md` before acting. It is the only common learning-rule source.

Use a checkpoint only when the user requests it or explicitly invokes this skill. Keep the answer action-first: show the current conclusion or next small action first, then use numbered steps when needed. For a Change Debrief, inspect the current repository's actual `git diff` and actual test output. Do not invent test results or execution metadata.

Use `templates/understanding-record.md` for a record at `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`. Run `python3 scripts/validate_record.py <record>` after writing it. Never use `confirmed` without a user answer that explains the important reason and impact or risk. Keep unavailable provider, model, turn, token, and cost values as `unknown`.
