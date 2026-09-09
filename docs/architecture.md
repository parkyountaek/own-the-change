# Small architecture

## Conclusion

Own The Change is a local learning aid that lives in a repository and needs no server. After an agent changes code, it gives the user a chance to explain the reason and risk in their own words, then stores that result in Markdown.

## Components

- `docs/protocol/understanding-protocol.md`: the only common learning-rule source for every agent.
- `skills/own-the-change/`: one shared skill bridge. It does not copy common rules.
- `adapters/claude-code/`: Claude Code manifest, commands, hook, and a link to the shared skill.
- `adapters/codex/`: Codex metadata and a link to the shared skill.
- `.agents/skills/` and `.cursor/skills/`: project discovery links to the same shared skill.
- `adapters/generic/`: guidance for another agent to use the canonical protocol.
- `templates/understanding-record.md`: the shared record template.
- `scripts/validate_record.py`: deterministic format validation only. It does not assess understanding.
- `docs/ai-understanding/YYYY-MM-DD/`: local records for actual work.

## Data flow

1. Before a task, the user may answer or skip the Plan Check questions.
2. After the task, the agent writes a Change Debrief from the actual `git diff` and actual test output.
3. The user answers at most three questions appropriate to the risk.
4. Without an answer, the agent records `not_confirmed`. With an important gap, it records `needs_follow_up`.
5. The validator checks only the file format. `confirmed` requires a human review of the user's answer and the supporting evidence.

## Extension boundary

Keep common rules only in `docs/protocol/understanding-protocol.md`. Each adapter links to it and documents only the invocation method supplied by that tool. A new agent starts from `adapters/generic/AGENT-INSTRUCTIONS.md` and uses the same canonical source.

## Non-goals

- Servers, accounts, databases, payments, or analytics dashboards
- API key requirements or transmission of source code, environment variables, secrets, or complete terminal logs
- Automatic code modification, deployment, merge, or pull-request approval
- Marking a record `confirmed` from passing tests or an agent self-assessment
- Sending reminders. The first version records `follow_up_at` for important changes only.
