# Repository development instructions

Read [the understanding protocol](docs/protocol/understanding-protocol.md) before running a checkpoint or changing learning behavior. It is the only source of common learning, record, and privacy rules; agent entry points must link to it instead of copying those rules.

Write repository documentation, instructions, comments, examples, and test descriptions in English.

For implementation changes, inspect the actual Git diff and run `python3 -m unittest discover -s tests -v`. Validate changed example records with `python3 scripts/validate_record.py <record>`. The protocol specifies the validation workflow for actual local records.

When Codex materially assists a new commit, preserve the human author and existing trailers, and include `Co-authored-by: Codex <noreply@openai.com>` after a blank line in the commit message. See [AI attribution](CONTRIBUTORS.md#ai-development-assistance). Do not rewrite published history solely to add attribution.
