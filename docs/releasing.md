# Release checklist

This is a manual distribution checklist, not an automatic deployment or approval workflow. Local builds and an MIT license make experimentation possible; they do not establish tested host compatibility.

These unchecked boxes are a reusable checklist for each release candidate, not a claim that every check is still untested. The [acceptance checklist](acceptance-checklist.md) holds dated observations and distinguishes completed local checks from pending publication decisions.

## Before proposing a release

- [ ] Review the [acceptance checklist](acceptance-checklist.md) and run the [host smoke test](host-smoke-test.md) on each host claimed as tested. Record host/version, operating system, installation method, scope, and actual outcomes.
- [ ] Verify the private security-reporting channel described in [SECURITY.md](../SECURITY.md), including delivery before a public release. Private vulnerability reporting is enabled; this checklist does not change repository settings.
- [ ] Establish a private conduct-reporting route and a conflict-of-interest alternative before inviting broader community participation; update [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) with verified contact information only.
- [ ] Set matching semantic versions in both adapter manifests. Use a new version for a published content change; do not represent an older installed cache as the new build.
- [ ] Update [CHANGELOG.md](../CHANGELOG.md) and distinguish experimental support from verified support. Delayed learning benefits remain a hypothesis until actual user follow-up.
- [ ] Run the full suite, example validation, and development-only lint from [CONTRIBUTING.md](../CONTRIBUTING.md). Review each configured CI job and matrix result; defining a workflow does not mean it has run.

## Prepare the GitHub marketplace

The repository itself provides both marketplaces. Claude's root catalog references `plugins/claude-code/own-the-change/`; Codex's `.agents/plugins/marketplace.json` references `plugins/own-the-change/`. Both packages are generated from the same explicit inputs as the temporary packages.

```sh
python3 scripts/sync_marketplace.py
python3 scripts/sync_marketplace.py --check
claude plugin validate .
claude plugin validate plugins/claude-code/own-the-change
git diff --check
```

Review the canonical source changes, the root catalog, and all generated package changes together. Commit them together after authorization. The sync command refreshes expected generated files, rejects unexpected files or symlinks, and never publishes. If a build input was removed, review and remove its obsolete distribution file explicitly before syncing. CI fails when the tracked distribution is stale.

After the reviewed files are pushed to the GitHub default branch, users can install without a manual clone or build:

```text
/plugin marketplace add parkyountaek/own-the-change
/plugin install own-the-change@own-the-change
```

For Codex, run these commands in a terminal and start a new thread:

```sh
codex plugin marketplace add parkyountaek/own-the-change
codex plugin add own-the-change@own-the-change
```

This uses a project-owned marketplace and requires no official marketplace submission. Test the GitHub route after publication; local validation and installation do not prove the remote branch contains the candidate. Use the root checkout's absolute path to test the same catalog locally before publication. See [installation layout](installation-layout.md#github-marketplace) for users migrating from a local catalog with the same name.

For each published package content change, increment both adapter manifest versions before syncing so installed caches can receive the update. Users then run `claude plugin marketplace update own-the-change` and `claude plugin update own-the-change@own-the-change --scope user`, followed by a new session. Match the scope to the actual installation. Uninstall with `claude plugin uninstall own-the-change@own-the-change --scope user`, then remove the catalog with `claude plugin marketplace remove own-the-change` if no longer needed.

Codex updates use `codex plugin marketplace upgrade own-the-change` followed by `codex plugin add own-the-change@own-the-change` and a new thread. Remove the plugin with `codex plugin remove own-the-change@own-the-change`; remove the catalog separately with `codex plugin marketplace remove own-the-change`. Validate its manifest with the Plugin Creator validator available in the maintainer's Codex skill installation, and test an actual installation from a fresh profile. Publishing these catalogs does not submit to either vendor's official directory or change workspace administration settings.

## Build and inspect

```sh
python3 scripts/build_plugins.py --output dist/release-candidate
```

Use a new output path for each candidate. Existing output is never replaced, and a previous build does not update when source files change. Do not distribute the source `adapters/` directories as plugins.

- [ ] Inspect both package directories for ordinary files, the license, security guidance, protocol, skill, template, resolver, and validator. Verify no private records, `.git`, secrets, or unrelated files were included.
- [ ] Confirm public homepage/repository links in both manifests and inspect file modes: data `644`, the hook and Python entry scripts `755`, directories `755`. The builder does not change source or existing ancestor permissions; distributing a package does not make a private ancestor directory accessible.
- [ ] Validate the Claude catalog and plugin with the installed host:

```sh
claude plugin validate dist/release-candidate/claude-code
claude plugin validate dist/release-candidate/claude-code/own-the-change
```

- [ ] Validate the Codex manifest and bundled skill with the current host's plugin/skill validation tooling, then test an actual new conversation. See [OpenAI's plugin guidance](https://learn.chatgpt.com/docs/build-plugins).
- [ ] Test Claude's copied installation separately from `--plugin-dir`. On a tester-controlled profile, add the generated catalog and install its plugin using [Claude's documented marketplace workflow](https://code.claude.com/docs/en/plugin-marketplaces#validation-and-testing):

```text
/plugin marketplace add /absolute/path/to/release-candidate/claude-code
/plugin install own-the-change@own-the-change
```

Adding a catalog changes that tester's host settings. Check for a pre-existing marketplace with the same name before adding it. Follow the host's activation instructions and test without `--plugin-dir`, so a local package cannot mask a stale cached copy. These commands are instructions for an explicitly chosen test, not actions this repository runs automatically.

In the interactive install dialog, choose the intended user, project, or local scope. Do not append CLI flags such as `--scope local` to the interactive marketplace source input: the observed Claude Code 2.1.236 dialog treated them as part of the path. For a non-interactive local-scope installation, use the shell commands instead:

```sh
claude plugin marketplace add /absolute/path/to/release-candidate/claude-code --scope local
claude plugin install own-the-change@own-the-change --scope local
```

For a disposable test, use a distinct temporary catalog name, record the actual installed scope, and remove only that test plugin/catalog afterward using the host CLI. An `installPath` entry alone does not prove the model used cached resources; inspect the resolver path in a fresh session. The source directory remained available during the observed local-catalog test.

The temporary Claude marketplace root is `claude-code/`; its catalog points to `./own-the-change`. Copy or distribute the whole root for catalog-based installation. A raw URL to the catalog alone cannot supply its relative package files. The temporary builder does not create a Codex catalog; `sync_marketplace.py` creates the repository's tracked Codex catalog and package. Neither command registers a marketplace on the user's machine.

## Publication decision

- [ ] Review the exact files to publish. Actual records remain local unless a user explicitly chooses to share a reviewed, redacted record.
- [ ] Review repository access and Git author metadata separately from package contents. The package excludes `.git`; publishing source history may expose metadata that is not present in the built plugin.
- [ ] With explicit authorization, commit the reviewed candidate and record its commit ID for release traceability. Local tests on a dirty tree do not establish that a future commit or tag contains the same files.
- [ ] Obtain explicit authorization for a tag, release, registry submission, or marketplace publication. Do not infer it from passing tests.
- [ ] Provide the release version, supported installation routes, observed host versions, known limitations, and update/removal instructions for the chosen distribution route.

No publication or private-reporting setup is performed by this checklist. Local Linux/macOS tests are not remote GitHub Actions runs. Record an observed installation in the acceptance ledger instead of treating these reusable boxes as permanent compatibility certification.
