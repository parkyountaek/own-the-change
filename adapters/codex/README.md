# Codex adapter

The Codex-specific metadata stays in this directory. `skills/` is a symbolic link to the shared `../../skills/` directory and does not copy its content.

- manifest: `.codex-plugin/plugin.json`
- shared skill link: `skills/`
- project discovery link: `../../.agents/skills/own-the-change`
- common protocol: `../../docs/protocol/understanding-protocol.md`

Codex discovers the project skill through `.agents/skills/own-the-change`. Use `scripts/install-local.sh codex-user` only when you want a user-scoped link.
