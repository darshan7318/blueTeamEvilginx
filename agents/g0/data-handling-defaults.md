# G0 data-handling defaults — portable local mode

**Status:** PM-01 policy proposal for G0. DATA-06 and SEC-04 review, runtime enforcement, and assurance evidence are still pending.

## Default data path

- Process normalized JSONL locally. Do not upload telemetry or contact external services in portable mode.
- Keep raw input in the caller-provided file; do not copy it into an application database, prompt cache, crash report, or audit log.
- Keep normalized event values in memory only for correlation. Discard them when the run completes.
- Write findings only to the explicitly selected output path. Findings contain source event references, event-type/time evidence, and pseudonymous subject IDs; they do not copy raw event objects.
- Keep prompt bundles and model context ephemeral. No prompt or case data is retained after invocation.
- Write audit metadata locally only: run ID, timestamp, prompt snapshot, role ID, counts, gate decision, result IDs, and error codes. Never log event payloads, secret values, full URLs, email bodies, raw IPs, or provider credentials. Proposed metadata retention default: 30 days, configurable downward or upward by local policy.

## Ingestion and redaction

- Apply a strict field allowlist from `docs/event-schema.md`. Drop unknown fields before correlation or model context construction.
- Reject a record before storage/model use if it contains a forbidden secret field (password/passcode, OTP/MFA code, access/refresh/id token, cookie/set-cookie, authorization header, private key, secret, raw request/body). Record only the line number, safe event ID if available, and redaction error code.
- Also scan values for credential/token formats. On a likely secret match, reject the whole record and stop the case bundle from reaching any model; do not echo the match in diagnostics.
- Redact PII not required for behavior correlation. Preserve only the minimum evidence needed for the stated detection or investigation question.
- Never include message bodies, attachments, raw HTTP payloads, passwords, MFA material, cookies, bearer/refresh tokens, private keys, or unredacted credentials in prompts, logs, examples, or outputs.

## Identifier handling

- Replace usernames/email addresses with tenant-scoped pseudonyms before persistence or model use. Keep any mapping key outside the prompt/runtime context.
- Use opaque, provider-issued event IDs where verified safe; otherwise store a keyed hash as the citation handle.
- Treat session IDs as opaque correlation references only; reject values that resemble credentials or session-cookie content.
- Keep IP/ASN and full user-agent strings in local in-memory correlation only. Model context uses coarsened network/client attributes where sufficient; findings cite source event IDs rather than copying raw values.
- Hash device and mailbox targets before persistence/model use unless the investigation question requires the original value and policy explicitly allows it.

## Storage, access, and retention

- Default storage is local-only. Do not create a database or hidden cache in portable mode.
- Create output/log files with owner-only permissions (POSIX mode 0600; equivalent user-only ACL on Windows). If the platform cannot apply the requested ACL, fail closed for sensitive output.
- Findings are written only to a user-selected path and remain until explicitly deleted; the application has no hidden retention copy. Audit metadata defaults to 30 days, pending DATA-06/SEC-04 approval.
- Do not store secrets in environment files, prompts, configuration, crash dumps, or command-line arguments. Future external-provider credentials must use the OS credential store and remain disabled by default.
- Backups and exports are explicit, local, and redacted. No automatic sync, telemetry, or crash upload.

## Inference and tools

- Deterministic detection works without a model and without network access.
- External model providers are disabled by default. If enabled in a later approved configuration, transmit only minimized, redacted case facts and event citations; do not send raw logs or identifiers.
- Agent tool grants are empty in the current portable profile. No external browsing, filesystem-wide access, shell, identity-provider writes, mailbox writes, user contact, or takedown actions.
- A redaction failure, policy mismatch, or unavailable local permission control blocks model invocation and side effects.

## Required validation before G0 can pass

DATA-06 and SEC-04 must review this proposal. A later authorized implementation must demonstrate secret-field rejection, value redaction, unknown-field dropping, output permission enforcement, no unexpected network/storage writes, and deletion/retention behavior using synthetic data. Until those controls are implemented and independently reviewed, this file is policy intent only.

