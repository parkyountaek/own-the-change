#!/usr/bin/env sh
# This hook only suggests an optional next step. It never writes a record.
# Command names are language-neutral; conversational wording belongs to the agent.
printf '%s\n' '{"systemMessage":"Own The Change | /own-the-change:own-change-debrief | /own-the-change:own-understanding-check"}'
exit 0
