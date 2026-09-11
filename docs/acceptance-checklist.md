# Acceptance checklist

This page records what has been tested and what still needs observation. The [canonical protocol](protocol/understanding-protocol.md) defines the learning rules; this checklist does not replace them. A passing test does not confirm a user's understanding.

## Current verification

Observed on macOS on 2026-09-09 and 2026-09-10, unless another environment is listed below. Host tests used fictional code in disposable Git repositories. They did not use private project code or establish anyone's understanding.

| Area | Observed result | Limit |
| --- | --- | --- |
| Automated suite | On 2026-09-11, all 83 tests passed on macOS with Python 3.12.0 after adding multi-question transcript and partial-response regressions. | Structural and behavioral tests are not an agent or human assessment. The earlier platform matrix below covered 65 tests. |
| Development lint | Ruff 0.16.6 and ShellCheck 0.11.0 passed with the pinned development requirements. | Lint does not prove runtime correctness. |
| Package validation | On 2026-09-11, both 0.2.3 packages built without symlinks or private records; all six public example records validated. Claude manifests and the Codex manifest/skill validators passed. | A valid manifest alone does not prove host discovery. |
| Package portability | Both packages resolve a foreign nested Git target and validate a record after their original source snapshot is removed. | Host installation behavior needs a separate test. |
| Claude Code 2.1.236 | All three commands ran through `--plugin-dir`. Interactive marketplace addition and project-scope installation succeeded; a new installed session completed a Korean debrief, four fixture tests, exact-path privacy checks, and record validation. | That local catalog remained available. Cache-only loading is unverified. |
| Repository-root Claude marketplace | On 2026-09-10, Claude Code 2.1.236 validated the root catalog and tracked package. With a disposable `CLAUDE_CONFIG_DIR`, CLI catalog addition and user-scope installation succeeded. `plugin details` discovered all three checkpoint commands, the shared skill, and the Stop hook. | The first test used a temporary local copy. The published GitHub route was subsequently verified below. No new model conversation was run. |
| Repository-root Codex marketplace | On 2026-09-10, Codex CLI 0.153.4 added the local repository marketplace, installed version 0.2.0, and listed it as enabled from `plugins/own-the-change/` in a disposable configuration. The native manifest passed the Plugin Creator validator. | This verifies local catalog discovery and copied installation, not a new model conversation or the remote GitHub route. |
| Codex checkpoint picker, 0.2.1 | In a disposable profile, Codex CLI 0.153.4 installed the updated local package. App-server `skills/list` reported all four skills enabled, with labels, starter prompts, plugin-qualified names, and paths in the installed cache. The interactive `/skills` → List skills menu displayed all four labels; selecting Change Debrief inserted `$own-the-change:own-change-debrief`. | The menu-only session used a loopback-only dummy model endpoint with no model request submitted. This proves discovery, menu display, and insertion, not a completed checkpoint or desktop-app behavior. |
| Claude installed-cache helpers | With that temporary catalog moved away, the installed resolver found its bundled protocol, template, and validator and resolved a separate Git target. The cached Stop script returned valid shortcut JSON. | `plugin details` failed while the local catalog was absent and succeeded after restoration. Direct helper checks do not establish cache-only loading in a model session. |
| Claude language and evidence | A conversation switched from Korean to English. Skipping questions kept `not_confirmed`; a stale-test probe kept the earlier pass historical and used `unknown`. Missing execution metadata stayed unknown. | These are bounded synthetic observations, not guarantees for every conversation. |
| Claude Stop hook | The hook returned exit 0 and valid command-only `systemMessage` JSON during real sessions. A peer-run interactive launcher test observed the shortcut text in the terminal. | Display was checked by whitespace-insensitive matching of the PTY capture, not across every terminal or host version. |
| Codex CLI 0.153.4 | The final package was installed through a temporary marketplace. From a nested target directory, all three checkpoints used the installed cache and saved valid records at the Git root. Plan/debrief prose was Korean; the Understanding Check followed an English preference and preserved the previous Korean record. | Questions were skipped; no actual user explanation was assessed. |
| Codex cache-only loading | With the local marketplace source temporarily renamed, a new session used the installed cache, passed four fixture tests, and saved a valid Korean debrief. | `codex plugin list` failed while that local source was absent, although the session itself worked. Keep the catalog available for plugin management. |
| Scope and privacy | Installed debriefs reported the exact record as untracked and not ignored, warned about publication, and left fixture source, tests, and Git ignore settings unchanged. Temporary test registrations were removed through each host's CLI. | These checks are not a security sandbox or a test of every sensitive-data scenario. |
| Launcher | Seven automated tests cover the lifecycle and errors. A peer-run interactive session started, displayed all three slash commands, began a debrief, and exited with code 0; its temporary package was removed. | The debrief reached the normal tool-permission prompt, which was canceled. This wrapper test did not complete a record roundtrip. SIGKILL can leave temporary files. |

The Codex Plan Check distinguished its proposed change from existing edits and did not implement it. Its existing tests were not presented as proof of the proposed behavior. Installed Understanding Checks rejected passing tests as a substitute for an answer. All no-answer records remained `not_confirmed`, with the five unavailable metadata fields set to `unknown`.

The Claude installed debrief preceded the final wording and status-punctuation changes; its manifests were revalidated after those changes. The final Codex checkpoint and cache-only sessions used the revised runtime files. Neither test was an installation of a published release.

The marketplace packaging change also passed Ruff 0.16.6, ShellCheck 0.11.0, distribution synchronization, and validation of all three example records. A local `file://` Git URL probe was rejected by Claude's source parser; it is not an installation route documented for users here.

### Published GitHub installation

On 2026-09-10, commit [44b6b0f](https://github.com/parkyountaek/own-the-change/commit/44b6b0fbd620e7244177ead506364e761a097b92) was pushed to `main` after an independent subagent review found no actionable defects. That reviewer also passed all 72 tests, the sync check, and Claude validation. The commit's [GitHub Actions run](https://github.com/parkyountaek/own-the-change/actions/runs/34434988526) passed lint and all four Ubuntu/macOS Python 3.11/3.13 test jobs, including builds, example validation, and distribution checks.

Fresh temporary configurations installed directly from the published GitHub repository without a manual source clone or build:

- Claude Code 2.1.236: `claude plugin marketplace add parkyountaek/own-the-change`, then `claude plugin install own-the-change@own-the-change --scope user`. The CLI listed version 0.2.0 as enabled and discovered the three commands, shared skill, and Stop hook.
- Codex CLI 0.153.4: `codex plugin marketplace add parkyountaek/own-the-change`, then `codex plugin add own-the-change@own-the-change`. The CLI listed version 0.2.0 as installed and enabled from the GitHub marketplace, using the native package.

Both downloaded marketplace snapshots resolved to the tested commit. Installed package contents matched the committed distributions; Claude additionally created its `.in_use` cache marker. Both installed resolvers located their bundled resources and a separate synthetic Git target. These checks establish installation and resource availability, not a new model conversation or an assessment of user understanding. Normal user profiles were not modified.

### Published update from 0.2.0 to 0.2.1

Commit [fbb1625](https://github.com/parkyountaek/own-the-change/commit/fbb1625f1cd29406eeb233f22d7df9608c369b01) added the Codex checkpoint skills and onboarding improvements. Its [GitHub Actions run](https://github.com/parkyountaek/own-the-change/actions/runs/34455724622) passed lint and all four Ubuntu/macOS Python 3.11/3.13 jobs, each running the 75-test suite, example validation, builds, and distribution checks.

Before publication, separate temporary profiles installed the public 0.2.0 package. After publication, the exact sequences in the [update guide](updating.md) produced these results on September 10, 2026:

- Claude Code 2.1.236 reported an update from 0.2.0 to 0.2.1 at user scope and listed it as enabled.
- Codex CLI 0.153.4 refreshed the GitHub catalog, installed 0.2.1, and listed it as installed and enabled. A fresh app-server skill listing found the three new checkpoint entries and the original generic entry in the updated cache.

Both marketplace snapshots resolved to the published commit, and both installed packages matched the committed files (excluding Claude's host-generated `.in_use` marker). These are upgrade and discovery checks, not new model conversations. Normal user profiles and learning records were not changed.

### GitHub project setup

On 2026-09-10, the repository description, README homepage link, and nine relevant topics were set. Discussions and a `feedback` issue label were enabled for voluntary reports. GitHub's private vulnerability reporting API returned `enabled: true` after activation. No advisory, outreach post, directory application, tag, or GitHub release was created by this setup. A private conduct-reporting contact and end-to-end security-report delivery remain unverified.

### Multiple-choice update, 0.2.2

Observed on macOS on 2026-09-11:

- The 81-test suite includes 64 response-mode/status/answer/evidence combinations, number-only and unsure replies, Korean choice text, rejection of choice-only confirmation, and byte-preserving validation of legacy records without `response_mode`. Both built packages enforce the same new guard after their source snapshot is moved away.
- Ruff 0.16.6, ShellCheck 0.11.0, all five fictional example records, the skill/manifest validators, and distribution synchronization passed. Validation dependencies were installed only in a temporary Python environment.
- Disposable Claude Code 2.1.236 and Codex CLI 0.153.4 profiles installed 0.2.2 from local catalogs. A separate temporary Codex source copy also passed the Plugin Creator cachebuster/reinstall flow with the `0.2.2` prefix preserved; that development suffix is not part of the public package.
- Three read-only Codex CLI probes explicitly loaded the generated 0.2.2 skill path. The first inspected the index-based synthetic whitespace diff, passed all four fixture tests, asked one numbered question with an unsure option, and waited. Separate fresh probes received that question plus a synthetic `2` or `4` reply. Both reran the four tests, gave short feedback, and ended without an essay or retry; the correct selection stayed `not_confirmed`, and the unsure selection used `needs_follow_up`.

The conversation probes used [non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode), `--ephemeral`, `--ignore-user-config`, a read-only sandbox, and invocation-only disabling of plugins, apps, hooks, multi-agent work, and web search. Authentication remained with the normal host; no credentials were copied or inspected. The explicit package path was used instead of testing picker discovery. No source files or learning records were written. macOS emitted Git/Xcode cache warnings in the read-only sandbox, but the inspected diff, resolver, and test commands returned exit 0 with usable output.

These are synthetic instruction-following observations, not a continuous installed conversation or a real learner assessment. Claude multiple-choice conversations, incorrect/invalid/skipped replies in a model session, optional-depth behavior, and live record creation with the new mode remain to be observed. The tests do not establish reduced burden, better recall, or future maintenance ability.

The implementation was published as [c179ca4](https://github.com/parkyountaek/own-the-change/commit/c179ca4dd4ec229b3c20a8c5f3772d97ad16e27a). Its [GitHub Actions run](https://github.com/parkyountaek/own-the-change/actions/runs/34544752079) passed lint and all four Ubuntu/macOS Python 3.11/3.13 jobs. Before publication, separate disposable profiles installed the public 0.2.1 package. After publication, the [update commands](updating.md) upgraded both Claude and Codex to 0.2.2. Both downloaded catalogs resolved to that commit, installed contents matched the published packages (excluding Claude's `.in_use` marker), and both cached validators accepted all five example records. This verifies the public upgrade route, not an additional model conversation. Normal user profiles and private learning records were not modified; no announcement, comment, tag, or GitHub release was posted for this update.

### Multi-question update, 0.2.3

Observed on macOS on 2026-09-11:

- All 83 unit tests passed, including byte-preserving validation of two-, three-, and five-reply transcripts and early-stop transcripts. Contradictory partial-response fields and choice-only confirmation are rejected. These tests check record structure, not question sequencing or answer correctness.
- Both generated 0.2.3 packages passed synchronization and manifest/skill validation. Ruff 0.16.6, ShellCheck 0.11.0, and all six fictional example records passed. The examples include a completed two-question check, uncertainty followed by a correct choice, and an early stop that preserves the first selection.
- Four bounded Codex CLI 0.153.4 probes loaded the generated skill by explicit path. The initial probe inspected the synthetic index-based diff, passed four fixture tests, planned two low-risk questions, and waited at `1/2`. A continuation receiving synthetic reply `4` explained uncertainty and advanced to `2/2`. The final continuation received `1`, ended the planned sequence without an extra question, and retained `needs_follow_up` for the earlier uncertainty. Both continuation probes reran the four tests successfully.
- A separate branch received `1. stop` at the first question. It acknowledged the correct selection, stopped after `1/2`, and left the behavior topic unasked and unchecked, without claiming independent understanding. The fixture files still matched the supplied after fixtures and no learning record was created.

The probes used the same [non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode) isolation as the 0.2.2 probes: read-only sandbox, ephemeral sessions, ignored user configuration, and unrelated integrations disabled for the invocation. Previous assistant output and explicitly synthetic replies were supplied to fresh continuation processes. They were not a continuous installed conversation or real user participation. Three- and five-question model conversations, Claude's updated conversation flow, individual-question skipping, invalid replies, format changes, and live partial-record creation remain unobserved. Structural tests and these bounded probes do not establish reduced burden or a learning benefit.

The implementation was published as [2147b85](https://github.com/parkyountaek/own-the-change/commit/2147b85fdb27771ceed61fc93521b484f4fbfca3). Its [GitHub Actions run](https://github.com/parkyountaek/own-the-change/actions/runs/34556194696) passed lint and all four Ubuntu/macOS Python 3.11/3.13 jobs. Disposable profiles installed public 0.2.2 before publication, then used the documented update commands to reach 0.2.3 in Claude Code 2.1.236 and Codex CLI 0.153.4. Both downloaded catalogs resolved to that commit; both installed packages matched the published contents, excluding Claude's `.in_use` marker, and their cached validators accepted all six example records. Normal user profiles and private records were not modified. No announcement, comment, tag, or GitHub release was posted.

### Local platform matrix

All 65 tests passed in each environment after the runtime fixes:

| Environment | Python |
| --- | --- |
| macOS | 3.11.11 |
| macOS | 3.13.14 |
| Debian Linux arm64 container | 3.11.16 |
| Debian Linux arm64 container | 3.13.15 |

The containers used a read-only source snapshot without original Git history or private records, and no runtime network. This local matrix is separate from the Ubuntu/macOS GitHub Actions matrix. Check [CI results](https://github.com/parkyountaek/own-the-change/actions/workflows/test.yml) for the exact commit you plan to use.

Native Windows, WSL, Cursor, Copilot, and generic-agent runtime sessions are not claimed as tested.

## Reproduce the checks

From the source checkout:

```sh
python3 scripts/sync_marketplace.py --check
python3 -m unittest discover -s tests -v
python3 scripts/validate_record.py docs/examples/records/*/*.md
python3 scripts/build_plugins.py --output /path/to/new-build
git diff --check
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for pinned lint commands and the [host smoke test](host-smoke-test.md) for a fictional target, installation steps, and permission guidance. Use a new build path each time.

| Test file | Coverage |
| --- | --- |
| `test_validate_record.py` | Status/response/evidence/mode consistency, legacy record preservation, required sections, YAML scalars, status punctuation, actual/example separation, and follow-up dates |
| `test_resolve_context.py` | Foreign nested targets, source aliases, exact record tracking/ignore checks, external links, and path conflicts |
| `test_build_plugins.py` | Complete packages, private-input exclusion, source independence, safe output handling, and normalized POSIX permissions |
| `test_sync_marketplace.py` | Tracked distribution consistency, complete catalog target, stale-file detection, private-input exclusion, and preservation of unexpected files or symlinks |
| `test_install_layout.py` | Discovery links, repeat installation/removal, foreign-file protection, and setup hints |
| `test_launch_claude.py` | Launcher lifecycle, prerequisites, invocation forms, arguments, signals, and cleanup |
| `test_prepare_demo.py` | Fresh synthetic Git/index setup, all four example tests, record exclusion, and preservation of existing destinations |
| `test_repository_content.py` | Maintained English text, local Markdown links, and the four-case smoke fixture |
| `test_runtime_language.py` | Localized record prose, original answers, and follow-up reasons with stable schema identifiers |

The validator checks structure and consistency. It cannot authenticate a quotation, determine whether a test really ran, or judge whether an answer demonstrates understanding.

## Onboarding and compact instructions: 0.3.0

Observed locally on September 11, 2026, with Python 3.12.0 on macOS:

- The full `python3 -m unittest discover -s tests -v` suite passed all 98 tests. Six public example records passed validation. Ruff 0.16.6, ShellCheck 0.11.0, distribution sync checks, and `git diff --check` passed.
- Both packages build from explicit inputs. With their copied source snapshot moved out of reach, the bundled Demo helper prepared a new target, its four fixture tests passed, Doctor ran outside Git, and the protocol reader and validator worked. No learning record was created by demo preparation.
- Five-question ordering tests preserve all four content choices, the matching key, and uncertainty last. They reject malformed input and prevent consecutive identical correct positions without a fixed cycle. They do not test semantic quality or establish better discrimination between learners.
- All eleven canonical entry bodies contain 183-246 characters, excluding YAML discovery metadata, and have a tested 250-character ceiling. The reader selects complete verbatim sections and rejects an unmapped/duplicate heading. A debrief selection contains 16,397 characters versus 34,314 in the complete protocol at this candidate; these are text sizes, not token or billing measurements.
- Claude Code 2.1.236 validated the repository catalog and complete package. The Codex Plugin Creator validator and all six skill validators passed. The new feedback YAML parsed with unique IDs and no required free-text body field; GitHub rendering has not yet been observed.
- Codex CLI 0.154.0 ran a bounded synthetic Understanding Check from the built package with read-only sandboxing, normal host authentication, user configuration ignored, and plugins/apps/hooks/multi-agent/web search disabled. The first Korean response honored an explicit three-question request, inspected the index-based fixture, ran four passing tests, used the ordering helper, and displayed question 1/3 with correct position 4 and uncertainty at 5. No code or learning record was written.
- A fresh-process replay supplied an explicitly synthetic uncertainty reply of `5`; the next response explained the reason and asked a distinct NBSP behavior question as 2/3, with correct position 3 and uncertainty at 5. It did not force an essay or retry. These are tool/response probes, not a continuous installed-picker conversation or real-user learning evidence. Host usage was emitted, but there is no matched old-version comparison and no measured savings claim.
- A final fresh-process replay supplied a correct second selection plus an early-stop request. The response ended without question 3, preserved the earlier uncertainty as `needs_follow_up`, left the unasked topic unchecked, and created no code changes or learning record. No real participant is represented by these replies.

Published implementation: `41d831fb2d5d033fd0e5cbff0480a29867833af5`. [GitHub Actions](https://github.com/parkyountaek/own-the-change/actions/runs/34598714224) passed all five jobs: lint and the Ubuntu/macOS matrix on Python 3.11/3.13. In disposable profiles, existing GitHub installs upgraded from 0.2.3 to 0.3.0 using Claude Code 2.1.236 and Codex CLI 0.154.0. The resulting cache contents matched the published packages (excluding Claude's `.in_use` marker); both cached Doctor helpers passed. This verifies download/update and package contents, not new interactive picker behavior.

The previous known public source before this candidate was `f14d6d0b5199c9b81b022ecc9dad008862ce7908` (0.2.3). No tag or GitHub release is implied by the 0.3.0 development version. Fresh installed picker interactions, full three- and five-question conversations on both hosts, a first-save privacy decision in a real target, human-rated wording/question quality, Windows/WSL use, and delayed learning effects remain separate checks. Private conduct contacts, security-report delivery, and public-release approval still require maintainer decisions.

## Remaining host checks

These are additional acceptance scenarios, not claims of completed testing:

- [ ] Claude: test resource loading with the original local catalog unavailable.
- [ ] Complete a debrief through the interactive launcher after the tester grants its required evidence/record permissions. Discovery, invocation, shortcut display, and cleanup are already observed; the separately installed headless flow completed the record roundtrip.
- [ ] Exercise already-committed changes, mixed task history, and real already-tracked records in host sessions. Staged/unstaged synthetic changes and path checks are covered, but not every scope combination.
- [ ] Observe missing and failing test evidence in separate fresh sessions. Stale-evidence handling has been observed; it is not a substitute for both scenarios.
- [ ] Observe reuse of a real user's supplied answer without repeating the question.
- [ ] Observe low-, medium-, and high-risk answers, specific gap feedback, and transfer to a related example with a participating user.

Use only synthetic, non-sensitive fixtures for automated host probes. Role-play answers must remain labeled as examples and cannot close the real-user rows.

## Delayed learning check

With a participating user, revisit an important actual change on its recorded follow-up dates using the [canonical follow-up workflow](protocol/understanding-protocol.md#follow-up). If the user opts into independent recall, ask why the change was needed, what could fail, and where they would start a small related repair. A correct selection in the default choice mode does not complete the unaided-recall checks below. Record only the actual answer and any gaps.

- [ ] D+1: actual recall and a concrete next check recorded.
- [ ] D+7: actual recall and a related-maintenance direction recorded.

No delayed session has been observed. The user need not implement a repair, and an unobserved session stays unobserved.

## Distribution and community readiness

The MIT-licensed source and local installation methods are available for experimentation. Use generated packages, not source adapter directories, for plugin installation.

Before a tagged release or broader community launch:

- [ ] Verify a working private vulnerability-reporting channel; see [SECURITY.md](../SECURITY.md).
- [ ] Establish a private conduct-reporting contact and an alternative for complaints involving a maintainer; see [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).
- [ ] Choose and authorize the release version and distribution destination, then follow the [release checklist](releasing.md).

These maintainer decisions and real-user learning checks cannot be completed by marking boxes after automated tests.
