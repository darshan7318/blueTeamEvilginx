"""Explainable, deterministic detections for normalized identity events."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any


def _time(event: dict[str, Any]) -> datetime:
    value = str(event.get("timestamp", ""))
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(value)
        return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def correlate(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return findings; raw secret-bearing fields are never copied into output."""
    by_user: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        if event.get("user"):
            by_user[str(event["user"])].append(event)
    findings: list[dict[str, Any]] = []
    for user, rows in by_user.items():
        rows.sort(key=_time)
        successes = [e for e in rows if e.get("event_type") == "identity.signin" and e.get("result") == "success"]
        for current in successes:
            evidence: list[str] = []
            score = 0
            prior = [e for e in successes if _time(e) < _time(current)]
            prev = prior[-1] if prior else None
            if current.get("risk") in {"anomalous_token", "token_issuer_anomaly", "token_replay"}:
                score += 50
                evidence.append(f"Identity provider marked event {current.get('event_id', 'unknown')} as {current['risk']}")
            if current.get("token_bound") is False and current.get("interactive") is False:
                score += 20
                evidence.append("Successful non-interactive sign-in used an unbound session")
            if prev and current.get("session_id") and current.get("session_id") == prev.get("session_id"):
                changed = any(current.get(k) and prev.get(k) and current.get(k) != prev.get(k) for k in ("source_ip", "asn", "device_id"))
                if changed:
                    score += 35
                    evidence.append("Same session identifier appeared with a changed network or device context")
            if current.get("device_trusted") is False:
                score += 10
                evidence.append("Sign-in came from a device not marked trusted")
            if not evidence or score < 35:
                continue
            nearby = [e for e in rows if abs((_time(e) - _time(current)).total_seconds()) <= 3600]
            inbox = [e for e in nearby if e.get("event_type") == "identity.inbox_rule" and e.get("rule_action") in {"delete", "forward", "redirect"}]
            if inbox:
                score += 20
                evidence.append("Suspicious inbox rule activity followed or preceded the sign-in within one hour")
            findings.append({
                "finding_id": f"aitm-{current.get('event_id', len(findings) + 1)}",
                "user": user,
                "severity": "critical" if score >= 80 else "high" if score >= 55 else "medium",
                "score": min(score, 100),
                "event_ids": [e.get("event_id") for e in [current, *inbox] if e.get("event_id")],
                "evidence": evidence,
                "attack_mapping": ["T1557", "T1539", "T1550.004"],
                "recommended_actions": [
                    "Verify the activity with the user through a trusted channel.",
                    "Review identity-provider risk, device compliance, session binding, and adjacent mailbox or data-access events.",
                    "If confirmed compromised, an authorized identity administrator should revoke sessions, reset credentials, and review MFA methods.",
                    "Preserve provider event IDs and relevant DNS, proxy, and endpoint telemetry for investigation."
                ],
                "response_requires_human_approval": True,
            })
    return sorted(findings, key=lambda f: (-f["score"], f["finding_id"]))
