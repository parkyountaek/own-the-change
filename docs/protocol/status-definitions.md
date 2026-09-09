# Understanding status definitions

- `confirmed`: The user explained the important reason, effect, or risk in their own words, and the actual change evidence supports that explanation.
- `needs_follow_up`: The user answered, but an important gap remains. Record a concrete next check and, for high-risk work, a follow-up date.
- `not_confirmed`: The user did not answer, or the conversation did not establish understanding. This is the default status.
- `unknown`: Evidence is unavailable or cannot be trusted.

Passing tests, an agent's opinion, or a successful build never change the status to `confirmed` by themselves.
