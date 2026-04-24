import json
from datetime import datetime, timezone
from pathlib import Path

from services.dlq.dead_letter import read_dlq
from services.risk_service.service import evaluate_contract


REPLAY_LOG_PATH = Path("logs/replay.jsonl")


def run(limit: int = 50) -> dict:
    records = read_dlq(limit=limit)
    summary = {
        "attempted": len(records),
        "succeeded": 0,
        "failed": 0,
        "results": [],
    }

    for record in records:
        candidate = record.get("candidate") or {}
        try:
            evaluate_contract(
                contract_address=candidate.get("contract_address", ""),
                chain=candidate.get("chain", "base"),
                context=candidate.get("context", {}),
            )
            item = {
                "trace_id": record.get("trace_id"),
                "status": "replayed",
                "source": record.get("source"),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            summary["succeeded"] += 1
        except Exception as exc:
            item = {
                "trace_id": record.get("trace_id"),
                "status": "failed",
                "source": record.get("source"),
                "error": str(exc),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            summary["failed"] += 1
        summary["results"].append(item)

    _append_replay(summary)
    return summary


def _append_replay(summary: dict) -> None:
    REPLAY_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPLAY_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary, ensure_ascii=True) + "\n")


if __name__ == "__main__":
    run()
