import json
from datetime import datetime, timezone
from pathlib import Path

from services.outcome_memory.memory import get_recent_decisions
from services.outcome_memory.outcome_states import (
    BLOCKED_HIGH_RISK,
    EMERGENCY_RISK_CONFIRMED,
    MISSED_RISK_CANDIDATE,
    SAFE_SO_FAR,
    UNKNOWN,
)


VERIFIED_OUTCOMES_PATH = Path("logs/verified_outcomes.jsonl")


def verify_outcome(record: dict) -> dict:
    action = str(record.get("action") or "")
    score = int(record.get("score", 0) or 0)
    threat_class = str(record.get("threat_class") or "unknown")
    actual_outcome = classify_stub_outcome(record)

    if actual_outcome == BLOCKED_HIGH_RISK:
        verifier_confidence = 0.7
    elif actual_outcome == EMERGENCY_RISK_CONFIRMED:
        verifier_confidence = 0.75
    elif actual_outcome == SAFE_SO_FAR:
        verifier_confidence = 0.55
    elif actual_outcome == MISSED_RISK_CANDIDATE:
        verifier_confidence = 0.65
    else:
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


def classify_stub_outcome(record: dict) -> str:
    action = str(record.get("action") or "")
    score = int(record.get("score", 0) or 0)
    threat_class = str(record.get("threat_class") or "unknown")

    if action == "BLOCK" and score >= 85:
        return BLOCKED_HIGH_RISK
    if action == "EXIT_NOW":
        return EMERGENCY_RISK_CONFIRMED
    if action == "ALLOW" and threat_class == "normal":
        return SAFE_SO_FAR
    if action == "ALLOW" and threat_class != "normal":
        return MISSED_RISK_CANDIDATE
    return UNKNOWN


def verify_recent_outcomes(limit: int = 50) -> list:
    records = get_recent_decisions(limit=limit)
    verified = [verify_outcome(record) for record in records]

    if verified:
        VERIFIED_OUTCOMES_PATH.parent.mkdir(parents=True, exist_ok=True)
        with VERIFIED_OUTCOMES_PATH.open("a", encoding="utf-8") as f:
            for row in verified:
                f.write(json.dumps(row, ensure_ascii=True) + "\n")

    return verified
