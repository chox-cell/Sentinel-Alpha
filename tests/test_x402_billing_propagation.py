from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402 import replay_guard, settlement_ledger


def _request_body() -> dict:
    return {
        "contract_address": "0x1111111111111111111111111111111111111122",
        "chain": "base",
        "context": {"event_type": "new_deploy"},
    }


def test_demo_response_billing_status(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("PAYMENT_DEMO_SIGNATURE", "demo")
    monkeypatch.setenv("PRICE_BASIC", "0.02")

    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json=_request_body(),
        headers={"PAYMENT-SIGNATURE": "demo"},
    )
    assert response.status_code == 200
    billing = response.json()["billing"]
    assert billing["method"] == "x402"
    assert billing["status"] == "demo"
    assert billing["amount"] == "0.02"


def test_real_tx_format_valid_response_billing_status(monkeypatch, tmp_path):
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", tmp_path / "x402_payments.jsonl")
    monkeypatch.setattr(settlement_ledger, "SETTLEMENT_LOG_PATH", tmp_path / "x402_settlements.jsonl")
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "false")
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("PRICE_BASIC", "0.09")

    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json=_request_body(),
        headers={"X402-PAYMENT": "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    )
    assert response.status_code == 200
    billing = response.json()["billing"]
    assert billing["method"] == "x402"
    assert billing["status"] == "tx_format_valid_unverified"
    assert billing["amount"] == "0.09"


def test_missing_real_payment_returns_challenge(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xtreasury")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")

    client = TestClient(app)
    response = client.post("/contracts/risk-score", json=_request_body())
    assert response.status_code == 402
    body = response.json()
    assert "detail" not in body
    assert body["x402_version"] == "0.2"
    assert body["payment_method"] == "x402"
    assert body["resource"] == "/contracts/risk-score"
