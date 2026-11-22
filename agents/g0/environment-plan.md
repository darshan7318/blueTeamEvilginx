# G0 local-first environment plan

## Deployment decision

The product is self-contained and portable by default. It does not require a cloud account, container engine, or network connection for deterministic detection. Local inference is optional; external model APIs are opt-in and receive only redacted evidence. Side-effect tools stay disabled in the portable baseline.

## Local project environments created

- `.venv/`: local development Python virtual environment.
- `.venv-test/`: separate Python virtual environment reserved for synthetic validation.
- `.python-version` pins Python 3.12; `uv.lock` records the resolved project environment.
- Both environments use uv-managed CPython 3.12.13 and were verified. `uv lock --offline` and `uv lock --check --offline` completed.
- `.uv-cache/` is a local setup cache and is excluded by `.gitignore`. No dependency packages were installed, and no tests were run.
- No production tenant telemetry or secrets may be used in these environments.
- `agents/g0/prompt_preview.py --agent-id PM-01` is the pattern for verifying and assembling a role bundle; it is preview-only and does not activate an agent or call a model.

These virtual environments separate Python package sets. They do not isolate processes, network access, filesystems, or credentials. Since the first shippable workflow is offline and read-only with agent tools disabled, the portable baseline does not depend on a container runtime. Any later feature that executes tools or mutates accounts requires a separately reviewed OS-level sandbox and deterministic policy gateway before activation.

## Packaging target

- Keep the core on Python 3.11+ and avoid mandatory native/system services.
- Provide a simple bootstrap path using the pinned runtime and lockfile; later evaluate a standalone executable for users without Python.
- Keep local event/case data in user-selected local storage with restrictive OS permissions and explicit retention/export controls.
- Start with JSONL/SQLite-compatible local workflows. No external telemetry upload by default.
- Support an offline deterministic mode. Agent inference should report unavailable cleanly when no local or opt-in provider is configured.
- Declare the supported OS/version matrix only after Windows, Linux, and macOS installation/evaluation is verified.

## Current environment evidence

- Windows host has uv 0.11.3 and uv-managed CPython 3.12.13; `.venv` and `.venv-test` exist.
- Docker, Podman, Windows Sandbox, and cloud CLIs/connectors are unavailable. WSL reports WSL 1 unsupported by the current machine configuration.
- This does not block the cloud-free deterministic product direction. It does prevent enabling agent tool execution or claiming cross-platform packaging readiness.

## G0 remainder

1. Assign/instantiate the local role runtime with explicit prompts and no tools by default; bind each assignment to its role and prompt digest.
2. Define local redaction, data permissions, and retention defaults before any real telemetry is used.
3. Keep the stage gate deterministic. Do not activate a later stage until its required role assignments, environment checks, and independent review are evidenced.
4. Build and test packaging only after G0 assignment and setup artifacts are reviewed. Container-based hardening remains an optional future profile, not a prerequisite for the basic product.

