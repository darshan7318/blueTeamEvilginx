# G0 decision log

## DEC-0001 — Local-first portable deployment

- **Date:** 2026-11-23
- **Raised by:** Product CEO (user direction)
- **Decision owner:** PM-01 (current Codex office agent)
- **Decision:** Make the core product self-contained and easy to deploy on supported machines. No cloud account is required for basic detection. The user has no cloud account to provision. Deterministic detection works offline; agent inference is an adapter, with local inference preferred for offline use and external providers opt-in. Agent tools and side effects remain disabled by default until deterministic local authorization controls are implemented and verified.
- **Impact:** The managed cloud runner is no longer a G0 prerequisite for the portable baseline. Container isolation remains an optional hardening profile. G0 still requires prompt/role assignment, local data and redaction defaults, reproducible packaging, stage-gate controls, and independent assurance before advancing.
- **Status:** Accepted by PM-01; implementation and cross-platform validation are later-stage work.

