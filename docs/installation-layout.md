# Installation layout

## Local use

- Claude Code: `claude --plugin-dir adapters/claude-code`
- Codex: automatically discovers `.agents/skills/own-the-change` at the repository root
- Cursor: automatically discovers `.cursor/skills/own-the-change` at the repository root
- GitHub Copilot and other Agent Skills-compatible tools: use `.agents/skills/own-the-change`

The repository keeps one shared skill in `skills/own-the-change/`. Discovery paths are symbolic links only. The common rules live only in `docs/protocol/understanding-protocol.md`.

## Not published yet

`adapters/claude-code/.claude-plugin/marketplace.json` and `adapters/codex/.codex-plugin/plugin.json` are metadata for a possible future marketplace release. This repository currently does not publish or push externally; use the local paths above while developing.
