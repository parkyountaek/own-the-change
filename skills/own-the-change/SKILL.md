---
name: own-the-change
description: Run a local-first Plan Check, Change Debrief, or Understanding Check for AI-made code changes. Use actual local diff and test evidence only. Do not auto-edit code, score the user, approve a PR, or send repository data externally.
---

First locate `docs/protocol/understanding-protocol.md` relative to this SKILL.md: it is two directories above this file, then under `docs/protocol/`. It is the only common learning-rule source. This matters when the skill is installed for a user but the current working directory is another project.

Use a checkpoint only when the user requests it or explicitly invokes this skill. Keep the answer action-first: show the current conclusion or next small action first, then use numbered steps when needed. For a Change Debrief, inspect the current target repository's actual `git diff` and actual test output. Do not invent test results or execution metadata.

The target repository is the current working directory. Write its record to `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`. Read the template and run the validator from this skill's repository, also two directories above this SKILL.md: `templates/understanding-record.md` and `scripts/validate_record.py`. Never use `confirmed` without a user answer that explains the important reason and impact or risk. Keep unavailable provider, model, turn, token, and cost values as `unknown`.
