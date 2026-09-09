#!/usr/bin/env sh
set -eu

usage() {
  printf '%s\n' 'Usage: scripts/install-local.sh claude-project|codex-project|codex-user|remove-codex-user'
  exit 2
}

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
command=${1:-}

case "$command" in
  claude-project)
    printf '%s\n' "Run this from the repository root: claude --plugin-dir $root"
    ;;
  codex-project)
    if [ -L "$root/.agents/skills/own-the-change" ] && [ "$(readlink "$root/.agents/skills/own-the-change")" = "../../skills/own-the-change" ]; then
      printf '%s\n' "Project skill already available: $root/.agents/skills/own-the-change"
    else
      printf '%s\n' "Project skill is missing or changed; restore the tracked .agents/skills/own-the-change link." >&2
      exit 1
    fi
    ;;
  codex-user)
    mkdir -p "$HOME/.agents/skills"
    ln -sfn "$root/skills/own-the-change" "$HOME/.agents/skills/own-the-change"
    printf '%s\n' "Installed user skill: $HOME/.agents/skills/own-the-change"
    ;;
  remove-codex-user)
    rm -f "$HOME/.agents/skills/own-the-change"
    ;;
  *) usage ;;
esac
