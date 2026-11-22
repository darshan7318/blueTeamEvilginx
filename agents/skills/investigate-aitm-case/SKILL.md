---
name: investigate-aitm-case
description: Coordinate an evidence-first, read-only investigation of suspected AiTM phishing, authentication relay, session replay, or post-authentication abuse.
---

# Investigate an AiTM case

Use for a scoped SOC case involving suspected AiTM or session compromise. This skill is for defensive analysis; it does not create or simulate phishing infrastructure.

## Procedure

1. Verify the case has tenant authorization, pseudonymous subject IDs, a bounded time window, source provenance, and redacted normalized events. Stop on secrets or cross-tenant material and report a redaction defect.
2. Ask the telemetry quality analyst to assess event completeness, schema, time alignment, duplicates, and ingestion delay.
3. Delegate only relevant domains: delivery, identity, session, endpoint/network, mailbox/OAuth/persistence, and constrained threat intelligence. Each analyst must cite stable event IDs.
4. Build one chronology. Preserve contradictions; do not count repeated copies of one source as independent corroboration.
5. Describe the strongest supported behavioral hypothesis, confidence and rationale, benign alternatives, ATT&CK mapping where evidence warrants, and unknowns.
6. If a detection gap is relevant, request a defensive, synthetic test proposal. If response planning is requested, ask the response planner for options under the supplied playbook and route the result to independent safety review.
7. Return the common JSON contract. Keep any side effect with EXEC-15 behind AUT-18 and the deterministic policy gateway.

## Completion checks

- Every material claim cites source event IDs or approved source IDs.
- Facts and hypotheses are separate; product attribution is not inferred from generic behaviors.
- Token/cookie/credential values are absent; correlation uses opaque identifiers only.
- Read-only scope and tenant boundary are preserved.
- Telemetry gaps, competing explanations, confidence limits, and agent authorization requirements are explicit.

