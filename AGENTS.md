# Repository rules

- `docs/protocol/understanding-protocol.md` is the only source of common learning rules.
- Agent-specific files link to that source and must not copy the common rules.
- Do not present an explanation as fact without the actual `git diff` and execution output.
- Without a user response, use `not_confirmed` or `unknown` for understanding status.
- Passing tests or an agent self-assessment never justify `confirmed`.
- Do not send source code, secrets, environment variables, or complete terminal logs outside this repository.
- Automatic code changes, deployment, merge, and pull-request approval are out of scope.
- After creating or changing a record, run `python3 scripts/validate_record.py <record>`.
