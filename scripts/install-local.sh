#!/usr/bin/env sh
set -eu

usage() {
  printf '%s\n' 'Usage: scripts/install-local.sh claude-project|codex-project|codex-user|remove-codex-user [--skills-dir ABSOLUTE_PATH]'
  exit 2
}

root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
command=${1:-}
if [ "$#" -gt 0 ]; then shift; fi
skills_dir="$HOME/.agents/skills"
if [ "$#" -gt 0 ]; then
  case "$command" in codex-user|remove-codex-user) ;; *) usage ;; esac
  [ "$#" -eq 2 ] && [ "$1" = "--skills-dir" ] || usage
  case "$2" in /*) skills_dir=$2 ;; *) usage ;; esac
fi
destination="$skills_dir/own-the-change"
source_skill="$root/skills/own-the-change"

owned_link() {
  [ -L "$destination" ] && [ "$(readlink "$destination")" = "$source_skill" ]
}

collision() {
  printf '%s\n' "Refusing to change an existing destination not owned by this installation: $destination" >&2
  exit 1
}

case "$command" in
  claude-project)
    printf '%s\n' "Start a session: python3 \"$root/scripts/launch_claude.py\" \"/absolute/path/to/your-project\""
    printf '%s\n' "Replace the project path above. The launcher builds a fresh temporary package for each session."
    ;;
  codex-project)
    if [ -L "$root/.agents/skills/own-the-change" ] && [ "$(readlink "$root/.agents/skills/own-the-change")" = "../../skills/own-the-change" ] && [ -f "$root/.agents/skills/own-the-change/SKILL.md" ]; then
      printf '%s\n' "Project skill already available: $root/.agents/skills/own-the-change"
    else
      printf '%s\n' "Project skill is missing or changed; restore the tracked .agents/skills/own-the-change link." >&2
      exit 1
    fi
    ;;
  codex-user)
    if owned_link; then
      printf '%s\n' "User skill already available: $destination"
    elif [ -e "$destination" ] || [ -L "$destination" ]; then
      collision
    else
      mkdir -p "$skills_dir"
      ln -s "$source_skill" "$destination"
      printf '%s\n' "Installed user skill: $destination"
    fi
    ;;
  remove-codex-user)
    if owned_link; then
      rm "$destination"
      printf '%s\n' "Removed owned user skill link: $destination"
    elif [ -e "$destination" ] || [ -L "$destination" ]; then
      collision
    else
      printf '%s\n' "No user skill installed at: $destination"
    fi
    ;;
  *) usage ;;
esac
