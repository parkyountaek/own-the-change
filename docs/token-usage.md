# Context and token use

Own The Change uses the host agent's normal model and account. It has no separate model call, token meter, subscription, or telemetry service. A fixture test or a shorter prompt is not evidence of a lower bill.

## What changes in 0.3.0

- Each skill/command entry body is limited to 250 characters, excluding YAML discovery metadata. An automated check enforces this limit; characters are not tokens.
- The protocol reader loads complete relevant sections from one canonical document. A debrief does not load the quiz procedure, planning procedure, or record schema before they are needed.
- The host is instructed to reuse current evidence and loaded rules across number-only answers instead of rereading files and rerunning tests each turn.
- Scope inventories precede focused diff/caller/test inspection. Generated duplicates, unrelated history, and full logs are not default context.
- Questions have four short content choices plus uncertainty. The ordering helper returns only reordered choices and a key, not repeated question text and rationale.
- A saved record is normally written and validated once at completion or early stop. Conversation-only mode does not load a template or write a record.

These are instruction and tooling changes, not a host-enforced token ceiling. The [canonical efficiency rules](protocol/understanding-protocol.md#efficient-execution) preserve required evidence, privacy, and risk checks. Broader inspection remains appropriate when the change requires it. More choices can increase output; not every task will cost less.

## Request a smaller checkpoint

After selecting Change Debrief, you can say:

```text
Keep it brief and do not save a record.
```

For Understanding Check, you can request one question or stop early. A compact answer still needs to identify the change, actual tests, and important unknowns. The plugin does not change your model, reasoning settings, context limits, or billing configuration.

## Measure honestly

Use the same client/model/settings and comparable task scope when comparing versions. Record only host-supplied per-execution input/output/cached-token data and whether a record was saved; separate first invocation from subsequent answers. Do not publish raw session logs or private code. If the host does not provide attributable usage, report `unknown` rather than estimating from characters or account totals. A single run cannot establish typical savings or equal learning quality.

The [September 11 pilot](research/2026-09-11-token-pilot.md) compared 0.2.3 with 0.3.0 on one synthetic change: mean input fell, but first-question output increased and per-run cache behavior varied. It does not measure 0.3.1, a complete conversation, typical bills, or human learning.
