# Agile SDLC office charter

## Operating decision

BlueTeamEvilginx uses an agent-run office: every product, engineering, research, assurance, release, triage, and response-planning function has a separately assigned agent and role prompt. No human is modeled as a workflow role. Agents may make delegated decisions only inside preconfigured policy. Deterministic services enforce access, stage gates, approval capabilities, execution scope, audit, and rollback; LLM text is never authorization by itself. If the evidence or policy is insufficient, the system denies or holds the work.

This is a design draft for a portable local-first product. Local Python environments and logical role assignments exist; the product runtime, tool enforcement, and stage-gate service have not been implemented or verified in this workspace. Therefore G0 is **not verified**, and implementation or later-stage execution is **blocked**. Current checks and the G0 backlog are recorded in [g0/readiness.md](g0/readiness.md); drafting these artifacts does not count as advancing the product lifecycle.

## Agent assignment model

The roster and responsibilities in `README.md` are the office directory. Each ID has an independent file under `prompts/roles/`; `prompts/role-prompts.md` is only an index. `prompts/common-contract.md` is the shared safety contract, and `prompts/assignment-packet.md` carries scoped task data. An agent instance receives exactly one role prompt plus the common contract and one assignment packet. It receives no general office-wide tool access.

Before an assignment activates, PO-02 must register: stable logical role ID, runtime identity when provisioned, prompt/skill version, stage, accountable owner, objective, inputs, exclusions, tools and data scope, environment, artifact path, acceptance criteria, dependencies, and escalation route. The deterministic assignment control rejects incomplete or mismatched packets. Agents cannot assign themselves, alter another agent's scope, or activate downstream work.

## Readiness gates

### G0 — Office and environment ready

G0 is the global prerequisite for all lifecycle work. It requires all of the following evidence:

- PM-01 has approved a bounded product charter, outcome measures, non-goals, and initial priority order.
- PO-02 has mapped every required role to a stable local logical identity, versioned role prompt/skill, and least-privilege tool profile (none by default). Runtime identity binding is recorded as a later activation prerequisite, not fabricated in this workspace.
- SRE-10 has provisioned and health-checked the portable local development and synthetic-test environments, documented local data/retention boundaries, and recorded optional future hardening. No production tenant telemetry or secrets are used to establish readiness. A cloud account/container engine is not required for the core workflow.
- ARCH-03, SEC-04, and DATA-06 have documented trust boundaries, threat baseline, data classification, prohibited inputs, retention, and failure modes.
- The assignment/stage-gate control is deny-by-default, versioned, and auditable. Agent tools and side-effect actions are disabled in the portable baseline. A separate deterministic action gateway is required before any future write/action capability can be enabled; AUT-18 cannot change that policy.
- AUD-16 has independently checked the evidence and the gate service has recorded G0 pass.

Until every item passes, all assignments remain `blocked`; no sprint, implementation, live-data verification, deployment, or response action starts. Current status for this draft: **G0 not verified (local agent runtime and gate enforcement are not implemented here).**

### Lifecycle sequence

After G0, work proceeds strictly in order through discovery/research, backlog/sprint planning, architecture/environment readiness, implementation, verification, release readiness, controlled deployment, and operate/improve, using the owners, deliverables, and gates in `README.md`. A failed gate stops the current stage. Only the gate service can activate the next stage after AUD-16's independent evidence review. Later-stage templates can be drafted but may not be represented as started, verified, or approved.

## Agent-only decisions and side effects

- PM-01 prioritizes work but cannot waive gates or authorize its own release/action.
- AUD-16 reviews evidence independently and returns pass/fail; it cannot change policy or activate a stage.
- AUT-18 independently evaluates an exact proposed release or response action against a signed, versioned policy. Its decision is advisory input to a deterministic gateway, not an authorization token.
- EXEC-15 performs only a single exact action after the gateway verifies role identity, tenant, target, policy version, expiry, idempotency, and signed delegated authorization. It cannot chain or widen actions.
- The gateway denies actions outside explicit preauthorization, with stale/contradictory evidence, missing rollback, failed health checks, or ambiguous scope. There is no informal human override path in this agent-run model; unsafe actions remain blocked.

This model supports autonomous bounded operations, not unrestricted agent autonomy. Prohibited capabilities remain prohibited: collection or handling of credentials/session secrets; phishing or relay construction; arbitrary browsing/sample execution; cross-tenant access; policy mutation by an LLM; and unsupervised actions outside explicit machine-enforced authorization.

