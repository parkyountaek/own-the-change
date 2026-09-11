# Use Own The Change in Codex

Install the [native plugin](../README.md#codex-cli), open the project you changed, and start a new session.

## Choose an action, then send

In Codex CLI, type `/skills`, choose **List skills**, and search for `own-change`. Select **Own The Change: Change Debrief**, then send the inserted skill mention. You can also type `$` to open the list directly. When the current task is clear, you do not need to write a separate instruction.

| Action | Claude Code | Codex CLI skill mention |
| --- | --- | --- |
| Explain a completed change | `/own-the-change:own-change-debrief` | `$own-the-change:own-change-debrief` |
| Think through a change before coding | `/own-the-change:own-plan-check` | `$own-the-change:own-plan-check` |
| Take a quick multiple-choice check | `/own-the-change:own-understanding-check` | `$own-the-change:own-understanding-check` |

Codex CLI 0.153.4 reports the plugin-qualified names above. You do not need to type them out: select the entry from **Own The Change** and keep the mention inserted by your client. Unqualified shortcut names are not a verified alias. Add filenames or a task description when multiple changes are present. If the scope is missing, the agent asks which task you mean.

The original **Own The Change** entry remains supported. Its local-skill name is `$own-the-change`; the native plugin reports `$own-the-change:own-the-change`. Invoking it alone starts a Change Debrief; naming another checkpoint selects that workflow. Asking how to install or use the plugin does not start a checkpoint.

Understanding Check uses numbered choices in the conversation, so you can send just a number; it does not depend on a native form or a special slash command for answers. See the [multiple-choice walkthrough](examples/multiple-choice-check.md). Ask to explain it in your own words only when you want that deeper mode.

## Why not `/own-change-debrief`?

Codex CLI's documented route is `/skills` or a `$` mention. Claude plugin commands are a different interface; installing this plugin does not register Claude-style slash commands in Codex. Legacy `/prompts:...` custom prompts are deprecated, so this package does not install files into your personal prompts directory. See the official [skills guide](https://learn.chatgpt.com/docs/build-skills), [CLI command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli), and [custom prompt notice](https://developers.openai.com/codex/custom-prompts).

Desktop surfaces can expose a different picker. The official skills guide describes `@` selection in ChatGPT and `/skills` or `$` in Codex CLI/IDE. Do not assume that the CLI menu exists in every desktop app or third-party wrapper. The package includes display names, descriptions, and starter prompts for clients that expose this metadata. Desktop picker behavior still needs a hands-on check.

## Update an existing installation

Run in a terminal:

```sh
codex plugin marketplace upgrade own-the-change
codex plugin add own-the-change@own-the-change
```

Start a new thread to load the updated skills. Use `/plugins` to check installation and `/skills` to choose an action; installing a plugin does not itself run a debrief.

If you installed only the legacy local skill link, it exposes **Own The Change**, not the three native-plugin shortcuts. Refresh that source checkout and send `$own-the-change`, or follow the [marketplace migration guide](installation-layout.md#github-marketplace). Avoid installing duplicate copies under different scopes.

## If the action is missing

- Check `codex --version` and whether `codex plugin` is supported. Installation checks used CLI 0.153.4; untested clients may differ.
- Confirm the plugin is enabled in `/plugins`, then start a fresh session.
- Search `/skills` for `own-change`, not Claude's `/own-the-change:...` command.
- When two entries share a name, select the one from the intended plugin source. Codex does not merge duplicate skills.

All entry points use the same [understanding protocol](protocol/understanding-protocol.md). The shortcuts select a checkpoint; they do not introduce new learning, record, or privacy rules.
