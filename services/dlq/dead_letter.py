import json
from datetime import datetime, timezone
from pathlib import Path


DLQ_PATH = Path("logs/dlq.jsonl")


def write_dlq(record: dict) -> dict:
    payload = dict(record or {})
    if not payload.get("created_at"):
        payload["created_at"] = datetime.now(timezone.utc).isoformat()

    DLQ_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DLQ_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")
    return payload


def read_dlq(limit: int = 50) -> list[dict]:
    if limit <= 0 or not DLQ_PATH.exists():
        return []

    with DLQ_PATH.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    rows = []
    for line in reversed(lines):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
        if len(rows) >= limit:
            break
    return rows
