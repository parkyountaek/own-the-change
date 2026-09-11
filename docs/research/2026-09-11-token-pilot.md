# Codex token pilot: 0.2.3 versus 0.3.0

Measured on September 11, 2026. This is a local, eight-run descriptive pilot on one public synthetic change, not a benchmark of typical savings or a human-learning study. No product implementation was changed during measurement.

## Result

The candidate used less host-reported input on average in both scenarios. Mean uncached input fell by 22.2% for a brief Change Debrief and 20.0% for the first Understanding Check question. Mean output fell by 19.5% for the debrief but **increased by 3.2%** for the first question.

The four debriefs retained the inspected behavior, actual tests, limitations, and a related-fix starting point. Both candidate questions had four content choices plus uncertainty, but one still used weak distractors. More choices did not establish better discrimination or human understanding.

Each table cell below is an arithmetic mean followed by its observed minimum and maximum. There are only two runs per version per scenario. Percent change is `(candidate mean / baseline mean - 1) * 100`, not a mean of selected paired percentages.

| Scenario / metric | 0.2.3 mean (range) | 0.3.0 mean (range) | Change |
| --- | ---: | ---: | ---: |
| Debrief: input tokens | 102,820 (71,561-134,079) | 63,130.5 (54,499-71,762) | -38.6% |
| Debrief: uncached input tokens | 12,452 (11,913-12,991) | 9,690.5 (9,443-9,938) | -22.2% |
| Debrief: output tokens | 909.5 (820-999) | 732.5 (723-742) | -19.5% |
| Debrief: seconds | 70.244 (47.955-92.532) | 49.460 (48.281-50.638) | -29.6% |
| First question: input tokens | 130,943.5 (116,624-145,263) | 85,087 (75,957-94,217) | -35.0% |
| First question: uncached input tokens | 23,167.5 (21,615-24,720) | 18,527 (11,317-25,737) | -20.0% |
| First question: output tokens | 877.5 (836-919) | 906 (899-913) | +3.2% |
| First question: seconds | 77.857 (77.563-78.151) | 58.799 (56.140-61.457) | -24.5% |

Do not read these as guaranteed per-run reductions: candidate run 08 used more uncached input than either baseline first-question run, and baseline debrief run 04 finished slightly faster than either candidate debrief. Cache state and host overhead were not independently controlled.

## Method and controls

- Baseline: plugin 0.2.3, commit `f14d6d0b5199c9b81b022ecc9dad008862ce7908`.
- Candidate: plugin 0.3.0, commit `c6f3dbf41294d73cb6308dd9cd43b6b199224082`.
- Host: Codex CLI 0.154.0, macOS 26.6.2 (25G83), Python 3.12.0.
- Requested model: `gpt-6-astra`, reasoning effort `medium` for every run. This pins the requested alias and setting, not an immutable provider-side model snapshot.
- Archived committed `plugins/own-the-change` packages were copied into neutral, equal-length case paths. The named packaged skill was invoked by absolute file path, not through the installed marketplace or interactive skill picker.
- Each run used a fresh synthetic Git target prepared by the same candidate-revision `scripts/prepare_demo.py`. Its source fixture is unchanged between the compared revisions. Before-run hashes confirmed identical target file contents across all eight runs.
- The Git index contained the before implementation; there was no HEAD commit. The working tree normalized repeated whitespace and contained four tests. The prompt explicitly named this baseline and the two-file scope.
- Four fresh processes per scenario, in the prespecified order shown below. No reused conversation, supplied learner response, supplied test result, record save, or code edit.
- Normal host authentication; ignored user config; read-only sandbox; plugins, apps, hooks, multi-agent, and web search disabled for the measured process. The harness did not read or copy credentials. Normal account usage was consumed.
- Wall time measured with a monotonic clock around each Codex subprocess, excluding fixture and package preparation. Timeout: 480 seconds per process.
- The schedule, measures, and output-review criteria were written before inspecting generated answers. All eight planned runs completed; no retries or discarded samples.

The same prompt was used within each scenario, except for its required case-specific skill path:

```text
Use the skill at {skill}. The task is to normalize repeated whitespace in display names. Only display_name.py and test_display_name.py are in scope. The Git index is the before baseline; there is no HEAD commit. Explain in Korean. Do not edit code or save any learning record. {task}
```

| Scenario | Packaged skill directory | Task suffix |
| --- | --- | --- |
| Debrief | `skills/own-change-debrief` | `Run only a brief Change Debrief, without understanding questions.` |
| First question | `skills/own-understanding-check` | `Run an Understanding Check. Start with the first question and wait for my reply.` |

Each process used this command shape, with a fresh target and absolute paths:

```sh
codex exec --ignore-user-config --ephemeral --sandbox read-only \
  --disable plugins --disable apps --disable hooks --disable multi_agent \
  --config 'web_search="disabled"' \
  --model gpt-6-astra --config 'model_reasoning_effort="medium"' \
  --json -C "$case_target" --output-last-message "$case_answer" "$case_prompt"
```

`turn.completed.usage` was captured from the actual JSONL stream. Input already includes cached input; uncached input is the derived difference, not another host-supplied field. Output and reasoning-output fields are preserved separately without adding them together. These are execution-level usage values, not the tokens in the final paragraph or the plugin instruction file alone. The event and output conventions follow the [official Codex non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode).

Local harness SHA-256: `cd0f3479605203ecff4277f6d2ca3ea0db8d663abe95ee66322c74701c852257`.
Local prespecified review-plan SHA-256: `8f6ea9d8c59c9e984e0f9dd617f5c279ae784b00525a97335cd8c8f5af8db68b`.

## All measured runs

The order is debrief A-B-B-A, then first question B-A-A-B, where A is 0.2.3 and B is 0.3.0. Reasoning is the host's `reasoning_output_tokens`; `cache_write_input_tokens` was zero in every run.

| Run | Scenario | Version | Input | Cached input | Uncached input | Output | Reasoning | Seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 01 | Debrief | 0.2.3 | 134079 | 121088 | 12991 | 999 | 15 | 92.532 |
| 02 | Debrief | 0.3.0 | 54499 | 45056 | 9443 | 723 | 0 | 50.638 |
| 03 | Debrief | 0.3.0 | 71762 | 61824 | 9938 | 742 | 0 | 48.281 |
| 04 | Debrief | 0.2.3 | 71561 | 59648 | 11913 | 820 | 0 | 47.955 |
| 05 | First question | 0.3.0 | 75957 | 64640 | 11317 | 899 | 0 | 56.140 |
| 06 | First question | 0.2.3 | 116624 | 91904 | 24720 | 836 | 8 | 77.563 |
| 07 | First question | 0.2.3 | 145263 | 123648 | 21615 | 919 | 19 | 78.151 |
| 08 | First question | 0.3.0 | 94217 | 68480 | 25737 | 913 | 0 | 61.457 |

Command counts are completed `command_execution` items, not individual shell commands or model requests. Character counts are Unicode text lengths, not token estimates.

| Run | Command items | Nonzero command items | Tool-output characters | Final-answer characters |
| --- | ---: | ---: | ---: | ---: |
| 01 | 5 | 0 | 34331 | 563 |
| 02 | 6 | 0 | 23391 | 620 |
| 03 | 6 | 0 | 24142 | 556 |
| 04 | 9 | 0 | 32734 | 665 |
| 05 | 6 | 0 | 30268 | 363 |
| 06 | 5 | 0 | 35067 | 405 |
| 07 | 8 | 1 | 36577 | 382 |
| 08 | 7 | 0 | 30283 | 347 |

Run 07 included an `rg --files -g AGENTS.md` search with no matches, yielding exit 1. Its Codex process and actual test command still exited 0; the run remains in every aggregate. Git commands also emitted macOS Xcode/xcrun cache and filesystem warnings under the read-only sandbox. These warnings and their overhead were retained, not removed from measured output or time.

## Evidence and output review

The implementing assistant reviewed these outputs against the actual diff and captured command output. This was not an independent or blinded human evaluation, and no numerical quality or learning score is claimed.

### Tests and preservation

Every run inspected the scoped change and executed the fixture tests exactly once. The actual Python command was `python3 -B -m unittest -v test_display_name` in runs 01 and 04, `python3 -B -m unittest -v test_display_name.py` in runs 02, 03, and 07, and `python3 -B -m unittest test_display_name.py` in runs 05, 06, and 08. Each execution reported four tests and `OK`, with command exit 0.

The tests cover surrounding whitespace, repeated internal whitespace including a tab, whitespace-only input, and a nonbreaking space. This is test coverage for a tiny formatter, not for a production integration.

All eight processes exited 0 without a timeout or terminal error event. Before/after checks confirmed unchanged target file hashes and Git index hashes. There were no completed file-change events and no `docs/ai-understanding` directory. No learner answer or learning record was created.

### Brief Change Debrief

All four final debriefs explained the change from `value.strip()` to `" ".join(value.split())`, tied it to internal whitespace normalization, separated the incidental module-docstring change, reported the four passing tests, and named important untested boundaries. They identified preserving particular whitespace characters as a possible requirement conflict and pointed to the formatter and tests for a related fix. Only run 04 explicitly spelled out `test_display_name.py` as the follow-up location; the others identified tests by command or referred to the corresponding tests.

No debrief added unsolicited understanding questions, invented a successful test, or claimed the user understood the code. These observations support retained coverage on this fixture, not equal quality for all tasks.

Candidate runs loaded the debrief-specific protocol selection, whose command output was 16,397 characters. The baseline loaded the full 24,556-character protocol plus its shared entry instructions. The smaller load is consistent with the intended selective-loading mechanism, but this version comparison does not isolate the causal effect of the 250-character entry limit from other 0.3.0 changes or host behavior.

### First Understanding Check question

All four runs presented only question 1 of a planned two-question low-risk check, invited a number-only reply, offered uncertainty and stopping, and then waited. None requested an essay or invented a response. Showing one current question is not evidence that the planned check has been reduced to one question.

| Run | Content choices + uncertainty | Best position | Ordering helper | Reviewer observation |
| --- | --- | ---: | --- | --- |
| 05 | 4 + 1 | 3 | Ran once; displayed order matched output | Single supported answer, but capitalization and rejecting spaced names were weak distractors. |
| 06 | 3 + 1 | 1 | Not used | Single supported answer; capitalization was a weak distractor. |
| 07 | 3 + 1 | 1 | Not used | Single supported answer; capitalization was a weak distractor. |
| 08 | 4 + 1 | 2 | Ran once; displayed order matched output | Distractors concerned preserving edges, removing all spaces, and preserving tabs; closer to distinct whitespace misunderstandings. |

The baseline positions were checked against the fixture; candidate positions also matched `prepare_question.py` output. No final answer marked the correct choice or supplied a solution before a reply. The helper's tool trace contains its key, so this is not a secure examination interface. Two fresh first questions do not test randomness, within-session non-repetition, or the rest of the planned sequence.

All first questions asked about the reason for the change. This pilot did not reach a behavior-prediction or related-repair question, wrong-answer correction, or a delayed check. Output was Korean and allowed short selections; perceived naturalness and lower answering burden require real participant feedback.

## Limits and next measurement

- One small fixture, one client, one requested model alias, one environment, and two samples per cell cannot establish general savings or statistical significance. No confidence interval is claimed.
- Shared prompt caching was not reset or guaranteed; fresh processes are not guaranteed cold-cache runs. Uncached first-question input varied substantially even within the candidate condition.
- Host scheduling, service latency, and local Git warnings affect elapsed time. The time reduction cannot be attributed entirely to shorter instructions.
- This is direct packaged-skill invocation, not an installed marketplace/picker acceptance test. Claude, other models, Windows/WSL, and normal interactive discovery were not measured.
- Initial invocations only: no resumed number-only replies, full two/three/five-question sequence, saved-record flow, or cross-turn evidence reuse was measured.
- There was no no-plugin control, so this does not measure incremental cost versus asking the agent to explain a diff without the plugin.
- Host tokens are not an invoice. Monetary savings, subscription-limit effects, human comprehension, experienced burden, retention, and transfer to maintenance work remain unknown.
- Raw session logs and generated answer transcripts are intentionally not included in the repository report. The report contains synthetic-fixture measurements and English review observations, not private source code or participant records.

Next, strengthen the requirement for plausible, change-specific distractors and test it across distinct changes before claiming improved discrimination. A separate, consented study could measure completion time, skipped questions, and voluntary perceived difficulty, then use a new small input or repair task after a delay to assess retention or transfer. Do not substitute generated learner replies or token savings for those observations.

For cost follow-up, prespecify more fixtures and repetitions, include a no-plugin control, and measure full continuous conversations separately from first invocations. Record cache fields and failures as above; do not pool unmatched host settings or silently replace unsuccessful runs.
