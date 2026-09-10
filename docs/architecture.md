# Architecture

## Overview

Own The Change is a local learning aid that lives in a repository and needs no server. After an agent changes code, it gives the user a chance to explain the reason and risk in their own words, then stores that result in Markdown.

## Components

- `docs/protocol/understanding-protocol.md`: the only common learning-rule source for every agent.
- `skills/own-the-change/`: the shared skill entry point. It refers to the protocol without copying its rules.
- `adapters/claude-code/`: Claude Code manifest, commands, hook, and a link to the shared skill.
- `adapters/codex/`: Codex metadata and a link to the shared skill.
- `.agents/skills/` and `.cursor/skills/`: project discovery links to the same shared skill.
- `adapters/generic/`: guidance for another agent to use the canonical protocol.
- `templates/understanding-record.md`: the shared record template.
- `scripts/validate_record.py`: checks record format and consistency. It does not assess understanding.
- `scripts/resolve_context.py`: resolves source resources and a target Git root without writing files.
- `scripts/launch_claude.py`: builds a temporary plugin and starts a session in the user's project without registering a marketplace.
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
3. The user answers at most three questions appropriate to the risk.
4. Without an answer, the agent records `not_confirmed`. With an important gap, it records `needs_follow_up`.
5. The validator checks structure, response/evidence presence, status agreement, and follow-up dates. Semantic decisions follow the [canonical status rules](protocol/understanding-protocol.md#status); validator success cannot establish understanding.

## Adding another agent

Keep common rules only in `docs/protocol/understanding-protocol.md`. Each adapter links to it and documents only the invocation method supplied by that tool. A new agent starts from `adapters/generic/AGENT-INSTRUCTIONS.md` and uses the same canonical source.

## Non-goals

- Servers, accounts, databases, payments, or analytics dashboards
- API key requirements or transmission of source code, environment variables, secrets, or complete terminal logs
- Automatic code modification, deployment, merge, or pull-request approval
- Marking a record `confirmed` from passing tests or an agent self-assessment
- Sending reminders. The first version records `follow_up_at` for important changes only.
