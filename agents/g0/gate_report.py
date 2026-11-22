"""Read-only G0 gate status reporter. It cannot approve or advance stages."""

from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
G0 = ROOT / "agents" / "g0"


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path.name}")
    return value


def verify_artifact_manifest() -> set[str]:
    manifest = read_object(G0 / "prompt-manifest.json")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("Artifact manifest is empty or malformed.")
    verified: set[str] = set()
    for item in artifacts:
        if not isinstance(item, dict):
            raise ValueError("Artifact manifest entry is malformed.")
        relative = item.get("path")
        expected = item.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise ValueError("Artifact manifest entry lacks a path or digest.")
        path = (ROOT / relative).resolve(strict=True)
        try:
            path.relative_to(ROOT)
        except ValueError as exc:
            raise ValueError("Artifact manifest path escapes the workspace.") from exc
        actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        if actual != expected.upper():
            raise ValueError(f"Artifact integrity check failed: {relative}")
        verified.add(path.relative_to(ROOT).as_posix())
    required = {
        "agents/g0/gate-policy.json",
        "agents/g0/gate-state.json",
        "agents/g0/assignment-registry.json",
        "agents/g0/gate_report.py",
    }
    if not required.issubset(verified):
        raise ValueError("Manifest does not cover the gate policy, state, registry, and reporter.")
    return verified


def create_report() -> dict[str, Any]:
    verify_artifact_manifest()
    state = read_object(G0 / "gate-state.json")
    policy = read_object(G0 / "gate-policy.json")
    if policy.get("default_decision") != "deny" or policy.get("automatic_transition") is not False:
        raise ValueError("Gate policy must fail closed and prohibit automatic transitions.")
    if policy.get("agent_tools_enabled_by_default") is not False or policy.get("side_effect_actions_enabled_by_default") is not False:
        raise ValueError("Gate policy must keep tools and side effects disabled by default.")
    criteria = policy.get("criteria")
    if not isinstance(criteria, list):
        raise ValueError("Gate policy criteria are malformed.")
    if state.get("current_stage") != 0 or state.get("current_gate") != "G0":
        raise ValueError("G0 reporter refuses an unexpected stage/gate state.")
    if state.get("gate_status") != "blocked":
        raise ValueError("Read-only G0 reporter expects the gate to remain blocked.")
    if state.get("next_stage_enabled") is not False or state.get("assignment_activation_allowed") is not False:
        raise ValueError("Gate state enables work while G0 is blocked.")
    if state.get("agent_tools_enabled") is not False or state.get("side_effect_actions_enabled") is not False:
        raise ValueError("Gate state enables tools or side effects while G0 is blocked.")

    blockers: list[dict[str, str]] = []
    for criterion in criteria:
        if not isinstance(criterion, dict):
            raise ValueError("Gate policy contains a malformed criterion.")
        status = criterion.get("status")
        if status not in {"verified", "pending"}:
            raise ValueError(f"Invalid status for criterion {criterion.get('id', 'unknown')}.")
        evidence = criterion.get("evidence", [])
        if not isinstance(evidence, list):
            raise ValueError(f"Evidence list is malformed for {criterion.get('id', 'unknown')}.")
        if status == "verified" and not evidence:
            raise ValueError(f"Verified criterion lacks evidence: {criterion.get('id', 'unknown')}.")
        if status == "verified":
            for reference in evidence:
                if not isinstance(reference, str):
                    raise ValueError(f"Invalid evidence reference for {criterion.get('id', 'unknown')}.")
                evidence_path = (ROOT / reference.rstrip("/\\")).resolve(strict=False)
                try:
                    evidence_path.relative_to(ROOT)
                except ValueError as exc:
                    raise ValueError("Gate evidence path escapes the workspace.") from exc
                if not evidence_path.exists():
                    raise ValueError(f"Verified evidence is missing: {reference}")
        if status != "verified":
            blockers.append(
                {
                    "criterion": str(criterion.get("id", "unknown")),
                    "owner": str(criterion.get("owner", "unassigned")),
                    "status": status,
                }
            )

    audit_criteria = next(
        (item for item in criteria if item.get("id") == "independent_g0_assurance_attestation"),
        None,
    )
    if not audit_criteria or audit_criteria.get("status") != "verified":
        if not any(item["criterion"] == "independent_g0_assurance_attestation" for item in blockers):
            blockers.append(
                {
                    "criterion": "independent_g0_assurance_attestation",
                    "owner": "AUD-16",
                    "status": "pending",
                }
            )

    return {
        "policy_id": policy.get("policy_id"),
        "current_stage": 0,
        "current_gate": "G0",
        "gate_status": "blocked",
        "next_stage_enabled": False,
        "assignment_activation_allowed": False,
        "agent_tools_enabled": False,
        "side_effect_actions_enabled": False,
        "criteria_total": len(criteria),
        "criteria_verified": sum(1 for item in criteria if item.get("status") == "verified"),
        "blockers": blockers,
        "review_attestation_required": True,
        "report_only": True,
    }


def main() -> int:
    try:
        print(json.dumps(create_report(), ensure_ascii=False, indent=2))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"gate_status": "blocked", "report_only": True, "error": str(exc)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

