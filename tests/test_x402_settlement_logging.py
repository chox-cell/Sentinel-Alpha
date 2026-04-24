import json

from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402 import replay_guard, settlement_ledger


def _request_body() -> dict:
    return {
        "contract_address": "0x11111111111111111111111111111111111111aa",
        "chain": "base",
        "context": {"event_type": "new_deploy"},
    }


def test_settlement_logging_and_replay_block(monkeypatch, tmp_path):
    replay_path = tmp_path / "x402_payments.jsonl"
    settlement_path = tmp_path / "x402_settlements.jsonl"
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", replay_path)
    monkeypatch.setattr(settlement_ledger, "SETTLEMENT_LOG_PATH", settlement_path)
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xtreasury")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")

    tx_header = "tx:0x" + ("e" * 64)
    client = TestClient(app)

    first = client.post(
        "/contracts/risk-score",
        json=_request_body(),
        headers={"X402-PAYMENT": tx_header},
    )
    assert first.status_code == 200
    assert first.json()["billing"]["status"] == "tx_format_valid_unverified"

    settlement_lines = settlement_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(settlement_lines) == 1
    settlement = json.loads(settlement_lines[0])
    assert settlement["tx_hash"] == "0x" + ("e" * 64)
    assert settlement["verification_status"] == "tx_format_valid_unverified"
    assert settlement["payment_fingerprint"]
    assert tx_header not in settlement_path.read_text(encoding="utf-8")

    second = client.post(
        "/contracts/risk-score",
        json=_request_body(),
        headers={"X402-PAYMENT": tx_header},
    )
    assert second.status_code == 402
    assert second.json()["detail"] == {"error": "x402_replay_detected"}
    assert len(settlement_path.read_text(encoding="utf-8").strip().splitlines()) == 1
