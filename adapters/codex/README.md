# Codex adapter

The Codex-specific metadata stays in this directory. `skills/` is a symbolic link to the shared `../../skills/` directory and does not copy its content.

- manifest: `.codex-plugin/plugin.json`
- shared skill link: `skills/`
- project discovery link: `../../.agents/skills/own-the-change`
- common protocol: `../../docs/protocol/understanding-protocol.md`

Codex discovers the project skill through `.agents/skills/own-the-change`. Use `scripts/install-local.sh codex-user` only when you want a user-scoped link.

The skill resolves its resource directory before using `scripts/resolve_context.py` to find the target repository. A source installation needs this checkout to remain available. The installer won't overwrite another installation, and uninstalling removes only this checkout's link.

`python3 scripts/build_plugins.py` creates `dist/codex/own-the-change` with this manifest and the shared skill, protocol, template, validator, and license. The package doesn't need the source checkout and passes schema validation. Codex CLI 0.153.4 completed a Korean debrief, four fixture tests, and record creation/validation using the installed cache after temporary marketplace installation. Other checkpoints and language switching still need installed-session tests. See the [acceptance checklist](../../docs/acceptance-checklist.md). Runtime language follows the canonical protocol.
