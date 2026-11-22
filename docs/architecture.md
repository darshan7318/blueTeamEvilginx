# Agentic SOC architecture

## Principle

Use separately assigned agents for product, research, engineering, assurance, release, triage, and response planning. No human role is modeled in the workflow. Agents operate within delegated policy; deterministic gate and policy services decide whether work or actions may proceed and execute only explicitly authorized effects. No model receives authentication secrets or direct access to unrestricted identity-provider write APIs. Findings cite source event IDs and distinguish observed facts from hypotheses.

## Agents

1. **Ingestion/normalization worker** (non-LLM): validates schemas, timestamps, tenant boundaries, redaction, source provenance, and duplicate handling.
2. **Detection engine** (deterministic): runs versioned correlation rules, provider risk mappings, calibrated thresholds, and emits reason codes plus evidence references.
3. **Triage agent** (read-only LLM): groups related alerts, summarizes timelines, identifies missing telemetry, and produces a confidence-bounded hypothesis. It must not claim Evilginx attribution from generic signals.
4. **Threat-intel enrichment agent** (constrained retrieval): enriches domains/IPs/certificate metadata from approved sources; records source, observation time, confidence, and expiry. It cannot browse arbitrary internal URLs or execute samples.
5. **Investigation agents** (read-only, scoped): identity/session, endpoint/network, and mailbox/OAuth specialists each analyze only authorized evidence and return structured findings. A supervisor reconciles contradictions and missing evidence.
6. **Response planner** (policy-backed): proposes containment steps with impact, prerequisites, rollback, and evidence. It cannot execute.
7. **Autonomous authorization and response execution**: an independent authorization agent evaluates a specific proposed action under signed, versioned policy. A separate deterministic gateway validates identity, scope, expiry, idempotency, policy version, and rollback before issuing one short-lived capability to the executor. The gateway denies when policy or evidence is insufficient; agent text cannot create authorization.

## Orchestration contract

Input is a redacted case bundle with tenant/user pseudonym, event IDs, timestamps, normalized facts, and source labels. Agents return JSON: `observations`, `hypotheses`, `confidence`, `citations` (event IDs/source URLs), `unknowns`, and `recommended_next_steps`. Reject outputs that lack citations, contain secrets, request privilege expansion, or propose unsupported attribution. Tool calls are allowlisted and read-only. Do not expose one tenant's evidence to another.

## Policy-gated agent response ladder

- **Observe**: create a local case, preserve evidence references, and write an auditable local status record.
- **Verify**: correlate authorized identity/device/session evidence. The offline baseline does not contact users or third parties; an optional communications agent/integration requires its own role, policy, and review before activation.
- **Contain (explicit preauthorization required)**: propose scoped session revocation, temporary sign-in restriction, factor/grant review, or endpoint isolation only if signed policy explicitly allows it.
- **Eradicate/recover (explicit preauthorization required)**: propose narrowly scoped account recovery, phishing-resistant MFA enrollment, persistence removal, restore, and monitoring only through approved playbooks and gateway actions.
- **External actions (default deny)**: enterprise-wide blocking, partner/provider contact, or takedown requires a separate explicit policy capability; absent that, the autonomous workflow records a blocked recommendation.

Never allow an LLM score alone to block users, revoke sessions, change tenant policies, delete mailbox content, contact users, or submit takedown requests. Such effects are denied unless explicit signed policy permits the exact action and the independent agent and deterministic gateway checks pass.

## Evaluation

Measure precision/recall by scenario and tenant, alert latency, agent time-to-triage, false-positive rates for VPNs/travel/shared NAT, telemetry completeness, evidence citation rate, and harmful-action rate (target zero). Use synthetic events and provider-approved simulations that never collect real credentials/tokens. Red-team prompt injection in URLs, email bodies, and log fields; treat all telemetry as untrusted data, not instructions.
