# Event schema

Input is newline-delimited JSON. Required: `timestamp` (ISO 8601), `event_type`, and `user` for correlation. Keep one event per line. The target ingestion policy is a strict allowlist: unknown fields are dropped, and records with prohibited secret fields or likely secret values are rejected before persistence or model use.

| Field | Meaning |
|---|---|
| `event_id` | Source-system event ID; safe reference for investigation |
| `event_type` | `identity.signin`, `identity.inbox_rule`, `network.dns`, `network.proxy`, `endpoint.config_change`, `user.report` |
| `result` | Provider outcome such as success, failure, blocked |
| `source_ip`, `asn` | Source network context; protect as sensitive data |
| `user_agent`, `device_id`, `device_trusted` | Client and endpoint context |
| `session_id` | Opaque provider correlation ID; do not use a cookie or bearer token |
| `token_bound` | Whether provider reports device/session binding |
| `interactive` | Interactive vs. background/non-interactive event |
| `risk` | Provider risk label, e.g. `anomalous_token`, `token_issuer_anomaly`, `token_replay` |
| `rule_action`, `rule_target` | Sanitized mailbox rule metadata; never include message body |

Never include passwords, OTPs, access/refresh tokens, cookies, authorization headers, raw request bodies, or private keys. Redact PII not needed for correlation. Production adapters should map vendor fields to this schema and preserve vendor event IDs, not secrets.

**Prototype limitation:** these rejection, allowlist, and redaction rules are policy requirements, not fully enforced by the current CLI. Use synthetic, already-redacted events only until validation and rejection are implemented and reviewed.
