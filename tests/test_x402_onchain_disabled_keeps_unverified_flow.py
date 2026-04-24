from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402 import replay_guard, settlement_ledger


def _request_body() -> dict:
    return {
        "contract_address": "0x11111111111111111111111111111111111111bb",
        "chain": "base",
        "context": {"event_type": "new_deploy"},
    }


def test_onchain_disabled_keeps_tx_format_valid_unverified(monkeypatch, tmp_path):
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", tmp_path / "x402_payments.jsonl")
    monkeypatch.setattr(settlement_ledger, "SETTLEMENT_LOG_PATH", tmp_path / "x402_settlements.jsonl")
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "false")
    monkeypatch.setenv("PRICE_BASIC", "0.02")

    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json=_request_body(),
        headers={"X402-PAYMENT": "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    )
    assert response.status_code == 200
    billing = response.json()["billing"]
    assert billing["status"] == "tx_format_valid_unverified"
    assert billing["method"] == "x402"
