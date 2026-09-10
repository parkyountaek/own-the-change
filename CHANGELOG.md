# Changelog

## Unreleased - 0.2.1 development

No tag or GitHub release has been created. Development packages are available through this repository's Claude and Codex marketplaces. See the [acceptance checklist](docs/acceptance-checklist.md) for tested installation methods and known limits.

### Added

- A README campaign image, live test badge, sharing kit, and explicit Codex development credit with co-author guidance for new assisted commits.
- Three native Codex checkpoint skills with picker labels and starter prompts. Use `/skills` to choose an action without writing a long prompt.
- A runnable synthetic demo, a short reading walkthrough, and optional first-use feedback and launch drafts.
- Contributor attribution, newcomer contribution ideas, code ownership, and support routes.
- Repository-root Claude and Codex marketplaces with separate complete packages, installable from `parkyountaek/own-the-change` through each host's plugin commands without a manual clone or build.
- A marketplace refresh command and CI checks that keep distribution files synchronized with canonical sources and reject unexpected files or symlinks.
- Self-contained Claude Code and Codex packages built from one maintained protocol.
- A generated Claude marketplace catalog that references its adjacent complete package.
- Explicit runtime language selection, preserving English schema identifiers and original user answers.
- Automated coverage for package isolation, localized records, installation collisions, and record-path boundaries.
- A synthetic host smoke test, contribution and security guidance, and a release checklist.
- Expanded README background explaining the gap between completed code and maintainable knowledge.
- A README everyday-use walkthrough covering target-project startup, debrief, optional planning, understanding questions, saved records, review, and troubleshooting.
- A one-command Claude launcher that builds a temporary package, opens the target project, and cleans up the package on exit without registering a marketplace.
- A lightweight code of conduct, a feature request template, and pinned development-only Ruff/ShellCheck checks in CI.
- Public homepage and repository links in both host manifests.
- A four-case smoke fixture covering surrounding, repeated, empty, and nonbreaking whitespace.

### Changed

- The generic skill defaults to Change Debrief when explicitly invoked without a checkpoint; installation and usage questions do not start a checkpoint.
- The README leads with a concrete change, installation, and first use; detailed local setup is collapsible.
- Both distribution manifests advance to 0.2.1 for the changed public package content. No tag or GitHub release is implied.
- Records use structured response and evidence fields, an explicit diff scope, `record_kind`, and a date list plus reason for follow-up. Older records require explicit migration; validation does not rewrite them.
- Actual local records are ignored by Git in this repository; public examples live in a separate fictional-fixture directory.
- Checkpoints respect the requested scope, reuse supplied evidence and answers, and allow skipping without blocking coding.
- User guides and shared instructions use plainer English; contributor guidance now covers terminology and tone. Commands, schema identifiers, and required record headings are unchanged.
- Claude marketplace metadata is now a build template, not an installable source-adapter catalog.

### Fixed

- Status-line validation rejected a matching status followed by a dash. Common dash separators now work without accepting a different status value.
- The `claude-project` setup hint now uses the launcher instead of suggesting a build path that may already exist.
- The launcher now supports Python module invocation and reports a file target as "not a directory."
- Package permissions copied from private source files: generated data now uses `644`, designated executables and directories use `755`, and source/existing parent permissions are preserved. Content-only copies avoid carrying source extended metadata.
- Source-relative paths that could fail after a host copied a plugin into its cache.
- Assessed statuses without an answer or required evidence, inconsistent record fields, and invalid follow-up dates.
- Malformed quoted/plain YAML scalars and actual/example directory confusion, including directory aliases.
- Context resolution that accepted an external record-directory symlink or a file occupying a record-directory path.
- Missing Claude command descriptions reported by the real host validator.
- Unresolved Claude plugin-root references; commands now use `${CLAUDE_PLUGIN_ROOT}` substitution.
- Ambiguous record privacy checks: the context helper now checks the exact path, reports tracking and ignore matches separately, and checks final-path links.

### Known limits

Claude cache-only loading remains unverified. The interactive launcher showed its commands and Stop shortcuts; its debrief was canceled at the normal permission prompt. Codex completed cache-only loading, but its plugin-list command still needed the local marketplace source. Real-user answer assessment and delayed recall have not been observed. These limits do not establish a measured learning benefit or compatibility with untested hosts.
