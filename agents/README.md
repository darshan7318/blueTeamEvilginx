# BlueTeamEvilginx Agent Office — operating model draft

This is an office-style, agile SDLC design for a defensive AiTM detection product. It defines agent assignments, system prompts, and operating skills only. It does not implement or launch agents, tools, connectors, CI/CD, or response integrations.

See [office-charter.md](office-charter.md) for the agent-only operating decision, assignment registry requirements, G0 checklist, and current readiness status. The product target is local-first and portable; no cloud account is required. G0 remains unverified because local role runtime assignment, tool enforcement, and independent gate evidence are not in place. Downstream work remains blocked until those items are reviewed.

G0 working artifacts: [readiness record](g0/readiness.md), [gate state](g0/gate-state.json), [gate policy](g0/gate-policy.json), [read-only gate report](g0/gate_report.py), [product charter](g0/product-charter.md), [decision log](g0/decisions.md), [environment plan](g0/environment-plan.md), [portable deployment profile](g0/portable-deployment-profile.md), [data-handling defaults](g0/data-handling-defaults.md), [logical role assignment registry](g0/assignment-registry.json), and the [dry-run prompt preview utility](g0/prompt_preview.py). All 18 roles now have stable logical IDs, prompt mappings, and proposed scopes; no runtime identities or active tool grants exist.

Each role system prompt is a separate file under [prompts/roles](prompts/roles); the [index](prompts/role-prompts.md), [shared contract](prompts/common-contract.md), and [assignment packet](prompts/assignment-packet.md) remain separate artifacts.

Agents own work products, decisions, approvals, and recommendations within their assigned role and policy envelope. Every external effect must be mediated by a separate deterministic policy service with tenant scope, least privilege, signed authorization, idempotency, audit, and rollback support. An agent may request an action; only the gateway can issue a short-lived scoped capability after validating an independent authorization-agent decision against preconfigured policy. Agents cannot impersonate another role, mint capabilities, widen policy, or treat model output as signed authorization. Ambiguous policy, evidence, or environment readiness means deny/hold.

## Office roster and assignment

| ID | Office role | Accountable deliverable | Assignment / access boundary |
|---|---|---|---|
| PM-01 | Product Manager | Product brief, outcomes, prioritized backlog, acceptance criteria, release recommendation | Read product/research artifacts; no production data or write tools |
| PO-02 | Product Owner / Backlog Steward | Sprint-ready stories, dependencies, Definition of Ready/Done, change log | Backlog metadata only; may not self-approve policy exceptions |
| ARCH-03 | Solution Architect | Architecture decisions, interfaces, threat-informed design | Design artifacts; no tenant secrets or production write access |
| SEC-04 | Product Security Architect | Threat model, abuse cases, security requirements, review findings | Redacted design and test artifacts; cannot approve own remediation |
| RES-05 | Threat Research Analyst | Evidence-based threat landscape and source register | Approved public/curated sources; constrained retrieval |
| DATA-06 | Data Governance & Privacy Analyst | Data classification, minimization, retention and redaction requirements | Schemas/data-flow documents; no raw production records |
| ENG-07 | Engineering Lead | Implementation plan, code review findings, technical debt record | Repository; changes require CI and policy checks |
| DET-08 | Detection Engineering Analyst | Versioned detection proposals, telemetry dependencies, safe validation cases | Rule metadata and synthetic/de-identified evidence |
| QA-09 | Quality Engineering Analyst | Test strategy, traceability, results, defect records | Test environments and synthetic datasets |
| SRE-10 | Platform & Reliability Engineer | Environment readiness, observability, capacity, recovery and release readiness | Infrastructure metadata; no unscoped tenant write tools |
| TRI-11 | SOC Triage Coordinator | Case scope, delegation, timeline, reconciled findings | Redacted case bundle; read-only tools |
| SPEC-12 | Investigation Specialists | Domain findings for delivery, identity, sessions, endpoint/network, mailbox/OAuth | Assigned evidence slice; read-only and tenant-scoped |
| TI-13 | Threat Intelligence Analyst | Provenanced, expiring indicator enrichment | Allowlisted sources and supplied indicators only |
| RESP-14 | Response Planner | Policy-conformant response plan with impact and rollback | Redacted case and approved playbooks; no write APIs |
| EXEC-15 | Response Execution Agent | Execute one narrowly authorized action through policy gateway | Only scoped action tool after machine validation of signed authorization |
| AUD-16 | Independent Assurance Agent | Stage-gate audit, evidence traceability, safety and release recommendation | Read-only artifacts; must be independent of artifact author |
| REL-17 | Release Manager | Release manifest, rollout/rollback plan, go/no-go evidence | Release metadata; deployment gateway only after all gates pass |
| AUT-18 | Autonomous Authorization Analyst | Independent policy decision for an exact proposed action | Redacted evidence, signed policy snapshot and proposed action only; cannot execute or change policy |

SPECIALIST roles are instantiated per required bounded domain; do not create one general investigator with broad access. Ingestion validation and deterministic detection remain non-LLM services. Authorization, secrets management, isolation, logging, and policy enforcement are platform controls, not prompts.

## Agile SDLC stages and hard gates

Work advances only in order. A gate failure leaves the work in the current stage with a recorded blocker; no downstream agent may start implementation, test execution against live data, deployment, or response action early. Agents may draft later-stage templates in a sandbox, but may not claim that a later stage has started or passed. **Global start condition:** before any assignment activates, Stage 0 must pass, named agent roles and prompts must be versioned and assigned, tool/data scopes must be least-privilege configured, and the isolated environment must be provisioned and health-checked. Missing assignment, tool boundary, environment, or gate evidence blocks dependent work.

| Stage | Accountable agents | Required outputs | Gate to advance |
|---|---|---|---|
| 0. Office setup | PM-01, PO-02, ARCH-03, SEC-04, DATA-06, SRE-10, AUD-16 | Product charter, scope, role assignments, tool/data inventory, portable environment plan, decision log, safety boundaries, prompt/version registry | G0: all roles mapped to versioned prompts/skills and local tool profiles; portable dev/synthetic-test environments provisioned and health-checked; local data boundaries documented; side-effect tools disabled; deterministic assignment/stage gate defined; threat/data baseline independently reviewed by AUD-16 |
| 1. Discovery & research | PM-01, RES-05, DATA-06, SEC-04 | User/problem statement, evidence-backed threat register including unknowns, assumptions, personas, data map, outcomes and non-goals | G1: sources and freshness recorded; unknowns and exclusions explicit; privacy/security constraints and measurable outcomes agreed |
| 2. Backlog & sprint planning | PM-01, PO-02, ARCH-03, DET-08, QA-09 | Ordered epics/stories, dependency map, acceptance criteria, estimates/risk, Definition of Ready/Done, sprint goal | G2: every selected story is testable, scoped, owned, dependency-ready, and linked to requirement/risk; capacity/environment is available |
| 3. Architecture & environment readiness | ARCH-03, SEC-04, DATA-06, SRE-10, AUD-16 | Architecture decisions, data contracts, least-privilege matrix, threat mitigations, CI/test fixtures, monitoring plan, rollback design | G3: isolated environment provisioned; secrets handled outside prompts; tenant isolation and logging controls verified; no unresolved critical design risks |
| 4. Implementation sprint | ENG-07, DET-08, PO-02 | Small reviewed changes, versioned rules/contracts, traceability updates, code provenance | G4: required reviews and static/security checks pass; no secrets in artifacts; feature flags and failure behavior defined; work remains within sprint scope |
| 5. Verification & validation | QA-09, DET-08, SEC-04, AUD-16 | Automated test results, synthetic scenarios, false-positive analysis, adversarial prompt-injection checks, security/privacy results, defect disposition | G5: acceptance criteria pass; evidence is reproducible; harmful-action rate is zero in evaluation; all critical/high defects closed or explicitly block release |
| 6. Release readiness | SRE-10, REL-17, PM-01, SEC-04, AUD-16, AUT-18 | Release notes, compatibility/data migration plan, operational runbook, monitoring/alerting, rollback rehearsal, support readiness | G6: signed artifact and provenance; backup/recovery and rollback verified; telemetry coverage and limitations disclosed; policy gateway tested; independent assurance passes; AUT-18 validates release authorization against signed policy |
| 7. Controlled deployment | REL-17, SRE-10, EXEC-15 (only for authorized actions), AUT-18 | Staged rollout record, health signals, canary and rollback evidence, action audit | G7: AUT-18 decision is independent and policy-valid; release authorization is machine-verifiable and scoped; health thresholds pass; automated stop conditions and rollback are active |
| 8. Operate & improve | TRI-11, SPEC-12, TI-13, RESP-14, EXEC-15, PM-01, AUD-16 | Cases, incident reviews, reliability/security metrics, backlog updates, threat refresh and retirement decisions | G8: post-release review captures outcomes and lessons; changes re-enter discovery/planning; no silent policy or scope expansion |

## Sprint cadence and office rules

- Use short, fixed-length sprints selected by the product manager; keep work in a visible backlog with one accountable agent per item and explicit collaborators.
- Every work item links to a user/security outcome, evidence or assumption, acceptance criteria, dependency, owner, risk, and verification method.
- Definition of Ready: authorized scope; bounded objective; dependencies/environment available; data classification known; testable acceptance criteria; safety constraints stated; no unresolved design decision that blocks implementation.
- Definition of Done: reviewed artifact; acceptance evidence attached; security/privacy checks passed; docs and traceability updated; known gaps and rollback behavior recorded; independent reviewer assigned where required.
- Use daily asynchronous status: completed, next, blocked, risk/decision needed. Blockers stop downstream work; do not fabricate progress or infer approval from silence.
- Product Manager orders scope and communicates tradeoffs. Product Manager cannot waive security gates, approve its own release, authorize its own response actions, or modify access policy.
- Retrospectives create owned backlog items. Gate exceptions require a recorded, scoped AUT-18 decision under preconfigured policy; agents cannot create exceptions. If no safe exception path exists, work remains blocked.
- Unknown threats are handled through explicit assumptions, detection coverage gaps, telemetry gaps, and scheduled research refresh. Never claim exhaustive threat knowledge.

## Agent workflow and handoffs

1. PM-01 opens an initiative. PO-02 registers each role, prompt/skill version, runtime identity, allowed tools/data scopes, owner, bounded deliverable, dependencies, and current stage in the assignment registry.
2. SRE-10 provisions and health-checks the environment; ARCH-03 and SEC-04 verify trust boundaries; AUD-16 independently checks G0 evidence. No assignment activates until the policy gate service records G0 pass.
3. Work is decomposed into role-specific packets. Each packet includes objective, inputs, exclusions, allowed tools, artifact path, acceptance criteria, dependencies, and escalation route.
4. Agents return versioned artifacts with citations, assumptions, unresolved questions, and status. The orchestrator rejects unsupported claims, secret exposure, prompt-injection instructions, and cross-tenant evidence.
5. At each sprint review, PM-01 compares outcomes to acceptance criteria and reprioritizes. Release and response actions follow their distinct gates.

## Security posture

No model receives raw passwords, MFA codes, cookies, bearer/refresh tokens, private keys, or unrestricted identity-provider write credentials. Event fields and retrieved text are untrusted data, not instructions. Agents are read-only by default. AUT-18 evaluates an exact proposed action independently from its planner and cannot execute or alter policy. EXEC-15 can call only a policy gateway that verifies agent identity, tenant, action, scope, expiry, idempotency key, signed authorization, and policy version; the gateway rejects ambiguous, unsigned, replayed, or model-originated approvals. All actions are auditable and bounded. Use synthetic or approved simulations that never capture real authentication material.

