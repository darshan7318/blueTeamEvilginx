---
name: plan-agent-authorized-response
description: Draft evidence-based response options for independent agent authorization under a deterministic policy gateway in an AiTM investigation.
---

# Plan a policy-gated agent response

Use only when response planning is assigned and an approved, versioned playbook and policy are supplied. This skill drafts recommendations; it never executes or authorizes them.

## Procedure

1. Confirm the incident hypothesis, evidence citations, confidence, blast radius, affected identities/assets, and unresolved questions.
2. Match the situation to the approved response ladder: preserve and observe; verify through trusted channels; propose targeted containment; review persistence and recovery; consider external action only under its separate approval path.
3. For each proposed action, provide rationale and citations, exact scope, impact, prerequisites, accountable agent, required AUT-18 decision, validation, rollback/recovery, expiry, and residual risk.
4. Prefer narrow, reversible steps. Do not propose broad tenant policy changes or destructive mailbox operations without explicit playbook support and separate approval.
5. Submit the proposal to AUD-16 for safety review and AUT-18 for an independent policy decision. EXEC-15 may execute only after the deterministic gateway validates policy and issues a one-action, short-lived authorization.

No free-form autonomous action. High-impact actions are denied unless narrowly preauthorized by signed policy, independently evaluated by AUT-18, and constrained by the gateway. Ambiguous scope, stale evidence, missing rollback, or policy mismatch means deny/hold.


