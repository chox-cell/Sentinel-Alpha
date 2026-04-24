import json

from services.dlq import dead_letter


def test_write_and_read_dlq_jsonl(tmp_path, monkeypatch):
    target = tmp_path / "dlq.jsonl"
    monkeypatch.setattr(dead_letter, "DLQ_PATH", target)

    written = dead_letter.write_dlq(
        {
            "trace_id": "t-1",
            "source": "quicknode",
            "reason": "candidate_evaluation_failed",
            "candidate": {"contract_address": "0x1"},
            "error": "boom",
        }
    )
    assert written["trace_id"] == "t-1"
    assert target.exists()

    raw = target.read_text(encoding="utf-8").strip().splitlines()
    assert len(raw) == 1
    decoded = json.loads(raw[0])
    assert decoded["reason"] == "candidate_evaluation_failed"

    rows = dead_letter.read_dlq(limit=10)
    assert len(rows) == 1
    assert rows[0]["trace_id"] == "t-1"
