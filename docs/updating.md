# Update an existing installation

You do not need to clone the repository again. Refresh the marketplace, update its installed package, then start a new session. These steps apply to installation from `parkyountaek/own-the-change`; [local installations](#local-installations) use a different source.

The 0.3.0 development package adds Demo, Doctor, four content choices plus uncertainty, compact entry instructions, and conversation-only completion. The record schema is unchanged. See the [current acceptance scope](acceptance-checklist.md#onboarding-and-compact-instructions-030); older verification below applies only to its stated versions.

On September 11, 2026, both command sequences below upgraded existing GitHub installations from 0.2.2 to 0.2.3 in disposable profiles, using Claude Code 2.1.236 and Codex CLI 0.153.4. See the [0.2.3 verification details](acceptance-checklist.md#multi-question-update-023); the earlier [0.2.2 verification](acceptance-checklist.md#multiple-choice-update-022) and [0.2.0 to 0.2.1 check](acceptance-checklist.md#published-update-from-020-to-021) are retained separately.

Version 0.2.3 expands Understanding Check to normally three questions, two for low-risk changes, and up to five for high-risk changes, one at a time with visible progress. Incorrect or unsure replies receive feedback before the next planned question; stopping early preserves earlier answers. Update the installed instructions and start a fresh session to replace the 0.2.2 single-question behavior. Record fields do not change in 0.2.3.

Version 0.2.2 introduced `response_mode` to new records. The current bundled validator accepts existing 0.2.1 records without rewriting them; a pre-0.2.2 validator will reject the new field. Installation checks do not by themselves verify a conversation; the acceptance page records separate synthetic probes and remaining host checks.

## Claude Code

Run in a terminal:

```sh
claude plugin marketplace update own-the-change
claude plugin update own-the-change@own-the-change --scope user
```

Use the scope you originally installed into. For `project` or `local` scope, replace `user` and run from the corresponding project. `claude plugin list` shows installed entries; `claude plugin marketplace list` shows their catalog sources. Start a fresh Claude session after the update.

## Codex CLI

Run in a terminal:

```sh
codex plugin marketplace upgrade own-the-change
codex plugin add own-the-change@own-the-change
```

`plugin add` installs the version in the refreshed catalog; refreshing the catalog alone does not establish that the installed package changed. `codex plugin list` shows the installed plugin, and `codex plugin marketplace list` shows its source. Start a new Codex thread to discover new skills.

For the 0.2.1 update, `/skills` → **List skills** should include **Own The Change: Change Debrief**, **Plan Check**, and **Understanding Check**, as well as the original generic entry. You can type `$` to open the list directly. See [Codex usage](codex-usage.md) for installed names and client differences.

## If the old behavior remains

1. Confirm both commands succeeded, not just marketplace refresh.
2. Check that the installed version matches the package version in the [changelog](../CHANGELOG.md).
3. Start a new session; a running conversation can retain previously loaded instructions.
4. Check for a local catalog or a second skill installation with the same name. Use the [migration guide](installation-layout.md#github-marketplace) before changing its source.

Do not delete personal configuration or learning records to force an update. These instructions do not promise automatic updates; client and organization settings can differ.

## Local installations

- **Linked Codex skill:** update the source checkout with `git pull --ff-only`, then start a new session. Keep that checkout available. This route exposes only the generic skill; use the native marketplace plugin for the named shortcuts.
- **Claude launcher:** update the source checkout, then rerun `scripts/launch_claude.py`; it builds a fresh temporary package.
- **Manually built package or local marketplace:** pulling source alone does not rebuild that package. Build into a new output directory and follow the [local release verification](releasing.md#build-and-inspect) for the exact catalog you installed.

If Git reports local changes or a diverged branch, preserve those changes and resolve the conflict; do not reset the checkout as an update shortcut.

Updating plugin files does not migrate or validate old learning records automatically. If a record schema changes, follow the explicit migration notes in the [changelog](../CHANGELOG.md) and [protocol](protocol/understanding-protocol.md).
