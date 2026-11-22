---
name: review-detection-coverage
description: Assess defensive detection coverage for AiTM and session compromise using rule metadata and synthetic or de-identified evidence.
---

# Review detection coverage

Use when reviewing the defensive control plane, correlation rules, or evaluation cases for AiTM-related behaviors.

## Procedure

1. Define the behavior and outcome to detect (delivery, authentication anomaly, session replay, post-authentication persistence); do not depend on an Evilginx product fingerprint.
2. List required source fields, provider/schema versions, event latency, and known blind spots. Identify controls that prevent or limit impact, including phishing-resistant authentication and session binding where applicable.
3. Map each detection claim to evidence fields and existing deterministic rule IDs. Describe the event sequence and correlation window in terms of defensive observables only.
4. Identify benign cohorts and test them: VPN/travel, mobile networks, shared NAT, brokered clients, shared devices, proxies, and provider retries.
5. Propose synthetic or approved provider-simulation cases that never collect credentials, MFA material, cookies, or tokens. State expected alerts, non-alerts, reason codes, and measurable precision/recall criteria.
6. Mark all untested hypotheses as proposals. Return gaps, telemetry dependencies, and a prioritized defensive backlog.

Never produce relay implementation details, phishing lure templates, domain or hosting recipes, token extraction instructions, or evasion guidance.

