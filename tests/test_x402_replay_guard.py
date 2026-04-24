import json

from services.x402 import replay_guard


def test_replay_guard_records_fingerprint_without_raw_header(monkeypatch, tmp_path):
    log_path = tmp_path / "x402_payments.jsonl"
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", log_path)

    header = "tx:0x" + ("a" * 64)
    record = replay_guard.record_payment_fingerprint(header, trace_id="trace-1")
    assert record["fingerprint"] == replay_guard.get_payment_fingerprint(header)
    assert record["trace_id"] == "trace-1"
    assert "payment_header" not in record

    data = json.loads(log_path.read_text(encoding="utf-8").strip())
    assert data["fingerprint"] == record["fingerprint"]
    assert "payment_header" not in data
    assert header not in log_path.read_text(encoding="utf-8")


def test_replay_guard_detects_replay(monkeypatch, tmp_path):
    log_path = tmp_path / "x402_payments.jsonl"
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", log_path)
    header = "tx:0x" + ("b" * 64)

    assert replay_guard.is_payment_replay(header) is False
    replay_guard.record_payment_fingerprint(header)
    assert replay_guard.is_payment_replay(header) is True
