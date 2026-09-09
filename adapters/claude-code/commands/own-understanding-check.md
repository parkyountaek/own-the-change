# Understanding Check

Read `$CLAUDE_PLUGIN_ROOT/../../docs/protocol/understanding-protocol.md` first.

Use the current change's risk level to ask no more than the allowed number of questions. Listen for the user's own explanation rather than grading. Briefly separate what is understood, what is missing, and the next check. Create or update the local record using `$CLAUDE_PLUGIN_ROOT/../../templates/understanding-record.md`. Do not use `confirmed` without the user's answer and supporting change evidence; otherwise use `not_confirmed`, `needs_follow_up`, or `unknown`.
