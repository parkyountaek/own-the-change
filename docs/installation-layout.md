# Installation layout

## Local use

- Claude Code: run `python3 scripts/launch_claude.py /absolute/path/to/your-project` for a temporary, session-only installation
- Codex: automatically discovers `.agents/skills/own-the-change` at the repository root
- Cursor: a `.cursor/skills/own-the-change` discovery link is provided; runtime unverified
- GitHub Copilot and other Agent Skills-compatible tools: a `.agents/skills/own-the-change` link is provided; runtime unverified

The repository keeps one shared skill in `skills/own-the-change/`. Discovery paths are symbolic links only. The common rules live only in `docs/protocol/understanding-protocol.md`.

The Claude launcher checks for Claude Code, Git, and a valid target repository before building. It creates a fresh temporary package for each session, starts Claude in the requested directory, and removes that package when Claude exits. It does not install a marketplace or change host configuration. It doesn't erase Claude's own conversation history. Use a manual build and marketplace installation when you need a package that remains available after the session.

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

## Not published yet

`templates/claude-marketplace.json` is copied to the generated Claude marketplace root. Its relative source is `./own-the-change`, not the incomplete source adapter. The Codex manifest is copied into the Codex package; the builder does not create a Codex marketplace or alter a personal marketplace. This repository currently does not publish or push externally; use the local paths above while developing.

Automated tests cover resource lookup after copying a package. Temporary Claude and Codex marketplace installations also passed a debrief with record creation and validation. Codex used its installed cache; Claude used the still-available local catalog package. Those test registrations were removed afterward. No public release or marketplace submission was made. See the [acceptance checklist](acceptance-checklist.md) for versions and remaining tests.

Use [the host smoke test](host-smoke-test.md) for synthetic task setup and [the release checklist](releasing.md) for catalog validation, cached installation, and distribution boundaries. Source changes do not refresh an earlier build; choose a fresh output and a fresh host session when retesting.

## Host account independence

Host authentication is separate from this plugin. The package does not bundle a tester's email, organization, account identifier, credentials, host settings, or session history. No account-specific marketplace or model identifier is needed to build it or run its local tests.

If access to a host account changes, sign in to an authorized replacement account using the host's own login flow, then load or install the same plugin package. This project does not transfer credentials, subscriptions, host conversation history, or organization-managed installations between accounts.

Local Markdown records do not require the original account to be read, but their contents may belong to the project or organization that produced them. Portability is not permission to copy those records or any source code. Review ownership and sharing restrictions before moving project data. Keep actual records separate from distributable plugin files using the [canonical privacy workflow](protocol/understanding-protocol.md#privacy-and-safety).

Real host tests use the tester's host usage allowance and may leave history in that host's own storage. Removing a temporary plugin package does not erase that history or change the account. Use the host's own controls for any deliberately chosen account or history cleanup; this plugin performs neither automatically.
