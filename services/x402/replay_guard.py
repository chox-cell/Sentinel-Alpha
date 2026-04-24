import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


PAYMENTS_LOG_PATH = Path("logs/x402_payments.jsonl")


def get_payment_fingerprint(payment_header: str) -> str:
    value = (payment_header or "").strip()
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read_records() -> list[dict]:
    if not PAYMENTS_LOG_PATH.exists():
        return []
    rows: list[dict] = []
    with PAYMENTS_LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def is_payment_replay(payment_header: str) -> bool:
    fingerprint = get_payment_fingerprint(payment_header)
    for row in _read_records():
        if row.get("fingerprint") == fingerprint:
            return True
    return False


def record_payment_fingerprint(payment_header: str, trace_id: str | None = None) -> dict:
    fingerprint = get_payment_fingerprint(payment_header)
    record = {
        "fingerprint": fingerprint,
        "trace_id": trace_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    PAYMENTS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PAYMENTS_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=True) + "\n")
    return record


def get_replay_status() -> dict:
    return {
        "payment_log_path": str(PAYMENTS_LOG_PATH),
        "count_estimate": len(_read_records()),
    }
