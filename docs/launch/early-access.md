# Try Own The Change on two tasks

We are looking for the first ten developers who regularly use Claude Code or Codex and sometimes struggle to explain an AI-generated change in a pull request or later bug fix. This is an invitation, not a claim that ten people have joined.

## First task

1. [Install the plugin](../../README.md#install-and-verify) in your existing coding agent.
2. Choose a small finished change, or use the [synthetic demo](../demo.md) if you cannot use work code.
3. Run one Change Debrief. You can skip understanding questions.
4. Optionally share [first-use feedback](https://github.com/parkyountaek/own-the-change/issues/new?template=first_use_feedback.yml). Select the host, progress, usefulness, and actual repeat use; written explanations are optional.

No signup form, extra API key, or mandatory feedback is required. A real host session uses your normal account and usage allowance. The [canonical privacy guidance](../protocol/understanding-protocol.md#privacy-and-safety) applies; participation does not require sharing code or learning records.

## Another task within a week

If another suitable task comes up, try a second debrief. Update your own feedback issue with whether you actually used it again and why. If no suitable task occurred, say that rather than treating it as a failure. A maintainer may ask one public follow-up only when you opted in on that issue. The plugin does not send reminders or collect usage analytics.

## What maintainers should learn

For an optional comparison, use two similar small tasks: on one, ask your agent to explain its diff; on the other, run Change Debrief. Alternate which approach comes first across willing participants. Select whether the plugin was more useful, about the same, or less useful, and optionally note whether it helped identify a test limit or the starting point of a related fix. This is informal feedback: task differences, order effects, and self-selection prevent a causal learning claim. Do not require a second paid run on the same task merely for comparison.

If a user voluntarily returns after a few days, distinguish remembering a rationale, recognizing a choice, and applying the idea to a new case. Ask for no code, private record, or essay. Correct immediate selections alone cannot establish retained understanding. The [learning design review](../research/learning-principles.md#implementation-review-030) lists the intended mechanisms and remaining evidence gaps.

Track voluntary reports, not hidden telemetry. Report these separately, with counts and denominators:

| Question | Evidence |
| --- | --- |
| Can people get started? | Successful first debriefs / participants who reported attempting installation |
| Is the explanation useful? | Concrete self-reported insights and remaining gaps; no agent-assigned score |
| Do people choose to return? | Reported second-task uses / respondents with another suitable task within seven days |
| What is still unknown? | Missing follow-ups and people without another task, shown separately |

The initial target is ten attempted first uses, followed by enough actual second-task reports to understand reuse. Do not count stars, install intent, or a maintainer's fixture run as repeat use. Voluntary feedback is a biased sample, not evidence of a proven learning effect.

Prefer fixing the most repeated installation or action-selection barrier before expanding promotion. Obtain explicit permission before publishing quotes, names, or stories from reports. Recruitment copy and submission preparation are in the [launch drafts](recruitment.md) and [directory kit](directory-submission.md).
