#!/usr/bin/env sh
# This hook only suggests an optional next step. It never writes a record.
# Command names are language-neutral; conversational wording belongs to the agent.
# Stay quiet outside a Git work tree or when it has no pending changes.
# Work from the root so a session started in a subdirectory sees every change.
message='{"systemMessage":"Own The Change | /own-the-change:own-change-debrief | /own-the-change:own-understanding-check"}'
top=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$top" || exit 0
# A failed status cannot prove a clean tree, so suggest without caching.
if ! status=$(git status --porcelain 2>/dev/null); then
  printf '%s\n' "$message"
  exit 0
fi
[ -n "$status" ] || exit 0

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
    # Hash untracked content through a throwaway index: symlinks count as links and
    # no Git objects are written. Cache only when every step succeeds; if any path
    # cannot be listed, hashed, or diffed (for example a nested repository or an
    # unreadable file), suggest without caching so a real change is never hidden.
    list="$state/$session.$$.list"
    index="$state/$session.$$.index"
    trap 'rm -f "$list" "$index" "$index.lock"' EXIT
    if git ls-files -z --others --exclude-standard > "$list" 2>/dev/null &&
        warnings=$(GIT_INDEX_FILE="$index" git update-index --add --info-only -z --stdin < "$list" 2>&1) &&
        [ -z "$warnings" ] &&
        untracked=$(GIT_INDEX_FILE="$index" git ls-files -s 2>/dev/null) &&
        unstaged=$(git diff --no-ext-diff --no-textconv --no-color 2>/dev/null) &&
        staged=$(git diff --cached --no-ext-diff --no-textconv --no-color 2>/dev/null) &&
        fingerprint=$(printf '%s\n' "$top" "$status" "$untracked" "$unstaged" "$staged" | cksum) &&
        [ -n "$fingerprint" ]; then
      last="$state/$session"
      if [ -f "$last" ] && [ ! -L "$last" ] && [ "$(cat "$last" 2>/dev/null)" = "$fingerprint" ]; then
        exit 0
      fi
      [ -L "$last" ] || printf '%s\n' "$fingerprint" > "$last" 2>/dev/null
    fi
  fi
fi
printf '%s\n' "$message"
exit 0
