---
name: own-the-change
description: Use for a local-first Plan Check, Change Debrief, or Understanding Check after AI coding work. Do not use to auto-edit code, score users, approve a PR, or send repository data externally.
---

Read `$CLAUDE_PLUGIN_ROOT/../../docs/protocol/understanding-protocol.md` before acting. It is the only common learning-rule source.

Use the matching explicit command when the user asks for a checkpoint. Base a debrief only on the current repository's actual `git diff` and test output. Store records under `docs/ai-understanding/YYYY-MM-DD/` with the template at `$CLAUDE_PLUGIN_ROOT/../../templates/understanding-record.md`, then run the local validator.

Never mark `confirmed` without a user answer that explains the important reason and impact or risk. If runtime metadata is unavailable, preserve `unknown` for each unavailable metadata field.
