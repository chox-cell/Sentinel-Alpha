import json

from services.outcome_memory import memory


def test_record_decision_writes_jsonl(tmp_path, monkeypatch):
    target = tmp_path / "outcome_memory.jsonl"
    monkeypatch.setattr(memory, "OUTCOME_MEMORY_PATH", target)

    saved = memory.record_decision(
        {
            "trace_id": "t-1",
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "score": 70,
            "confidence": 0.75,
            "action": "REDUCE",
            "threat_class": "behavioral_launch_syndicate",
            "signals": {"shadow_link": 1},
            "attestation": {"decision_fingerprint": "sha256:test"},
            "created_at": "2026-01-01T00:00:00+00:00",
        }
    )

    assert saved["trace_id"] == "t-1"
    assert target.exists()

    lines = target.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    raw = json.loads(lines[0])
    assert raw["action"] == "REDUCE"


def test_get_recent_decisions_returns_latest_first(tmp_path, monkeypatch):
    target = tmp_path / "outcome_memory.jsonl"
    monkeypatch.setattr(memory, "OUTCOME_MEMORY_PATH", target)

    records = [
        {
            "trace_id": "t-1",
            "contract_address": "0x1",
            "chain": "base",
            "score": 10,
            "confidence": 0.6,
            "action": "ALLOW",
            "threat_class": "normal",
            "signals": {},
            "attestation": {},
            "created_at": "2026-01-01T00:00:00+00:00",
        },
        {
            "trace_id": "t-2",
            "contract_address": "0x2",
            "chain": "base",
            "score": 90,
            "confidence": 0.9,
            "action": "BLOCK",
            "threat_class": "behavioral_launch_syndicate",
            "signals": {"shadow_link": 1},
            "attestation": {},
            "created_at": "2026-01-01T00:01:00+00:00",
        },
    ]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(json.dumps(r) + "\n" for r in records), encoding="utf-8")

    recent = memory.get_recent_decisions(limit=1)
    assert len(recent) == 1
    assert recent[0]["trace_id"] == "t-2"
