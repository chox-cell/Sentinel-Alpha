import json
from datetime import datetime, timezone
from pathlib import Path

from services.outcome_memory.memory import get_recent_decisions


VERIFIED_OUTCOMES_PATH = Path("logs/verified_outcomes.jsonl")


def verify_outcome(record: dict) -> dict:
    action = str(record.get("action") or "")
    score = int(record.get("score", 0) or 0)
    threat_class = str(record.get("threat_class") or "unknown")

    if action == "BLOCK" and score >= 85:
        actual_outcome = "blocked_high_risk"
        verifier_confidence = 0.7
    elif action == "EXIT_NOW":
        actual_outcome = "emergency_risk_confirmed"
        verifier_confidence = 0.75
    elif action == "ALLOW" and threat_class == "normal":
        actual_outcome = "safe_so_far"
        verifier_confidence = 0.55
    elif action == "ALLOW" and threat_class != "normal":
        actual_outcome = "missed_risk_candidate"
        verifier_confidence = 0.65
    else:
        actual_outcome = "unknown"
        verifier_confidence = 0.4

    return {
        "original_trace_id": record.get("trace_id"),
        "contract_address": record.get("contract_address"),
        "chain": record.get("chain"),
        "predicted_score": score,
        "predicted_action": action,
        "threat_class": threat_class,
        "signals": record.get("signals", {}),
        "actual_outcome": actual_outcome,
        "verifier_confidence": verifier_confidence,
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }


def verify_recent_outcomes(limit: int = 50) -> list:
    records = get_recent_decisions(limit=limit)
    verified = [verify_outcome(record) for record in records]

    if verified:
        VERIFIED_OUTCOMES_PATH.parent.mkdir(parents=True, exist_ok=True)
        with VERIFIED_OUTCOMES_PATH.open("a", encoding="utf-8") as f:
            for row in verified:
                f.write(json.dumps(row, ensure_ascii=True) + "\n")

    return verified
