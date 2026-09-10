# Recruitment drafts

Drafts only. Nothing on this page indicates that a community post, message, or vendor submission was sent. Check each community's rules and finish the private conduct-reporting setup in the [release checklist](../releasing.md) before broader outreach.

For the campaign image, shorter social copy, and a small launch sequence, use the [sharing kit](media-kit.md). The [GitHub announcement copy](github-announcement.md) is maintained separately; a source file alone is not evidence of publication.

## Short post

Your AI changed the code. Can you explain why?

I'm building Own The Change, an open-source plugin for Claude Code and Codex. After a coding task, it explains the actual diff, why it matters, what the tests missed, and where to start a related fix. It keeps a local Markdown record; understanding questions are optional.

I'm looking for ten developers to try a debrief and, if it helps, use it on another task within a week. A synthetic example is available, so you do not need to share work code or records. I'd especially like feedback on installation and finding the right action.

[Try it](https://github.com/parkyountaek/own-the-change) · [Small demo](https://github.com/parkyountaek/own-the-change/blob/main/docs/demo.md) · [Trial instructions](early-access.md)

## Show HN draft

Title: **Show HN: Own The Change - explain the code your AI agent just changed**

I built this around a problem with AI-assisted coding: a task can be done and its tests can pass while the developer still cannot explain a key decision or where to fix a related bug.

Own The Change is a small plugin for Claude Code and Codex. It reads the actual change and test evidence, gives a debrief, and saves a local Markdown record. Optional questions help identify gaps; the plugin does not score understanding, approve code, or send reminders. It has no separate server or telemetry, though the coding agent's existing model and data policies still apply.

You can install it with the hosts' plugin commands. The repository also includes a synthetic whitespace-normalization change to try without using a real project. Codex CLI users can select a checkpoint from `/skills`; Claude users get named slash commands.

It is experimental. I have not measured whether it improves long-term recall. I would value feedback on what the debrief adds beyond asking the agent to explain its diff, and whether you would return to it on another task.

Project: https://github.com/parkyountaek/own-the-change

Before posting, run the linked installation/demo steps on the current public revision. The official [Show HN guidelines](https://news.ycombinator.com/showhn.html) call for something people can try; do not ask for coordinated votes. Replace drafts with genuine observations only after they exist.
