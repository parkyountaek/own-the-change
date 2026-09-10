# Installation layout

## GitHub marketplace

Claude Code can install the committed distribution directly from this repository:

```text
/plugin marketplace add parkyountaek/own-the-change
/plugin install own-the-change@own-the-change
```

The root `.claude-plugin/marketplace.json` points to `./plugins/claude-code/own-the-change`. That directory contains the complete generated Claude package as ordinary tracked files, so users need no manual checkout or build. This is a project-owned marketplace; installation does not depend on acceptance into Anthropic's official catalog.

Codex CLI uses the same GitHub repository:

```sh
codex plugin marketplace add parkyountaek/own-the-change
codex plugin add own-the-change@own-the-change
```

Its catalog is `.agents/plugins/marketplace.json`, with a local source object pointing to `./plugins/own-the-change`. Codex resolves this path from the repository root. The native package contains its own manifest, skill, and shared resources. Keeping separate complete packages gives each host only its own integration files. See [OpenAI's supported marketplace formats](https://learn.chatgpt.com/docs/enterprise/plugin-management#supported-formats). Distribution through this repository does not submit the plugin to OpenAI's public directory or install it in an organization's workspace.

For a local checkout test, substitute its absolute path for `parkyountaek/own-the-change`. Both routes use the same catalog and package. Claude copies only the package directory into its installed cache. The package excludes local records, credentials, host settings, and repository history.

If you already registered a generated local catalog named `own-the-change`, inspect `claude plugin marketplace list`. To switch deliberately, uninstall `own-the-change@own-the-change` in the scope you used, remove that catalog with `claude plugin marketplace remove own-the-change`, then add the GitHub source and reinstall. Removing a marketplace also removes its installed plugins; it does not delete learning records in your target projects.

For the corresponding Codex migration, inspect `codex plugin marketplace list`, remove the plugin with `codex plugin remove own-the-change@own-the-change`, remove the old catalog with `codex plugin marketplace remove own-the-change`, then run the GitHub commands above. Start a new thread after installation. If you previously installed the user skill link from this checkout, use `scripts/install-local.sh remove-codex-user` when you want to use only the marketplace copy; the script removes only its own link.

Maintainers run `python3 scripts/sync_marketplace.py` after changing package inputs and include both catalogs and package changes in the same commit. `python3 scripts/sync_marketplace.py --check` and the test suite detect stale content or unexpected package files. The refresh refuses symlinks and unexpected files instead of overwriting or deleting them. Edit canonical inputs, not the distribution copies. See the [release checklist](releasing.md#prepare-the-github-marketplace).

## Local use

- Claude Code: run `python3 scripts/launch_claude.py /absolute/path/to/your-project` for a temporary, session-only installation
- Codex: automatically discovers `.agents/skills/own-the-change` at the repository root
- Cursor: a `.cursor/skills/own-the-change` discovery link is provided; runtime unverified
- GitHub Copilot and other Agent Skills-compatible tools: a `.agents/skills/own-the-change` link is provided; runtime unverified

The repository keeps one shared skill in `skills/own-the-change/`. Discovery paths are symbolic links only. The common rules live only in `docs/protocol/understanding-protocol.md`.

The Claude launcher checks for Claude Code, Git, and a valid target repository before building. It creates a fresh temporary package for each session, starts Claude in the requested directory, and removes that package when Claude exits. It does not install a marketplace or change host configuration. It doesn't erase Claude's own conversation history. Use the GitHub marketplace when you need a persistent installation.

Resolve entry-point symlinks before finding the resource root. `scripts/resolve_context.py --target <working-directory>` reports resources and the target Git root, including when the working directory is nested in a different repository. Source-discovery links require the checkout; generated packages include their own resources.

The installer won't overwrite a same-name file, directory, or link from another installation. Use `--skills-dir <absolute-directory>` to test a separate installation directory. Uninstalling checks that the link points to this checkout; tests don't need to change your home-directory settings.

## Self-contained packages

`python3 scripts/build_plugins.py --output /path/to/new-build` creates:

```text
new-build/
  claude-code/.claude-plugin/marketplace.json  local catalog for the adjacent package
  claude-code/own-the-change/  Claude manifest, commands, hook, skill, and resources
  codex/own-the-change/        Codex manifest, skill, and resources
```

Each package includes its own license, protocol, template, context helper, and validator. The builder copies only explicitly listed inputs, follows source links into ordinary files, and emits no symbolic links. Existing output is never overwritten. Do not load `adapters/` directly: those directories are authoring inputs whose shared links can escape a host plugin root.

The portability test builds both packages from a temporary source snapshot, removes that snapshot's original path, and exercises each package against a different nested Git target. The source protocol remains the only maintained rule source; generated copies are build artifacts.

## Distribution and verification

`templates/claude-marketplace.json` is copied to the temporary Claude marketplace root with source `./own-the-change`. The sync script uses that template with source `./plugins/claude-code/own-the-change` for the tracked root catalog, and copies `templates/codex-marketplace.json` to `.agents/plugins/marketplace.json`. Neither catalog references an incomplete source adapter. Building and syncing do not push to GitHub or register anything in the user's host configuration.

Automated tests cover resource lookup after copying a package. Earlier temporary Claude and Codex marketplace installations also passed a debrief with record creation and validation. Codex used its installed cache; Claude used the still-available local catalog package. Both hosts later installed version 0.2.0 directly from the published GitHub marketplace in fresh temporary configurations. Those later checks verified discovery and bundled resources without running new model conversations. See the [acceptance checklist](acceptance-checklist.md#published-github-installation) for the tested commit, CI results, and remaining limits.

Use [the host smoke test](host-smoke-test.md) for synthetic task setup and [the release checklist](releasing.md) for catalog validation, cached installation, and distribution boundaries. Source changes do not refresh an earlier build; choose a fresh output and a fresh host session when retesting.

## Host account independence

Host authentication is separate from this plugin. The package does not bundle a tester's email, organization, account identifier, credentials, host settings, or session history. No account-specific marketplace or model identifier is needed to build it or run its local tests.

If access to a host account changes, sign in to an authorized replacement account using the host's own login flow, then load or install the same plugin package. This project does not transfer credentials, subscriptions, host conversation history, or organization-managed installations between accounts.

Local Markdown records do not require the original account to be read, but their contents may belong to the project or organization that produced them. Portability is not permission to copy those records or any source code. Review ownership and sharing restrictions before moving project data. Keep actual records separate from distributable plugin files using the [canonical privacy workflow](protocol/understanding-protocol.md#privacy-and-safety).

Real host tests use the tester's host usage allowance and may leave history in that host's own storage. Removing a temporary plugin package does not erase that history or change the account. Use the host's own controls for any deliberately chosen account or history cleanup; this plugin performs neither automatically.
