"""Build a verified, read-only prompt bundle for one logical agent role.

This G0 utility is preview-only. It never invokes a model, activates an
assignment, loads case data, or enables tools/side effects.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
G0 = ROOT / "agents" / "g0"


class PreviewError(Exception):
    """Raised when the role bundle is incomplete or fails integrity checks."""


def resolve_in_workspace(path_value: str, base: Path) -> Path:
    candidate = (base / path_value).resolve(strict=True)
    try:
        candidate.relative_to(ROOT)
    except ValueError as exc:
        raise PreviewError("Configured artifact path escapes the workspace.") from exc
    if not candidate.is_file():
        raise PreviewError("Configured artifact is not a file.")
    return candidate


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreviewError(f"Could not read JSON artifact: {path.name}") from exc
    if not isinstance(value, dict):
        raise PreviewError(f"Expected a JSON object in {path.name}.")
    return value


def verify_manifest(manifest: dict[str, Any]) -> set[str]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise PreviewError("Prompt integrity manifest has no artifacts.")

    found: dict[str, str] = {}
    for item in artifacts:
        if not isinstance(item, dict):
            raise PreviewError("Prompt integrity manifest entry is malformed.")
        artifact_path = item.get("path")
        expected = item.get("sha256")
        if not isinstance(artifact_path, str) or not isinstance(expected, str):
            raise PreviewError("Prompt integrity manifest entry lacks path or digest.")
        path = resolve_in_workspace(artifact_path, ROOT)
        actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        if actual != expected.upper():
            raise PreviewError(f"Prompt integrity check failed: {artifact_path}")
        found[artifact_path.replace("\\", "/")] = actual

    required = {
        "agents/prompts/common-contract.md",
        "agents/prompts/assignment-packet.md",
        "agents/g0/assignment-registry.json",
        "agents/g0/gate-state.json",
        "agents/g0/gate-policy.json",
        "agents/g0/gate_report.py",
    }
    if not required.issubset(found):
        raise PreviewError("Manifest does not cover the registry and shared prompt artifacts.")
    return set(found)


def build_preview(agent_id: str) -> dict[str, Any]:
    registry = read_json(G0 / "assignment-registry.json")
    gate = read_json(G0 / "gate-state.json")

    if registry.get("status") != "draft_only":
        raise PreviewError("Only the G0 draft registry can be previewed by this utility.")
    if gate.get("current_gate") != "G0" or gate.get("gate_status") != "blocked":
        raise PreviewError("Prompt preview is restricted to the recorded blocked G0 state.")
    if gate.get("next_stage_enabled") is not False:
        raise PreviewError("Gate state unexpectedly enables a downstream stage.")
    if gate.get("assignment_activation_allowed") is not False:
        raise PreviewError("Gate state unexpectedly allows assignment activation.")
    if gate.get("agent_tools_enabled") is not False or gate.get("side_effect_actions_enabled") is not False:
        raise PreviewError("Gate state unexpectedly enables tools or side effects.")

    roles = registry.get("roles")
    if not isinstance(roles, list):
        raise PreviewError("Role registry is malformed.")
    matches = [role for role in roles if isinstance(role, dict) and role.get("id") == agent_id]
    if len(matches) != 1:
        raise PreviewError("Unknown or duplicate logical agent ID.")
    role = matches[0]
    if role.get("assignment_status") != "logical_only" or role.get("runtime_identity") != "not_provisioned":
        raise PreviewError("Role is not in the expected inactive G0 state.")
    if role.get("tools") != []:
        raise PreviewError("The portable G0 baseline permits no agent tools.")

    registry_path = G0 / "assignment-registry.json"
    manifest_path = resolve_in_workspace(registry["prompt_manifest"], G0)
    manifest = read_json(manifest_path)
    verified_paths = verify_manifest(manifest)
    if "agents/g0/prompt_preview.py" not in verified_paths:
        raise PreviewError("Manifest does not cover the prompt preview utility.")

    common_path = resolve_in_workspace(registry["common_prompt"], G0)
    packet_path = resolve_in_workspace(registry["assignment_packet"], G0)
    role_path = resolve_in_workspace(role["role_prompt"], G0)
    role_relpath = role_path.relative_to(ROOT).as_posix()
    if (
        role_relpath not in verified_paths
        or registry_path.relative_to(ROOT).as_posix() not in verified_paths
        or (G0 / "gate-state.json").relative_to(ROOT).as_posix() not in verified_paths
    ):
        raise PreviewError("Registry, role prompt, or gate state is not covered by the integrity manifest.")

    bundle = "\n\n".join(
        (
            "# SHARED SAFETY CONTRACT\n" + common_path.read_text(encoding="utf-8"),
            "# ROLE SYSTEM PROMPT\n" + role_path.read_text(encoding="utf-8"),
            "# ASSIGNMENT PACKET TEMPLATE\n" + packet_path.read_text(encoding="utf-8"),
        )
    )
    return {
        "preview_only": True,
        "activates_assignment": False,
        "model_invoked": False,
        "agent_id": role["id"],
        "logical_identity": role["logical_identity"],
        "role": role["role"],
        "stage": "G0",
        "gate_status": "blocked",
        "authorized_tools": [],
        "side_effect_actions_enabled": False,
        "prompt_snapshot": manifest.get("snapshot_id"),
        "prompt_bundle": bundle,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preview one integrity-checked role prompt bundle; never activates or invokes it."
    )
    parser.add_argument("--agent-id", required=True, help="Logical role ID, for example PM-01")
    args = parser.parse_args()
    try:
        result = build_preview(args.agent_id)
    except (KeyError, PreviewError) as exc:
        print(json.dumps({"preview_only": True, "status": "blocked", "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

