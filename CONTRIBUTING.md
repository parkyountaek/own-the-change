# Contributing

Own The Change is an experimental, local-first learning plugin. Contributions that make it easier to use, work on more systems, or produce more accurate records are welcome.

Participation follows the [code of conduct](CODE_OF_CONDUCT.md). Its private reporting route still needs to be established; do not publish sensitive complaints in an issue.

## Start here

- For a bug, provide a minimal synthetic reproduction, host and plugin versions, expected behavior, and the observed result. Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).
- For a feature, use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) to describe the maintenance or learning problem before proposing new infrastructure. The [project scope](docs/architecture.md) explains the first version's boundaries.
- For a possible vulnerability or private-data exposure, follow [SECURITY.md](SECURITY.md), not a public bug report.

## Development

Use Python 3.11 or newer, Git, and a POSIX shell on macOS or Linux. The scripts use the Python standard library, so the local test suite needs no extra packages or API key. Native Windows and WSL have not been tested.

Keep changes focused and preserve unrelated work. Write maintained documentation, instructions, comments, and examples in English. Runtime conversation and private record prose follow the [canonical language policy](docs/protocol/understanding-protocol.md#runtime-language). Use Unicode escapes in localization test source so it remains English-readable.

Keep shared learning and privacy rules in the [canonical protocol](docs/protocol/understanding-protocol.md). Adapters should refer to it, not define their own rules. When changing the protocol, explain the effect on users and add a manual test scenario for behavior that automated tests cannot check.

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_record.py docs/examples/records/*/*.md
python3 scripts/build_plugins.py --output dist/contribution-check
git diff --check
```

Choose a fresh build destination if it already exists. The builder preserves existing output. Tests use temporary synthetic repositories and do not install into your real agent configuration.

The [host smoke test](docs/host-smoke-test.md) is separate from the automated suite. If you haven't run a session, mark it as not tested.

### Writing style

Use clear, conversational American English. Address readers as "you," use active verbs, and keep each paragraph focused on one point. Contractions are fine in user guides. Prefer familiar terms such as "AI-generated code," "test results," and "suggested review dates" over abstract phrases such as "evidence-backed outcomes" or "review candidates."

In user guides, say "coding agent" or name Claude Code or Codex. Use "host" when discussing plugin integration details. Keep product names, commands, schema fields, status values, and required record headings unchanged. Technical terms such as "canonical protocol" and "idempotent" are useful in technical references; explain them or use simpler wording in getting-started instructions.

State what was tested and what remains untested without repeating the same disclaimer in every paragraph. Plain wording must not weaken privacy, permission, or evidence requirements. This style guidance applies to maintained English text, not the user's language in conversations or private records.

### Development-only lint

CI also runs [Ruff](https://docs.astral.sh/ruff/installation/) and [ShellCheck](https://github.com/koalaman/shellcheck). These checks do not rewrite files. Ruff uses a small correctness-focused rule set, not a comprehensive formatting policy.

To run the same pinned tools without a global installation:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m ruff check scripts tests
.venv/bin/shellcheck scripts/install-local.sh adapters/claude-code/hooks/suggest-debrief.sh
```

Reuse an existing development environment if preferred. `shellcheck-py` is a [third-party installer for the ShellCheck binary](https://github.com/shellcheck-py/shellcheck-py). These development downloads, Python/Git, CI actions, and the host agent still have supply-chain dependencies; standard-library runtime helpers do not eliminate that risk. Neither the development requirements nor their installed tools are bundled with the plugin.

## Before submitting

- Include the reason for the change, concise test results, and any remaining limits.
- Check staged and untracked files for private records, secrets, generated packages, and accidental local paths. Keep public examples fictional.
- Update [CHANGELOG.md](CHANGELOG.md) for user-visible behavior and [the acceptance checklist](docs/acceptance-checklist.md) when evidence changes.
- Follow [the release checklist](docs/releasing.md) for distribution work. A contribution does not authorize publication or installation on another person's machine.

Contributions use the repository's [MIT license](LICENSE). You don't need to sign a separate contributor agreement or create an account with another service. Maintainers cannot guarantee response times.
