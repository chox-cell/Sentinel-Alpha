import json
from datetime import datetime, timezone
from pathlib import Path


OUTCOME_MEMORY_PATH = Path("logs/outcome_memory.jsonl")

REQUIRED_FIELDS = {
    "trace_id",
    "contract_address",
    "chain",
    "score",
    "confidence",
    "action",
    "threat_class",
    "signals",
    "attestation",
    "created_at",
}


def record_decision(record: dict) -> dict:
    payload = dict(record or {})
    if not payload.get("created_at"):
        payload["created_at"] = datetime.now(timezone.utc).isoformat()

    missing = REQUIRED_FIELDS.difference(payload.keys())
    if missing:
        missing_sorted = ", ".join(sorted(missing))
        raise ValueError(f"Missing required outcome memory fields: {missing_sorted}")

    OUTCOME_MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTCOME_MEMORY_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")

    return payload


def get_recent_decisions(limit: int = 50) -> list:
    if limit <= 0:
        return []
    if not OUTCOME_MEMORY_PATH.exists():
        return []

    with OUTCOME_MEMORY_PATH.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    decisions = []
    for line in reversed(lines):
        try:
            decisions.append(json.loads(line))
        except json.JSONDecodeError:
            continue
        if len(decisions) >= limit:
            break

    return decisions
