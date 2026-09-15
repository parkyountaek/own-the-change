# Repository development instructions

Read [the understanding protocol](docs/protocol/understanding-protocol.md) before running a checkpoint or changing learning behavior. It is the only source of common learning, record, and privacy rules; agent entry points must link to it instead of copying those rules.

Write repository documentation, instructions, comments, examples, and test descriptions in English.

## What this repository is

Own The Change is a local-first learning plugin: after an agent changes code it runs a Plan Check, a Change Debrief, and an optional multiple-choice Understanding Check, with optional Markdown records. No server, no account, no API key. See [the architecture overview](docs/architecture.md) for the component map.

## Where to change what

- Learning, record, privacy, status, and language rules: `docs/protocol/`
- Shared skill body used by every host: `skills/own-the-change/SKILL.md`
- Named checkpoint skills (Codex package only): `skills/own-plan-check/`, `skills/own-change-debrief/`, `skills/own-understanding-check/`, `skills/own-demo/`, `skills/own-doctor/`
- Claude Code commands, hook, and manifest: `adapters/claude-code/`; Codex metadata: `adapters/codex/`; other agents: `adapters/generic/`
- Python helpers (standard library only): `scripts/`; their tests: `tests/`

Every skill and command body stays within 250 characters. If a change would duplicate a protocol rule elsewhere, change the protocol instead.

## Generated files you must not hand-edit

`plugins/claude-code/own-the-change/`, `plugins/own-the-change/`, `.claude-plugin/marketplace.json`, and `.agents/plugins/marketplace.json` are tracked build output. Edit the canonical input, run `python3 scripts/sync_marketplace.py`, and commit the refreshed copies with the source change. CI fails on a stale copy.

`.agents/skills/own-the-change` and `.cursor/skills/own-the-change` are discovery links to the shared skill, not separate copies. `dist/` and `docs/ai-understanding/` are ignored. Never commit a real local record, a private path, or a secret; public examples stay fictional.

## Checks

For implementation changes, inspect the actual Git diff and run these from the repository root:

```sh
python3 scripts/sync_marketplace.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_record.py docs/examples/records/*/*.md
git diff --check
```

Validate changed example records with `python3 scripts/validate_record.py <record>`. The protocol specifies the validation workflow for actual local records.

`scripts/build_plugins.py` refuses to write into an existing directory, so give it a path that does not exist yet (`--output dist/check-$(date +%s)`) or remove the previous output first. It defaults to `dist/`, which usually already exists locally.

Lint matches CI:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m ruff check scripts tests
.venv/bin/shellcheck scripts/install-local.sh adapters/claude-code/hooks/suggest-debrief.sh
```

Automated tests cannot check host behavior. For a real session, follow [the host smoke test](docs/host-smoke-test.md) and say plainly when you did not run one.

## Repository-specific traps

- Maintained text must be English. A test scans tracked files for CJK characters, so localization fixtures use Unicode escapes.
- A test resolves every relative Markdown link; a renamed file breaks documentation before it breaks code.
- Claude and Codex plugin manifests must declare the same version, or the build fails.
- `validate_record.py` checks record structure only. It never establishes that someone understood a change, and passing tests never justify a `confirmed` status.
- Report what you actually ran. Do not present an agent review as human review.

## Commit attribution

When Codex materially assists a new commit, preserve the human author and existing trailers, and include `Co-authored-by: Codex <noreply@openai.com>` after a blank line in the commit message. See [AI attribution](CONTRIBUTORS.md#ai-development-assistance). Do not rewrite published history solely to add attribution.
