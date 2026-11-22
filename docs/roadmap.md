# Roadmap

## 0.1 — local detection core (current)
- JSONL schema, explainable correlation, synthetic example, threat model, agent safety architecture.

## 0.2 — ingestion and quality
- Provider adapters for Entra ID and Google Workspace sign-in/audit logs; schema validation, tenant partitioning, event-time windows, deduplication, and redaction.
- DNS/proxy/EDR connectors and telemetry coverage dashboard. Read-only permissions by default.

## 0.3 — case management and investigation
- Correlation graph and timeline UI; evidence citations; analyst feedback and rule tuning; approved threat-intel enrichment with TTL and provenance.
- LLM triage with structured output, prompt-injection isolation, tenant-scoped retrieval, and quality evaluation.

## 0.4 — controlled response
- Independent agent authorization and a deterministic policy gateway for narrowly scoped identity-provider actions, dry-run, idempotency, rollback and audit log. Side effects stay disabled until the gateway is implemented and verified.
- Provider-specific playbooks for session revocation, factor/app-grant review, and account recovery.

## 1.0 — production readiness
- Multi-tenant security review, threat modeling, data retention, encryption, RBAC, SSO, audit, HA, disaster recovery, signed rule packs, versioned migrations, independent penetration test, and measured detection validation.

## Exit criteria

No production claim until connectors are validated against current vendor schemas, representative tenants have measured telemetry coverage, detections are calibrated on labeled benign/malicious data, actions are authorization-tested, and data governance/security reviews are complete.
