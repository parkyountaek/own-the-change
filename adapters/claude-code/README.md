# Claude Code adapter

The Claude Code implementation stays in this directory. It links to shared resources rather than copying their rules.

- manifest: `.claude-plugin/plugin.json`
- commands: `commands/`
- optional Stop hook: `hooks/`
- shared skill link: `skills/`
- common protocol: `../../docs/protocol/understanding-protocol.md`

Run it from the repository root with `claude --plugin-dir adapters/claude-code`.
