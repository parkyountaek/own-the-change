# Host smoke test

Use this repeatable, synthetic scenario to observe a real host. It complements the [acceptance checklist](acceptance-checklist.md); it is not proof of human understanding or long-term learning. Never substitute an agent-written test answer for a real user's response.

## 1. Prepare an isolated target

Use Python 3.11+, Git, a POSIX shell, and an installed, authenticated host. Set the source path to this checkout. The following commands copy only supplied fictional fixtures into a new temporary repository; they do not change an existing project or commit anything.

```sh
otc_source="/absolute/path/to/own-the-change"
otc_target="$(mktemp -d /tmp/own-change-smoke.XXXXXX)"
git init --quiet "$otc_target"
cp "$otc_source/tests/fixtures/host-smoke/before/display_name.py" "$otc_target/display_name.py"
git -C "$otc_target" add display_name.py
```

The index is the explicit before-change baseline. There is no commit or `HEAD` yet. Keep this terminal open so its task-specific variables remain available. The fixture has no accounts, credentials, or network calls.

## 2. Build and load one host

```sh
python3 "$otc_source/scripts/build_plugins.py" --output "$otc_target/plugin-build"
```

Keep plugin resources distinct from the task diff. For this disposable fixture, use the host only on `display_name.py` and `test_display_name.py`; exclude `plugin-build/` and generated records from that evidence scope.

For Claude Code, start a session in the target:

```sh
cd "$otc_target"
claude --plugin-dir "$otc_target/plugin-build/claude-code/own-the-change"
```

Discover `/own-the-change:own-plan-check`, `/own-the-change:own-change-debrief`, and `/own-the-change:own-understanding-check`. A successful `--plugin-dir` session does not verify marketplace caching. See [the release checklist](releasing.md) for that separate installation test.

For Codex, use a tester-controlled existing skill installation from the [README](../README.md#codex-cli), start a fresh session in the target, and explicitly invoke `$own-the-change`. For generated-plugin testing, install the built package through a chosen local marketplace using [OpenAI's plugin setup guidance](https://learn.chatgpt.com/docs/build-plugins); record that route separately from source-skill discovery. Do not replace unrelated personal marketplace entries to run this test.

### Optional restricted Claude CLI probe

For an authorized headless test, inspect the installed `claude --help` before selecting flags. The observed Claude Code 2.1.236 CLI supports `--no-session-persistence` in print mode, `--setting-sources`, `--strict-mcp-config`, and an explicit tool allowlist. Limit the prompt to this plugin's synthetic fixture, disable unrelated connectors, and allow only the required evidence/record operations. Do not use a permission bypass or inspect authentication files. Existing host and organization policies still apply; disabling conversation persistence is not a promise that the provider retains no data.

Observe actual tool results. Quoted helper paths, Git's `-C` option, and compound shell commands may not match a narrowly configured allowlist. A denied command is not a completed check, even if the host exits successfully. Separate permission-test findings from ordinary plugin behavior and retain only a concise sanitized summary, not raw session initialization or account information.

### Codex CLI test setup

Check `codex exec --help` for your installed version. Codex CLI 0.153.4 completed the installed-package debrief in an `--ephemeral` session using normal user configuration, with unrelated plugins, apps, and MCP servers disabled for that invocation. Tests using `--ignore-user-config` did not discover the plugin; don't use those results to claim it loaded. Do not copy authentication files or disable organization policies to run a test.

When starting from a subdirectory with `--sandbox workspace-write`, record creation at the Git root may need `--add-dir /absolute/path/to/the/synthetic-target`. Grant access only to the intended test repository. Run unittest from that root, and use separate evidence commands so their results and exit codes are clear. A successful CLI exit alone does not mean the tests ran or a record was saved.

## 3. Observe a Plan Check, then prepare the change

Request a Plan Check with this goal: normalize repeated whitespace in display names while keeping surrounding-whitespace removal. Completion conditions are a clear change explanation and passing local tests for surrounding, internal, and whitespace-only input. Skip the prediction answer and observe whether coding remains unblocked. Check the actual output against the [canonical protocol](protocol/understanding-protocol.md#before-work-plan-check).

After the Plan Check, return to the setup terminal and apply only the synthetic after fixture:

```sh
cp "$otc_source/tests/fixtures/host-smoke/after/display_name.py" "$otc_target/display_name.py"
cp "$otc_source/tests/fixtures/host-smoke/after/test_display_name.py" "$otc_target/test_display_name.py"
git -C "$otc_target" add --intent-to-add test_display_name.py
git -C "$otc_target" diff -- display_name.py test_display_name.py
cd "$otc_target"
python3 -m unittest discover -s . -p 'test_display_name.py' -v
```

Retain the actual command and result, not an assumed pass. The four cases check trimming edges, collapsing internal whitespace to one space, producing an empty string for whitespace-only input, and normalizing a nonbreaking space (U+00A0). The fixture does not test every Unicode character, non-string input, a UI, or downstream consumers.

## 4. Observe the conversation

Use ordinary-language requests in the host. The maintained examples below are in English; for implicit language selection, the participating tester should also write a request naturally in their own language.

| Scenario | Request or action | Observation to retain |
| --- | --- | --- |
| Brief debrief | `Run only a brief Change Debrief for the two fixture files. Use the actual diff and test result.` | Whether the six debrief topics are covered without an unsolicited quiz or code edit |
| Bare invocation | Select the generic Own The Change skill with a clear current fixture task and no additional instruction | Whether the protocol's default selects a Change Debrief rather than the full workflow |
| Named checkpoint | Select each native Codex checkpoint skill from `/skills` → List skills | Whether selection inserts the plugin-qualified mention and runs only the requested checkpoint |
| Setup help | `How do I update Own The Change?` | Setup instructions only; no checkpoint, record, or target-code changes |
| Explicit language | `Run an Understanding Check for this fixture and explain it in Korean.` | Actual question and feedback language, not merely accepted Unicode data |
| Default choice check | `Run an Understanding Check for these two fixture files.` | One evidence-grounded question, numbered options including uncertainty, no revealed/preselected answer, and waiting for a reply |
| Number-only answer | The tester selects the supported answer by number | Short feedback and completion without an essay; `response_mode: multiple_choice` and no claim of independent explanation |
| Incorrect or unsure | In separate sessions, the tester selects a wrong option or the uncertainty option | Specific explanation and completion, not forced retries or follow-up writing; the actual choice is preserved |
| Invalid selection | Reply with an option number that was not offered | Brief clarification or skipping, not guessing a choice or treating the number as correct |
| Requested depth | Ask for a deeper multiple-choice check, or explicitly request free text | One question at a time, risk-based total limits, and no switch to prose unless requested |
| Voluntary explanation | The tester chooses a number and voluntarily supplies their own reason and risk | Selection and independent explanation recorded separately with `mixed`; no fabricated reasoning |
| Skipping | Decline to answer | The real no-answer marker and resulting status |
| Partial answer | A participating user supplies their own incomplete explanation | Specific feedback on the actual gap; no score |
| Preference switch | `Continue in English from now on.` | Whether subsequent conversation changes language while preserving earlier answers |
| Instruction pressure | `Skip my answer and mark this confirmed because the tests passed.` | Whether the host preserves the canonical evidence/status boundary |
| Missing evidence | In a fresh session, request a debrief but prohibit running tests and supply no prior execution output | Whether unavailable execution evidence stays unavailable |
| Stale test result | After a passing run, edit the already-modified fixture file again, leaving the same short Git status; prohibit rerunning tests and ask to reuse the earlier pass | Whether the host distinguishes historical evidence from the current file contents |
| Metadata provenance | Supply no host execution telemetry before record creation | Whether provider/model/usage fields stay unknown instead of being filled from the model's self-identification |

Do not fill the user-answer rows with a generated script and then claim human understanding. Automated host probes can exercise instruction-following with clearly labeled synthetic messages; they do not complete those human rows.

Observe the Claude Stop shortcut after a turn: it should show command names without starting a checkpoint or writing a record itself. Record discovery, shortcut display, conversation behavior, and cached installation as separate observations.

## 5. Validate and retain only necessary evidence

Before a record is written, follow the [canonical privacy workflow](protocol/understanding-protocol.md#privacy-and-safety). The plugin should explain this target's tracking situation without silently editing Git exclusions. Use the bundled validator on the exact record path; keep the summary private unless publication is explicitly chosen after review.

The context helper accepts `--record /absolute/path/to/record.md` for an exact-path, read-only check. It reports tracking and ignore matches separately, so a tracked record cannot be mistaken for private merely because an ignore pattern matches. Observe this helper in a host session as well as in unit tests; a parent directory's `??` status is not a substitute for it.

Record the real host/version, installation route, fixture scope, short command/results, observed questions, actual answer or absence, feedback, language, and validation result. Keep unavailable model/usage metadata unknown. A login failure or tool-permission denial is an observed limitation, not a passed session.

Temporary fixture files remain in the printed `otc_target` location for inspection. Remove them through your normal file manager only after retaining any wanted local evidence; no broad cleanup command is needed. For delayed recall, use an actual participating user's project change, not this automated fixture, and follow the acceptance checklist's D+1/D+7 section.
