# Per-agent system prompt index

Every agent invocation composes exactly three artifacts: one role prompt, [the shared safety contract](common-contract.md), and [the assignment packet](assignment-packet.md). Role prompts are independent files; do not merge them into a universal prompt.

## Roles

- [ARCH-03 — Solution Architect](roles/ARCH-03.md)
- [AUD-16 — Independent Assurance Agent](roles/AUD-16.md)
- [AUT-18 — Autonomous Authorization Analyst](roles/AUT-18.md)
- [DATA-06 — Data Governance & Privacy Analyst](roles/DATA-06.md)
- [DET-08 — Detection Engineering Analyst](roles/DET-08.md)
- [ENG-07 — Engineering Lead](roles/ENG-07.md)
- [EXEC-15 — Response Execution Agent](roles/EXEC-15.md)
- [PM-01 — Product Manager](roles/PM-01.md)
- [PO-02 — Product Owner / Backlog Steward](roles/PO-02.md)
- [QA-09 — Quality Engineering Analyst](roles/QA-09.md)
- [REL-17 — Release Manager](roles/REL-17.md)
- [RES-05 — Threat Research Analyst](roles/RES-05.md)
- [RESP-14 — Response Planner](roles/RESP-14.md)
- [SEC-04 — Product Security Architect](roles/SEC-04.md)
- [SPEC-12 — Investigation Specialist (instantiate per domain)](roles/SPEC-12.md)
- [SRE-10 — Platform & Reliability Engineer](roles/SRE-10.md)
- [TI-13 — Threat Intelligence Analyst](roles/TI-13.md)
- [TRI-11 — SOC Triage Coordinator](roles/TRI-11.md)

The G0 logical identity and proposed scope for each role are in [assignment-registry.json](../g0/assignment-registry.json). Runtime identities and tool grants remain inactive until the local orchestrator enforces the assignment.
