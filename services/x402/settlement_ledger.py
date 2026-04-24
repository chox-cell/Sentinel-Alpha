import json
import os
from datetime import datetime, timezone
from pathlib import Path


SETTLEMENT_LOG_PATH = Path("logs/x402_settlements.jsonl")


def write_settlement_record(record: dict) -> dict:
    payload = dict(record or {})
    if not payload.get("created_at"):
        payload["created_at"] = datetime.now(timezone.utc).isoformat()
    SETTLEMENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SETTLEMENT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")
    return payload


def read_settlement_records(limit: int = 50) -> list[dict]:
    if limit <= 0 or not SETTLEMENT_LOG_PATH.exists():
        return []

    with SETTLEMENT_LOG_PATH.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    rows: list[dict] = []
    for line in reversed(lines):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
        if len(rows) >= limit:
            break
    return rows


def get_settlement_status() -> dict:
    network = (os.getenv("X402_NETWORK", "base") or "base").strip().lower() or "base"
    return {
        "settlement_log_path": str(SETTLEMENT_LOG_PATH),
        "count_estimate": len(read_settlement_records(limit=1000000)),
        "network": network,
    }
