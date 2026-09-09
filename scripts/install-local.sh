#!/usr/bin/env sh
set -eu

usage() {
  printf '%s\n' 'Usage: scripts/install-local.sh claude-project|codex-project|codex-user|remove-codex-project|remove-codex-user'
  exit 2
}

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
command=${1:-}

case "$command" in
  claude-project)
    printf '%s\n' "Run this from the repository root: claude --plugin-dir $root/adapters/claude-code"
    ;;
  codex-project)
    mkdir -p "$root/.agents/skills"
    ln -sfn "$root/adapters/codex/.agents/skills/own-the-change" "$root/.agents/skills/own-the-change"
    printf '%s\n' "Installed project skill: $root/.agents/skills/own-the-change"
    ;;
  codex-user)
    mkdir -p "$HOME/.agents/skills"
    ln -sfn "$root/adapters/codex/.agents/skills/own-the-change" "$HOME/.agents/skills/own-the-change"
    printf '%s\n' "Installed user skill: $HOME/.agents/skills/own-the-change"
    ;;
  remove-codex-project)
    rm -f "$root/.agents/skills/own-the-change"
    rmdir "$root/.agents/skills" 2>/dev/null || true
    rmdir "$root/.agents" 2>/dev/null || true
    ;;
  remove-codex-user)
    rm -f "$HOME/.agents/skills/own-the-change"
    ;;
  *) usage ;;
esac
