# A number-only Understanding Check

This is an illustrative conversation using the [synthetic whitespace fixture](../demo.md), not a live transcript or evidence of a real user's understanding. The behavior and record rules live in the [canonical protocol](../protocol/understanding-protocol.md#understanding-check).

After a coding task, invoke `/own-the-change:own-understanding-check` in Claude Code or select **Own The Change: Understanding Check** from Codex's `/skills` menu.

## Default interaction

This small, low-risk fixture uses two questions; a normal medium-risk check uses three and a high-risk check can use up to five. The agent shows only the current question:

> Two short questions for this low-risk change. Reply with a number. Say `stop` or `skip` to end, or `skip this question` to move on.
>
> Question 1/2: Which stated requirement motivated replacing the edge-only trim?
>
> 1. Remove only surrounding whitespace.
> 2. Normalize inconsistent whitespace in display names.
> 3. Reject names containing internal whitespace.
> 4. I'm not sure.

The illustrative user replies:

```text
2
```

The agent explains briefly, then asks the next planned question:

> The stated goal is consistent whitespace throughout names, not edge-only trimming or input rejection.
>
> Question 2/2: What does `display_name("   ")` return?
>
> 1. An empty string, `""`.
> 2. A single space, `" "`.
> 3. It raises an error.
> 4. I'm not sure.

The illustrative user replies `1`. The agent finishes:

> Whitespace-only input gives `split()` no words, so joining them returns an empty string. The fixture test covers this case. Check complete; no written explanation is needed. The tests do not settle whether the product should alter someone's intentionally chosen name spacing.

The [choice-only record](records/2026-09-11/whitespace-choice.md) preserves both original replies, their question mappings, and the feedback. Its response mode is `multiple_choice`; the record distinguishes selecting correct answers from independently explaining the reason and risk.

## If the answer is wrong or unsure

Choosing `1` for question 1 gets a short correction: the earlier edge-only trim did not meet the goal of normalizing internal whitespace too. Choosing `4` gets the same useful explanation without implying that the user guessed wrong. Either way, the agent continues to question 2 without a retry, remedial question, or essay. The [unsure record](records/2026-09-11/whitespace-unsure.md) shows that a later correct selection does not erase earlier uncertainty.

## Stopping early

Saying `Skip` before any answer ends the check with no substantive response. Saying `stop` after question 1 preserves that answer and leaves question 2 unchecked, as in the [early-stop record](records/2026-09-11/whitespace-stopped.md). Saying `skip this question` instead consumes that question's position and moves to the next planned question without adding a replacement. You can keep coding regardless of the recorded status.

## Optional explanation

If you want to explain the change yourself, say `Let me explain it in my own words.` Keywords can be enough; a polished paragraph is unnecessary. For example, the following fictional response adds independent reasoning beyond choosing a number:

```text
2. Standardize name spacing; this can also overwrite spacing someone intentionally chose. I'd check that product requirement before relying on it.
```

The agent records the selection and independently supplied explanation separately using `mixed`, and evaluates the actual explanation against the change evidence. Merely copying an option does not turn a selection into independent explanation.
