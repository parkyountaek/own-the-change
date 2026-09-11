# A 45-second walkthrough

An illustrative reading walkthrough, not a recorded AI session. The change and four test cases come from the [synthetic smoke fixture](../tests/fixtures/host-smoke/after). No real user answer or learning outcome is represented.

## 1. The change looks tiny

```diff
 def display_name(value):
-    return value.strip()
+    return " ".join(value.split())
```

The goal is to collapse repeated whitespace in display names. Tests passing is only one part of understanding this change.

## 2. Select Change Debrief

In Claude: `/own-the-change:own-change-debrief`.

In Codex CLI: `/skills` → **Own The Change: Change Debrief** → send. No separate instruction is needed when the task is clear.

For this fixture, add: `Debrief display_name.py and test_display_name.py. Use the index as the before baseline; there is no HEAD commit. Skip understanding questions.`

## 3. Keep the explanation that matters

An illustrative debrief:

- **What and why:** `strip()` removes edge whitespace. Splitting and joining also collapses internal whitespace to one ordinary space, matching the stated normalization goal.
- **Files and impact:** `display_name.py` changes the formatter; `test_display_name.py` exercises it. Any caller relying on internal spacing could observe a change.
- **Test evidence:** the runnable fixture contains four passing cases: surrounding whitespace, repeated internal whitespace, whitespace-only input, and nonbreaking space. Run the command below to get your own result.
- **Limits:** these unit tests do not cover non-string input, every Unicode separator, UI rendering, or downstream callers.
- **Risk and next fix:** preserving a person's preferred spacing is a product decision the tests do not settle. Start in `display_name`, agree on that requirement, and add the missing case.

## 4. Return to it when you need it

In a real checkpoint, you can save a validated local record or finish without saving. Skipping questions does not establish understanding. The [protocol](protocol/understanding-protocol.md) governs the actual workflow; this page is not a learning record.

## Try the real workflow

Install or update to plugin 0.3.0 using the [README](../README.md#install-and-verify), then start a fresh session. No source clone is needed:

- Claude Code: `/own-the-change:own-demo`.
- Codex CLI: `/skills` > **List skills** > **Own The Change: Demo**, then send the selection.

The agent prepares the bundled fixture in a new temporary Git repository, runs its four tests, and explains the observed change and limits. The caller does not need to be inside Git. The demo defaults to no questions and no saved learning record. Ask for an Understanding Check if you want to try the number-only interaction.

For manual fixture preparation from a source checkout, the same helper remains available:

```sh
python3 scripts/prepare_demo.py
```

The script prints the new temporary directory and commands to enter it, inspect the diff, and run:

```sh
python3 -m unittest discover -s . -p 'test_display_name.py' -v
```

Open Claude or Codex in that printed directory and use the prompt above. The script prepares only fictional files in a fresh Git repository. It does not launch an agent, create a learning record, or change your existing project's files or ignore settings. Its new synthetic repository excludes local records from Git. No commit, Git identity, separate API key, or live account is needed for fixture preparation; a real agent session uses your normal host account and permissions.

The directory remains available after the script exits. When finished, remove only that printed demo directory using your file manager. For all checkpoints and adversarial scenarios, see the [host smoke test](host-smoke-test.md).

Tried it? Share an optional [first-use report](https://github.com/parkyountaek/own-the-change/issues/new?template=first_use_feedback.yml). Selections are enough; written explanations, code, and records are not required.
