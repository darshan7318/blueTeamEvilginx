# Agent assignment packet

Each invocation receives exactly one role prompt from `roles/`, the shared contract from `common-contract.md`, and this bounded packet. All fields must be explicit. Reject incomplete packets; do not infer missing authority or scope.

```json
{
  "assignment_id": "...",
  "agent_id": "...",
  "stage": "...",
  "stage_gate_status": "...",
  "objective": "...",
  "inputs": [],
  "excluded_inputs": [],
  "authorized_tools": [],
  "artifact_path": "...",
  "acceptance_criteria": [],
  "dependencies": [],
  "owner": "...",
  "escalation_route": "..."
}
```

If the current gate has not passed, set status to `blocked` and do not begin dependent work. The packet grants no permissions by itself; runtime policy must independently enforce tool and data scopes. The portable baseline assigns no tools and no side-effect actions.