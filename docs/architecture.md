# Architecture

## Overview

Own The Change is a local learning aid that needs no server. After an agent changes code, it explains the change and offers an optional multiple-choice Understanding Check, with optional Markdown storage. Independent explanation is an optional deeper mode.

## Components

- `docs/protocol/understanding-protocol.md`: the only common learning-rule source for every agent.
- `skills/own-the-change/`: the shared skill entry point. It refers to the protocol without copying its rules.
- `skills/own-change-debrief/`, `skills/own-plan-check/`, and `skills/own-understanding-check/`: thin named checkpoint entry points bundled only in the native Codex plugin. They select canonical protocol sections through the reader, with UI metadata for skill pickers.
- `adapters/claude-code/`: Claude Code manifest, commands, hook, and a link to the shared skill.
- `adapters/codex/`: Codex metadata and a link to the shared skill.
- `.agents/skills/` and `.cursor/skills/`: project discovery links to the same shared skill.
- `adapters/generic/`: guidance for another agent to use the canonical protocol.
- `templates/understanding-record.md`: the shared record template.
- `scripts/validate_record.py`: checks record format and consistency. It does not assess understanding.
- `scripts/resolve_context.py`: resolves source resources and a target Git root without writing files.
- `scripts/launch_claude.py`: builds a temporary plugin and starts a session in the user's project without registering a marketplace.
- `skills/own-demo/` and `skills/own-doctor/`: thin Codex setup actions; Claude exposes corresponding commands. Every skill/command body stays within 250 characters.
- `scripts/read_protocol.py`: selects complete verbatim sections from the canonical protocol for the requested mode. It fails on unmapped headings so new rules cannot silently disappear.
- `scripts/prepare_question.py`: stateless ordering of four evidence-authored content choices and an uncertainty choice; no model call, record, or semantic correctness claim.
- `scripts/doctor.py`: read-only prerequisites/resource checks, optionally using an exact target/record context.
- `scripts/prepare_demo.py`: prepares a fresh synthetic Git change without launching an agent or creating a learning record. The builder maps the three canonical smoke fixture files into bundled `assets/demo/` paths for both hosts.
- `scripts/build_plugins.py`: copies explicitly listed canonical inputs into self-contained host packages without symlinks, private records, or a second maintained rule source.
- `scripts/sync_marketplace.py`: refreshes or checks both tracked distributions against the canonical build.
- `.claude-plugin/marketplace.json` and `plugins/claude-code/own-the-change/`: generated Claude catalog and complete package for installation from GitHub.
- `.agents/plugins/marketplace.json` and `plugins/own-the-change/`: generated Codex catalog and native package for installation from the same repository.
- `docs/ai-understanding/YYYY-MM-DD/`: private local records for actual work, ignored by Git.
- `docs/examples/records/YYYY-MM-DD/`: explicitly fictional public fixtures.
- `dist/`: generated Claude Code and Codex packages, ignored by Git.

## Data flow

1. Before a task, the user may answer or skip the Plan Check questions.
2. After the task, the agent writes a Change Debrief from the actual `git diff` and actual test output.
3. A requested Understanding Check follows the [conversation rules](protocol/understanding-protocol.md#understanding-check), using a short risk-based multiple-choice sequence with visible progress, one question at a time.
4. The agent preserves the actual reply and response mode, and applies the [status rules](protocol/understanding-protocol.md#status) without treating recognition as independent explanation.
5. The validator checks structure, response/evidence presence, declared response-mode consistency, status agreement, and follow-up dates. It cannot establish understanding or the truth of the declared mode.

## Adding another agent

Keep common rules only in `docs/protocol/understanding-protocol.md`. Each adapter links to it and documents only the invocation method supplied by that tool. A new agent starts from `adapters/generic/AGENT-INSTRUCTIONS.md` and uses the same canonical source.

## Non-goals

- Servers, accounts, databases, payments, or analytics dashboards
- API key requirements or transmission of source code, environment variables, secrets, or complete terminal logs
- Automatic code modification, deployment, merge, or pull-request approval
- Marking a record `confirmed` from passing tests or an agent self-assessment
- Sending reminders. The first version records `follow_up_at` for important changes only.
