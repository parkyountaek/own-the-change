# Security

## Scope and current support

This project is experimental. Security fixes target the development branch. We don't guarantee backports or response times for older builds. Review the source and use a repository with fictional code when trying the plugin for the first time.

The plugin adds no network service or telemetry. The coding agent that loads it may use a remote model, and its permissions and data-handling settings still apply. This is not an offline sandbox or a security approval tool. Learning records can contain sensitive project context even when they contain no source code.

The [privacy and safety policy](docs/protocol/understanding-protocol.md#privacy-and-safety) defines what the plugin may do. Its helper scripts catch common path and record errors, but they can't prevent every unsafe agent action or protect against files changing during a check.

## Report a concern privately

GitHub private vulnerability reporting was disabled when checked on September 10, 2026. Until a private channel is verified, do not post sensitive details. Maintainers should recheck this setting before a release.

If the repository's GitHub Security tab offers **Report a vulnerability** after it is enabled, use that private reporting channel.

If private reporting is unavailable, open an issue asking the maintainer for a private contact method, without exploit details, source code, secrets, records, or logs. Wait for a private channel before sending sensitive information. There is no verified project security email to use as a fallback.

A useful private report includes the affected plugin version and host, a minimal synthetic reproduction, observed impact, and a proposed mitigation if known. Do not send a real repository, environment variables, authentication material, or complete terminal logs.

For ordinary installation failures without sensitive impact, use a sanitized public bug report. Maintainers should establish and verify a private reporting channel before a public release; see the repository's release checklist.
