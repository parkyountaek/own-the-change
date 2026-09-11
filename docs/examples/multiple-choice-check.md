# A number-only Understanding Check

This is an illustrative conversation using the [synthetic whitespace fixture](../demo.md), not a live transcript or evidence of a real user's understanding. The behavior and record rules live in the [canonical protocol](../protocol/understanding-protocol.md#understanding-check).

After a coding task, invoke `/own-the-change:own-understanding-check` in Claude Code or select **Own The Change: Understanding Check** from Codex's `/skills` menu.

## Default interaction

The agent asks one question:

> After this change, what does `display_name("Ada   Lovelace")` return?
>
> 1. `"Ada   Lovelace"`, preserving the internal spaces.
> 2. `"Ada Lovelace"`, with one internal space.
> 3. `"AdaLovelace"`, without an internal space.
> 4. I'm not sure.
>
> Reply with a number, or skip.

The illustrative user replies:

```text
2
```

The agent explains briefly and finishes:

> That's the behavior shown by the change: `split()` separates whitespace-delimited words and `join()` puts one space between them. This also changes intentional spacing in a name, so passing the fixture tests does not settle whether the product should do it. Check complete; no written explanation is needed.

The [choice-only record](records/2026-09-11/whitespace-choice.md) preserves the original `2`, the question and options, and the agent's feedback. Its response mode is `multiple_choice`; the record distinguishes selecting a correct answer from independently explaining the reason and risk.

## If the answer is wrong or unsure

Choosing `1` gets a short correction: the new behavior collapses internal spaces too; trimming only the edges was the earlier behavior. Choosing `4` gets the same useful explanation without implying that the user guessed wrong. Neither response requires a retry or an essay. The [unsure record](records/2026-09-11/whitespace-unsure.md) illustrates that distinction.

Saying `Skip` ends the check without a substantive answer. You can keep coding regardless of the recorded status.

## Optional explanation

If you want to explain the change yourself, say `Let me explain it in my own words.` Keywords can be enough; a polished paragraph is unnecessary. For example, the following fictional response adds independent reasoning beyond choosing a number:

```text
2. Standardize name spacing; this can also overwrite spacing someone intentionally chose. I'd check that product requirement before relying on it.
```

The agent records the selection and independently supplied explanation separately using `mixed`, and evaluates the actual explanation against the change evidence. Merely copying an option does not turn a selection into independent explanation.
