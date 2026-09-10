# Directory submission kit

Prepared for maintainer review. **Not submitted, approved, or officially listed.** The GitHub marketplaces work independently of vendor directory review. Requirements below were checked against official documentation on September 10, 2026; recheck them before submitting.

## Reusable copy

- **Name:** Own The Change
- **Short description:** Explain AI code changes, their reasons, risks, and test limits.
- **Category candidate:** Productivity
- **Repository:** https://github.com/parkyountaek/own-the-change
- **Publisher label:** Own The Change contributors. This is package metadata, not a claim of a verified legal identity.
- **Description:** Own The Change helps developers review what their AI coding agent changed. Run a Change Debrief, optional Plan Check, or optional Understanding Check, using the actual diff and available test evidence. Keep a local Markdown explanation for later maintenance. It does not edit or approve code, score understanding, send reminders, or add telemetry. The host's model execution and data policies still apply.
- **Demo:** [synthetic walkthrough](../demo.md)
- **Support:** [support routes](../../SUPPORT.md)
- **Privacy behavior:** [canonical protocol](../protocol/understanding-protocol.md#privacy-and-safety). This is technical behavior documentation, not a substitute for a required publisher privacy policy or terms.

## Claude directory

Use the public GitHub repository and the complete package at `plugins/claude-code/own-the-change`. The catalog is `.claude-plugin/marketplace.json`.

Before applying, run Claude's plugin validator and the [release checks](../releasing.md), then review the official [submission instructions](https://claude.com/docs/plugins/submit). The Console submission route requires the appropriate organization role. The author must supply any required identity, contact, and listing fields. Directory acceptance and verification are vendor decisions, not results of this project's unit tests.

## OpenAI directory

OpenAI's [submission guide](https://developers.openai.com/plugins/deploy/submission) supports skills-only plugins. Start from the complete native package at `plugins/own-the-change`, not just one `SKILL.md`; its referenced protocol, template, and Python helpers are required.

The maintainer still needs to provide or verify:

- Publisher identity and appropriate Apps Management access.
- Listing logo, website, support contact, privacy-policy and terms URLs accepted by the portal.
- Supported product surfaces and availability. Do not claim ChatGPT web/mobile compatibility from local Codex CLI tests; this workflow requires local Git and Python access.
- Current test evidence, release notes, and accurate policy attestations.

Do not create an MCP server or a data collection service just to fill the form. Do not treat repository installation as universal-directory acceptance.

### Review scenarios

These are proposed cases with expected behavior, not assertions that they were all run. Use the [smoke fixture](../host-smoke-test.md) and record observed outcomes separately.

| Case | Starter request | Expected behavior |
| --- | --- | --- |
| Positive 1 | Select Change Debrief with a clear current task | Debrief the actual change and available tests, including limits |
| Positive 2 | Select Plan Check with a synthetic task goal | Run only the Plan Check; do not implement code |
| Positive 3 | Select Understanding Check after a debrief | Ask appropriate questions and wait for the actual user response |
| Positive 4 | Select Change Debrief and add `Explain in Korean; skip questions.` | Follow the requested language and skip without claiming understanding |
| Positive 5 | Ask to review an existing synthetic local record | Follow the protocol's follow-up workflow while preserving the original |
| Negative 1 | Ask how to install the plugin | Explain setup without creating a learning record |
| Negative 2 | Ask to mark understanding confirmed because tests passed | Do not infer a user answer or confirmation from tests |
| Negative 3 | Supply a record path outside the target Git root | Reject the unsafe destination without writing there |

The author must review and submit through the vendor's own process. This kit neither submits an application nor makes policy attestations on the author's behalf.
