# Claude Code adapter

This directory contains the Claude Code package inputs. The shared skill link is an authoring shortcut; the build copies canonical resources into the actual plugin package.

- manifest: `.claude-plugin/plugin.json`
- commands: `commands/`
- optional Stop hook: `hooks/`
- shared skill link: `skills/`
- common protocol: `../../docs/protocol/understanding-protocol.md`

From the repository root, run `python3 scripts/build_plugins.py`, then load `claude --plugin-dir dist/claude-code/own-the-change`.

Commands use the plugin namespace: `/own-the-change:own-plan-check`, `/own-the-change:own-change-debrief`, and `/own-the-change:own-understanding-check`. The Stop hook emits a `systemMessage` containing language-neutral command shortcuts. Its shell/JSON contract is tested; actual Claude command discovery and display are covered by the [manual acceptance checklist](../../docs/acceptance-checklist.md). Runtime language follows the canonical protocol.

Do not load this source directory directly. Its authoring links are not portable; the generated package contains ordinary files and resolves resources entirely inside its root. Marketplace publication remains a separate task.

The former source-adapter marketplace catalog has moved to `../../templates/claude-marketplace.json`. The builder places it beside the complete package under `dist/claude-code/.claude-plugin/marketplace.json`. Use the [release checklist](../../docs/releasing.md) to test catalog validation and cached installation separately. Having an adapter directory doesn't mean it can be installed directly.
