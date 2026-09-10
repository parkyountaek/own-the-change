# Your AI changed the code. Can you explain why?

![Own The Change: a code diff becomes an annotated note, for Claude Code and Codex.](https://raw.githubusercontent.com/parkyountaek/own-the-change/main/docs/assets/own-the-change-social.jpg)

I'm building **Own The Change**, an open-source plugin for the moment after an AI coding task: the tests pass, but you still need to explain what changed, why, and where to start a related fix.

A **Change Debrief** uses the actual diff and test evidence, explains decisions and gaps, and saves a local Markdown record. Understanding questions are optional. It does not score you or approve your code.

## Try it without a manual clone

Inside Claude Code:

```text
/plugin marketplace add parkyountaek/own-the-change
/plugin install own-the-change@own-the-change
```

Start a new Claude session in your project and run `/own-the-change:own-change-debrief` after a coding task.

For Codex CLI, run in your terminal:

```sh
codex plugin marketplace add parkyountaek/own-the-change
codex plugin add own-the-change@own-the-change
```

Start a new Codex session in your project. Use `/skills` > **List skills** > **Own The Change: Change Debrief**, then send the selection. See the [installation guide](https://github.com/parkyountaek/own-the-change#install-and-verify) for requirements and tested client versions. Already installed? Use the [update guide](https://github.com/parkyountaek/own-the-change/blob/main/docs/updating.md).

## Help shape the first version

The [small synthetic demo](https://github.com/parkyountaek/own-the-change/blob/main/docs/demo.md) lets you try the workflow without sharing real work code. I'm looking for the first ten developers willing to try a debrief and optionally return on a second task within a week. This is an invitation, not a claim that ten people have already used it.

I'd especially like to know:

- Was installation and finding the right action straightforward?
- Did the debrief add anything beyond asking the agent to explain its diff?
- Would you use it again? What would need to change?

Leave a non-sensitive reply here or use the [first-use feedback guide](https://github.com/parkyountaek/own-the-change/blob/main/docs/launch/early-access.md). Host/plugin versions and the confusing step are enough; do not post private source code, learning records, logs, or credentials.

The project is experimental. We have not measured a long-term learning benefit. It adds no separate server, API key, or telemetry; your coding agent's own data policies still apply.

Created and maintained by [@parkyountaek](https://github.com/parkyountaek), with [AI development assistance from OpenAI Codex](https://github.com/parkyountaek/own-the-change/blob/main/CONTRIBUTORS.md). This is an independent community project, not an official OpenAI or Anthropic plugin.
