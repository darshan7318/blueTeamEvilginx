# BlueTeamEvilginx product charter (G0 draft)

**Status:** Approved by PM-01 in this office session on 2026-11-23. This product decision does not pass G0 or imply that a persistent PM runtime is provisioned.

**Deployment target:** Self-contained, local-first, and simple to install on supported Windows, Linux, or macOS systems. A cloud account is not a product prerequisite.

## Product purpose

BlueTeamEvilginx is a defensive, evidence-first system for identifying and investigating adversary-in-the-middle phishing and session compromise, including Evilginx-like behavior. It focuses on observable behaviors and outcomes rather than fingerprints for one tool.

## Users and problem

Security operations and identity-security teams need to correlate sign-in, session, endpoint/network, DNS/proxy, and post-authentication audit signals. Individual indicators are noisy: a valid stolen session may look normal alone, and VPNs, travel, shared NAT, roaming, and brokered clients can resemble anomalies. Analysts need a traceable timeline, missing-telemetry reporting, confidence limits, and proportionate action options.

## Outcomes and measures

- Improve detection quality: measure precision and recall by scenario and tenant using labeled synthetic or approved simulation cases.
- Reduce time to understand an alert: measure alert-to-triage time and analyst effort against a baseline.
- Improve evidence quality: measure claims with valid source citations, telemetry completeness, and reproducibility.
- Preserve safe operation: target zero harmful or out-of-policy actions; measure denied-action correctness, tenant-isolation failures, and secret-redaction failures.
- Set numeric targets only after baseline data and representative evaluation sets are available; do not invent performance claims.

## Initial scope

- Normalize authorized identity, endpoint/network, DNS/proxy, and user-report telemetry.
- Correlate authentication, session-context changes, device/client context, risk signals, and post-authentication persistence events.
- Produce explainable findings with event citations, hypotheses, uncertainty, alternatives, and telemetry gaps.
- Use bounded agent roles for discovery, research, engineering, validation, assurance, release, triage, and response planning.
- Permit side effects only through preconfigured policy, independent agent decision, and deterministic authorization gateway.
- Keep deterministic detection, configuration, and local storage usable offline. LLM inference is an adapter: prefer a configured local backend for offline use; external model providers are optional, disabled by default, and require explicit configuration.
- Package the runtime so supported machines can install without provisioning a cloud control plane. The supported OS/package matrix and installation experience are acceptance criteria for later validation.

## Non-goals and prohibited capabilities

- Do not proxy login flows, collect credentials/MFA material, handle cookie/token values, or build phishing infrastructure.
- Do not provide offensive reproduction or evasion guidance.
- Do not claim exhaustive knowledge of Evilginx or all AiTM variants.
- Do not make unrestricted autonomous changes. Out-of-policy or ambiguous actions are denied.
- Do not use production telemetry to establish G0 readiness.
- Do not require Docker, Kubernetes, a cloud account, or outbound network access for the basic detection workflow.

## Assumptions and open items

- Provider schemas, token-protection coverage, event timing, and tenant-specific benign behavior must be validated during discovery.
- Data retention, residency, and regulatory constraints require an approved deployment context and cannot be inferred from this draft.
- The initial environment, runtime agent identities, tool allowlists, and policy service have not been verified in this workspace.

## G0 acceptance

PM-01 reviewed and approved this charter in the current office session. This approval records the product direction; it does not pass G0 or stand in for the independent AUD-16 gate review.

