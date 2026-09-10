---
name: own-the-change
description: Run a Plan Check, Change Debrief, or Understanding Check for AI-generated code changes and save a local learning record. Use when the user requests a checkpoint or an Own The Change workflow.
---

Resolve this SKILL.md's real path first, following symbolic links (for example with Python `pathlib.Path(...).resolve()`). The resolved file is `<resource-root>/skills/own-the-change/SKILL.md`, in either the source checkout or an installed package. Resolve resources from that root, not from a discovery alias or the target working directory.

Read `<resource-root>/docs/protocol/understanding-protocol.md`, including **Runtime language**, and use the sections relevant to the requested checkpoint. This is the only source of learning rules, record requirements, and privacy behavior.

For a requested checkpoint, run `python3 <resource-root>/scripts/resolve_context.py --target <current-working-directory>` to get the target Git root and absolute protocol, template, validator, and record-root paths. Use those bundled resources even when the target is another repository. Checkpoint selection, including bare invocations and setup-help requests, follows the protocol.
