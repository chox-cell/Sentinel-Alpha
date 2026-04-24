import json

from services.x402 import settlement_ledger


def test_write_and_read_settlement_records(monkeypatch, tmp_path):
    log_path = tmp_path / "x402_settlements.jsonl"
    monkeypatch.setattr(settlement_ledger, "SETTLEMENT_LOG_PATH", log_path)

    written = settlement_ledger.write_settlement_record(
        {
            "trace_id": "trace-123",
            "tx_hash": "0x" + ("a" * 64),
            "payment_fingerprint": "fp-1",
            "lane": "basic",
            "amount": "0.02",
            "network": "base",
            "treasury_wallet": "0xtreasury",
            "verification_status": "tx_format_valid_unverified",
        }
    )
    assert written["trace_id"] == "trace-123"
    assert "created_at" in written

    rows = settlement_ledger.read_settlement_records(limit=10)
    assert len(rows) == 1
    assert rows[0]["trace_id"] == "trace-123"
    assert rows[0]["verification_status"] == "tx_format_valid_unverified"

    loaded = json.loads(log_path.read_text(encoding="utf-8").strip())
    assert loaded["trace_id"] == "trace-123"
    assert "X402-PAYMENT" not in loaded


def test_get_settlement_status(monkeypatch, tmp_path):
    log_path = tmp_path / "x402_settlements.jsonl"
    monkeypatch.setattr(settlement_ledger, "SETTLEMENT_LOG_PATH", log_path)
    monkeypatch.setenv("X402_NETWORK", "base")
    settlement_ledger.write_settlement_record({"trace_id": "t1"})
    status = settlement_ledger.get_settlement_status()
    assert status["settlement_log_path"] == str(log_path)
    assert status["count_estimate"] == 1
    assert status["network"] == "base"
