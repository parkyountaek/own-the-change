# Understanding protocol

## Purpose and scope

This is the only source of common learning rules for Own The Change. Claude Code, Codex, and other agents must link here rather than copy the rules. This tool does not write or modify code, score code quality, or approve pull requests.

## Before work: Plan Check

Before work begins, summarize the goal in one or two plain English sentences. Ask no more than three questions:

1. Which files or behavior may change?
2. What risk matters most?
3. Which test is likely needed?

Do not block work when the user does not answer. Record `not_confirmed`, or `unknown` when evidence is insufficient.

## After work: Change Debrief

Use only the actual `git diff` and actual test output. Explain:

1. What changed?
2. Why did it change?
3. Which files are affected?
4. Which tests actually ran?
5. What do those tests not prove?
6. What remains unverified or risky?

Do not repeat the whole codebase. Separate core behavior, tests, and incidental changes.

## Understanding Check

This is a conversation, not a quiz. Ask the user to explain the change without reading the code.

- `low`: one factual question
- `medium`: two questions about reason and impact
- `high`: at most three questions covering cause, consequence, and a new scenario

Respond with what is understood, what is missing, and the next check. Do not assign a score, offer vague praise, or treat the agent's self-assessment as evidence.

## Status

Follow [status definitions](status-definitions.md). Never use `confirmed` without a direct user response. Passing tests does not confirm understanding. Consider `confirmed` only when the user's answer and the actual change evidence support it.

## Records and follow-up

Use the [record schema](output-schema.md) and the template to write `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`. Leave unavailable `provider`, `model`, `turn`, `token`, and `cost` values as `unknown`.

For high-risk changes such as `authentication`, `authorization`, `payment`, `database migration`, `concurrency`, `deployment`, or `external integration`, record next-day and one-week follow-up dates in `follow_up_at`. This version does not send reminders.

## Privacy and safety

Do not send source code, environment variables, secrets, or complete terminal logs outside the local environment. Do not require an API key. Do not deploy, merge, or modify code automatically. Store only the necessary local summary of the visible repository diff and the user's answer.

## Readable output

Use this shape to keep the next action visible:

1. Put the current conclusion or one immediate action first.
2. When there are several steps, number them and keep one action per step.
3. For longer work, state what is complete and what comes next.
4. Split long lists into `Now` and `Later`.
5. For an error, state its cause, impact, and next check instead of adding filler.

This format was inspired by the action-first, small-step, visible-progress principles in [i-have-adhd](https://github.com/ayghri/i-have-adhd). Own The Change does not diagnose or treat ADHD and does not copy that project's code or wording. Clear explanation and safety take priority when the user requests detail or the change needs careful review.

## Research and product claims

The research basis and product hypotheses are in [learning principles](../research/learning-principles.md). The cited research does not guarantee that AI coding tools improve learning. Any effect in this product remains a hypothesis to test.
