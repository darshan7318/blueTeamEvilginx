# G0 readiness record

**Status: BLOCKED — G0 remains active.** The read-only [gate report](gate_report.py) reports 3 of 8 criteria evidenced and 5 pending. This record tracks work completed in the current workspace on 2026-11-23. No later SDLC stage is active.

| G0 requirement | Status | Evidence / blocker | Next owner |
|---|---|---|---|
| Product charter, outcomes, non-goals | Approved by PM-01 in this office session | [Product charter](product-charter.md) and [decision log](decisions.md) record the self-contained, local-first, offline-capable direction. This is not a gate pass. | PM-01 |
| Roles mapped to separate prompts and scopes | Logical assignment complete; runtime enforcement pending | [Assignment registry](assignment-registry.json) maps all 18 roles to separate files under `prompts/roles/`, stable logical IDs, and proposed tool scopes. [Prompt preview](prompt_preview.py) validates the registry and packages one role with tools disabled; runtime identities and enforcement remain unprovisioned. | PO-02 |
| Prompt/skill integrity | Snapshot verified; history blocked | [Prompt manifest](prompt-manifest.json) records SHA-256 digests for 35 role prompt, skill, assignment, gate, and G0 policy artifacts. Manifest verification passed. Git history remains unavailable because repo initialization triggers this sandbox's ownership check. | PO-02, SRE-10 |
| Portable development and synthetic-test environment | Python environments provisioned | `.venv/` and `.venv-test/` use uv-managed CPython 3.12.13. `.python-version` and `uv.lock` are present; `uv lock --check --offline` passed. Only Python/package readiness was verified; no app tests were run. | SRE-10, QA-09 |
| Self-contained deployment requirements | Defined; packaging pending | [Environment plan](environment-plan.md) and [portable deployment profile](portable-deployment-profile.md) specify offline deterministic mode, optional inference adapters, and no cloud/container prerequisite. No installer or runtime package exists yet. | SRE-10, ENG-07 |
| Local data boundaries, redaction, retention, audit | Defaults proposed; review and runtime enforcement pending | [Data-handling defaults](data-handling-defaults.md) and its [machine-readable profile](data-handling-defaults.json) define offline, minimal-retention behavior. DATA-06/SEC-04 review and runtime enforcement remain pending. | DATA-06, SEC-04 |
| Existing prototype alignment | Blocked | The deterministic engine currently emits the raw `user` value and a `response_requires_human_approval` field. This conflicts with the approved pseudonymous, agent-run policy; update only after G0 authorizes the implementation stage. Use synthetic data only. | ENG-07, DATA-06 |
| Assignment/stage-gate enforcement | Policy defined; report-only utility exists; enforcement blocked | [gate-policy.json](gate-policy.json) defines fail-closed criteria. [gate_report.py](gate_report.py) verified its artifact manifest and reported 3/8 criteria evidenced; it cannot activate/deny an external assignment service or sign approvals. | PO-02, ARCH-03 |
| Action safety | Read-only baseline specified; gateway deferred | Portable baseline disables tools and side effects. Any future write/action capability remains blocked until a separate deterministic gateway is implemented and reviewed. | SEC-04, ARCH-03 |
| Independent G0 assurance | Blocked | AUD-16 has a role prompt but no active runtime assignment; no independent gate result is recorded. | AUD-16 |

## Deployment decision

The user clarified that the product should be self-contained/easy to deploy and that no cloud account is available. PM-01 accepted the local-first decision in [decisions.md](decisions.md). A cloud runner is not a prerequisite for the core product. Container support is optional hardening, not a blocker for offline detection.

## G0 exit rule

G0 stays blocked until role assignments are enforceable by the local runtime, the portable dev/synthetic-test setup is health-checked, DATA-06/SEC-04 review the data-handling defaults, stage advancement is controlled deterministically, and AUD-16 independently verifies the evidence. The current prototype remains synthetic-data-only; side-effect capabilities remain disabled. Do not enter discovery, implementation, deployment, or response stages before the gate records a pass.

## Gate scope correction

The [gate policy](gate-policy.json) now keeps G0 focused on office setup, local role/environment readiness, data-policy review, and independent gate controls. Implementing and validating data controls is a downstream verification criterion (Stage 5); portable installer and OS-matrix validation is a release-readiness criterion (Stage 6). Neither is counted as G0 evidence.

## Environment investigation notes

- `uv 0.11.3` found CPython 3.12.13; `.venv/` and `.venv-test/` were created and their interpreter versions verified.
- `.python-version` and `uv.lock` were added; `uv lock --check --offline` completed. The SHA-256 manifest check passed for its six listed artifacts.
- No tests or dependency installs were run.
- Docker, Podman, and Windows Sandbox are unavailable. WSL reports WSL 1 unsupported by the current machine configuration; these are not prerequisites for the agreed portable baseline.
- Git CLI exists, but the workspace is not a repository. A temporary initialization hit the sandbox ownership check; its empty metadata and the exact global safe-directory entry were reverted to restore normal tool access.

