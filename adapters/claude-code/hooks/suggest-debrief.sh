#!/usr/bin/env sh
# This hook only suggests an optional next step. It never writes a record.
# Command names are language-neutral; conversational wording belongs to the agent.
# Stay quiet outside a Git work tree or when it has no pending changes.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
    && [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  printf '%s\n' '{"systemMessage":"Own The Change | /own-the-change:own-change-debrief | /own-the-change:own-understanding-check"}'
fi
exit 0
