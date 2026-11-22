# Portable local deployment profile (G0)

**Decision:** Build BlueTeamEvilginx as a self-contained, local-first product. A cloud account and managed runner are not required. This is the deployment target; this document is not an implementation or a claim of cross-platform validation.

## Product runtime

- Ship deterministic event parsing/correlation and local case output as the core path. The basic workflow must run offline.
- Keep event storage local and tenant-scoped. Use redacted, synthetic data for setup and evaluation; never collect credential or session-secret values.
- Load each agent as a separately assigned role prompt plus the shared safety contract and a bounded assignment packet. The assignment manifest pins prompt/skill digests and allowed tools.
- Keep LLM inference behind an adapter. Offline mode uses a locally configured compatible inference service; external model providers are optional, disabled unless explicitly configured, and receive only redacted, minimal case evidence.
- Default all agent tool access to none/read-only. Do not enable side-effect actions in the portable baseline. Future local actions require a deterministic policy gateway and separate execution control.
- Avoid mandatory Docker, Kubernetes, cloud services, telemetry uploads, and outbound calls for the core workflow. Container support may be an optional hardening profile where available.

## Distribution target

- Provide one documented installation path for supported operating systems, plus a reproducible source/developer path.
- Pin the runtime and dependencies; verify package signatures/hashes before install; include offline install instructions where feasible.
- Keep configuration local, validate it before launch, and never place secrets in prompts, logs, examples, or tracked files.
- Store local case data with restrictive OS permissions and configurable retention. Make export explicit and redacted.
- State the supported OS/version matrix and hardware requirements. Do not claim "any machine" until installation and evaluation pass on that matrix.

## G0 checks

1. Install the core package in the local dev and synthetic-test environments without a cloud account or mandatory network access.
2. Run the deterministic core on synthetic JSONL and verify the output cites source event IDs. (Do this only after the current project stage authorizes implementation/testing.)
3. Verify the app starts with no model backend configured and reports agent features unavailable rather than failing open.
4. Verify external model, tool, network, and response actions are disabled by default.
5. Verify prompt/skill digest validation, local data permissions, redaction behavior, and clean uninstall/data-retention behavior.

## Current limitations

The local Python 3.12.13 virtual environments are ready, and `agents/g0/prompt_preview.py` can assemble a manifest-checked role bundle in dry-run form. No model runtime, local inference backend, packaged installer, assignment-enforcement service, or local policy gateway exists yet. The current machine also lacks Docker/Podman/Windows Sandbox and has unsupported WSL configuration. These do not block the cloud-free product direction; they do block any claim that active agent execution is isolated and ready. No tests or application implementation were started in G0.

