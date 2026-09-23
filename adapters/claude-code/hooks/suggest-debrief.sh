#!/usr/bin/env sh
# This hook only suggests an optional next step. It never writes a record.
# Command names are language-neutral; conversational wording belongs to the agent.
# Stay quiet outside a Git work tree or when it has no pending changes.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
[ -n "$(git status --porcelain 2>/dev/null)" ] || exit 0

# Within one session, stay quiet until the pending changes differ from the last
# suggestion, so an unchanged tree or a finished debrief does not repeat it.
# Only a checksum is kept, in a private per-user temporary directory.
session=
[ -t 0 ] || session=$(tr -d '\n' | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([A-Za-z0-9_-]\{1,128\}\)".*/\1/p')
if [ -n "$session" ]; then
  uid=$(id -u)
  state="${TMPDIR:-/tmp}/own-the-change-$uid"
  [ -e "$state" ] || [ -L "$state" ] || mkdir -m 700 "$state" 2>/dev/null
  if [ -d "$state" ] && [ ! -L "$state" ] && [ -n "$(find "$state" -prune -user "$uid")" ]; then
    fingerprint=$({
      git rev-parse --show-toplevel
      git status --porcelain
      git diff --no-ext-diff --no-textconv --no-color
      git diff --cached --no-ext-diff --no-textconv --no-color
      git ls-files --others --exclude-standard | git hash-object --stdin-paths
    } 2>/dev/null | cksum)
    last="$state/$session"
    if [ -f "$last" ] && [ ! -L "$last" ] && [ "$(cat "$last" 2>/dev/null)" = "$fingerprint" ]; then
      exit 0
    fi
    [ -L "$last" ] || printf '%s\n' "$fingerprint" > "$last" 2>/dev/null
  fi
fi
printf '%s\n' '{"systemMessage":"Own The Change | /own-the-change:own-change-debrief | /own-the-change:own-understanding-check"}'
exit 0
