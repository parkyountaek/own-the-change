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

In a real checkpoint, the agent saves and validates a local record and reports its path. Skipping questions does not establish understanding. The [protocol](protocol/understanding-protocol.md) governs the actual workflow; this page is not a learning record.

## Try the real workflow

Install the plugin using the [README](../README.md#install-and-verify). To reproduce the example without using private project code, download or clone this repository and run from its root:

```sh
python3 scripts/prepare_demo.py
```

The script prints the new temporary directory and commands to enter it, inspect the diff, and run:

```sh
python3 -m unittest discover -s . -p 'test_display_name.py' -v
```

Open Claude or Codex in that printed directory and use the prompt above. The script prepares only fictional files in a fresh Git repository. It does not launch an agent, create a learning record, or change your existing project's files or ignore settings. Its new synthetic repository excludes local records from Git. No commit, Git identity, separate API key, or live account is needed for fixture preparation; a real agent session uses your normal host account and permissions.

The directory remains available after the script exits. When finished, remove only that printed demo directory using your file manager. For all checkpoints and adversarial scenarios, see the [host smoke test](host-smoke-test.md).

Tried it? Share an optional, sanitized [first-use report](../.github/ISSUE_TEMPLATE/first_use_feedback.md). A useful report says what was hard to find or explain; it does not need your code or record.
