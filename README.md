# BlueTeamEvilginx — Defensive AiTM Detection Prototype

BlueTeamEvilginx is a defensive, evidence-first system for detecting and responding to adversary-in-the-middle (AiTM) phishing and session-token replay. This repository starts with a local event correlator and an agentic SOC design. It does not proxy login flows, collect credentials/cookies, or generate phishing infrastructure.

The deployment target is self-contained and local-first: deterministic detection works offline and requires no cloud account. Agent inference is optional and provider-pluggable; tools and side-effect actions stay disabled in the portable baseline.

## Current scope

- Normalize identity, endpoint/network, DNS, proxy, and user-report events into a common schema.
- Correlate successful authentication with later token/session anomalies, unfamiliar client/device/network context, unbound sessions, and suspicious inbox changes.
- Produce explainable findings with evidence, confidence, ATT&CK mappings, and policy-bounded next steps.
- Keep containment actions policy-authorized and auditable. Agent decisions cannot bypass the deterministic policy gateway; out-of-policy actions are denied.

## Quick start

Requires Python 3.11+.

```powershell
python -m blueteam_evilginx --input examples/events.jsonl --output findings.json
```

Input is one JSON event per line. See `examples/events.jsonl` for synthetic data and `docs/event-schema.md` for fields. Findings are JSON with matched rules and evidence references.

## Architecture

See [docs/architecture.md](docs/architecture.md), [docs/threat-model.md](docs/threat-model.md), and [docs/roadmap.md](docs/roadmap.md). The first implementation is deterministic so analysts can inspect why an alert fired; LLM agents are planned as constrained investigation assistants over the same evidence and cannot execute response actions.

The office-style multi-agent SDLC, assignments, role prompts, and skills are in [agents/README.md](agents/README.md) and [agents/office-charter.md](agents/office-charter.md). They are specifications only; runtime agents and environment readiness are not evidenced in this workspace. G0 is not verified, so implementation and later lifecycle stages remain blocked.

## Safety and data handling

Treat raw authentication telemetry as sensitive. Never ingest passwords, MFA codes, bearer tokens, refresh tokens, or cookie values. Store only hashes or provider event IDs when correlation requires an identifier. Apply tenant isolation, retention limits, access controls, and redaction before sending any evidence to an LLM.
