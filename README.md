<h1 align="center">Own The Change</h1>

<p align="center">
  A local-first learning tool that turns AI-made code changes into knowledge you can explain and maintain.
</p>

<p align="center">
  Claude Code - Codex CLI - extensible to other agents - no server - no API key
</p>

## Why it exists

AI coding agents can make many changes quickly. A passing test does not mean you can later answer these questions:

- Why was this approach chosen?
- Which files and behavior did it affect?
- Which risks did the tests miss?
- Where would you start when it fails?

Own The Change does not score code quality or approve pull requests. It gives you a short chance to explain the real change in your own words, fills only the important gaps, and stores a local Markdown record.

## Flow

```text
Before work                     After work                        Later
Plan Check -> AI coding -> Change Debrief -> Understanding Record -> follow_up_at
expected change, risk, test     actual diff and test evidence     user explanation and risks    dates for important work
```

1. `Plan Check`: predict the files, risk, and needed test. Skipping an answer never blocks work.
2. `Change Debrief`: explain what changed, why, impact, and limits from the actual `git diff` and actual test output.
3. `Understanding Check`: listen to the user's explanation through at most three risk-appropriate questions.
4. `Understanding Record`: save the result at `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`.

## Safety rules

- Never use `confirmed` from a passing test or an agent self-assessment alone.
- When the user does not answer, use `not_confirmed` or `unknown`.
- Keep unavailable execution metadata as `unknown`: `provider`, `model`, `turn`, `token`, and `cost`.
- Do not send source code, environment variables, secrets, or complete terminal logs outside the local environment.
- Automatic code modification, deployment, merge, pull-request approval, and understanding scores are out of scope.

The [understanding protocol](docs/protocol/understanding-protocol.md) is the only common learning-rule source. Claude Code, Codex, and generic adapters link to it instead of copying it.

## Supported tools

| Tool | Delivery | Explicit invocation |
| --- | --- | --- |
| Claude Code | adapter manifest, commands, shared skill link, optional Stop hook | `/own-plan-check`, `/own-change-debrief`, `/own-understanding-check` |
| Codex CLI | `.agents/skills/` discovery link and adapter metadata | `$own-the-change` or a checkpoint request |
| Cursor and Copilot | discovery links to the shared skill | the tool's skill selection UI or a natural-language request |
| Other agents | generic integration notes | `adapters/generic/AGENT-INSTRUCTIONS.md` |

## Install and verify

### Shared verification

```sh
cd /path/to/own-the-change
python3 -m unittest discover -s tests -v
python3 scripts/validate_record.py docs/ai-understanding/*/*.md
```

### Claude Code

Try the adapter from the repository root:

```sh
claude --plugin-dir adapters/claude-code
```

Then invoke a command in the session:

```text
/own-plan-check
/own-change-debrief
/own-understanding-check
```

This loads the plugin only for the current session. Refer to the [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins) for version-specific permanent installation.

### Codex CLI

Codex automatically discovers `.agents/skills/own-the-change` in this repository. The path is a symbolic link to `skills/own-the-change/`, so no project installation is required.

```sh
scripts/install-local.sh codex-project
```

To make the skill available in every repository for this local user:

```sh
scripts/install-local.sh codex-user
```

Remove only the user-scoped installation:

```sh
scripts/install-local.sh remove-codex-user
```

Restart Codex if it does not discover a new skill. Locations and invocation follow the [Codex Skills documentation](https://developers.openai.com/codex/skills/).

## Understanding record

```yaml
---
task_id: authorization-guard
date: 2026-09-09
understanding_status: needs_follow_up
risk_level: high
follow_up_at: 2026-09-10, 2026-09-16 - explain the authorization boundary again
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
---
```

The body contains Goal, Changed Files, Test Evidence, Key Explanation, User Response, Understanding Status, Remaining Risks, and Next Check. Copy the [template](templates/understanding-record.md), then validate the record.

```sh
python3 scripts/validate_record.py docs/ai-understanding/YYYY-MM-DD/<task-id>.md
```

See the [low-risk](docs/examples/low-risk-change.md), [authorization](docs/examples/authentication-change.md), and [database](docs/examples/database-change.md) examples.

## Repository layout

```text
adapters/claude-code/  Claude Code manifest, commands, hook, and shared-skill link
adapters/codex/        Codex manifest and shared-skill link
adapters/generic/      generic agent integration notes
.agents/skills/        Codex and Copilot project discovery link
.cursor/skills/        Cursor project discovery link
skills/                one shared skill
/docs/protocol/        canonical learning rules and record schema
docs/research/         learning principles, research citations, and product hypotheses
docs/ai-understanding/ date-based local understanding records
templates/             record template
scripts/               installation helper and deterministic record validator
tests/                 validator and installation-layout tests
```

Read [architecture.md](docs/architecture.md) for the structure and deliberate non-goals.

## Research and output shape

The learning design draws from retrieval practice, self-explanation, faded support, cognitive load management, spaced practice, specific feedback, and the illusion of understanding. [Learning principles](docs/research/learning-principles.md) separates research facts from product hypotheses; the papers do not guarantee an effect in AI coding work.

The output style borrows the action-first, small-step, visible-progress principles from [i-have-adhd](https://github.com/ayghri/i-have-adhd). Own The Change is not an ADHD diagnosis or treatment product and does not copy that project's code or wording.

## Privacy

Own The Change has no server, account, database, payment system, or external SaaS. It requires no separate API key and uses your existing Claude Code or Codex login.

Local records should contain only the change summary needed for learning and the user's response. Do not store secrets or complete logs.

## Project status

The first version stays deliberately small: local records, format validation, Claude Code and Codex adapters, and date-based follow-up candidates for important changes. It intentionally does not send notifications, synchronize automatically, score understanding, or modify code.

## License

[MIT](LICENSE)
