from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402 import replay_guard, settlement_ledger


def _body() -> dict:
    return {
        "contract_address": "0x1111111111111111111111111111111111111111",
        "chain": "base",
        "context": {},
    }


def test_invalid_lane_returns_400(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("PAYMENT_DEMO_SIGNATURE", "demo")
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json=_body(),
        headers={"PAYMENT-SIGNATURE": "demo", "X-SENTINEL-LANE": "vip"},
    )
    assert response.status_code == 400
    assert response.json() == {"error": "invalid_lane"}


def test_default_lane_remains_basic_billing(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("PAYMENT_DEMO_SIGNATURE", "demo")
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json=_body(),
        headers={"PAYMENT-SIGNATURE": "demo"},
    )
    assert response.status_code == 200
    assert response.json()["billing"]["amount"] == "0.02"


def test_priority_lane_reflects_challenge_amount(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("PRICE_PRIORITY", "0.15")
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json=_body(),
        headers={"X-SENTINEL-LANE": "priority"},
    )
    assert response.status_code == 402
    body = response.json()
    assert "detail" not in body
    assert body["lane"] == "priority"
    assert body["amount_usdc"] == "0.15"


def test_priority_lane_reflects_billing_amount_on_paid_success(monkeypatch, tmp_path):
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", tmp_path / "x402_payments.jsonl")
    monkeypatch.setattr(settlement_ledger, "SETTLEMENT_LOG_PATH", tmp_path / "x402_settlements.jsonl")
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "false")
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("PRICE_PRIORITY", "0.15")
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json=_body(),
        headers={
            "X-SENTINEL-LANE": "priority",
            "X402-PAYMENT": "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        },
    )
    assert response.status_code == 200
    billing = response.json()["billing"]
    assert billing["amount"] == "0.15"
    assert billing["status"] == "tx_format_valid_unverified"


def test_internal_x402_lanes_endpoint(monkeypatch):
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("PRICE_EXECUTIVE", "0.05")
    monkeypatch.setenv("PRICE_PREMIUM", "0.10")
    monkeypatch.setenv("PRICE_PRIORITY", "0.15")
    client = TestClient(app)
    response = client.get("/internal/x402/lanes")
    assert response.status_code == 200
    body = response.json()
    assert body["supported_lanes"] == ["basic", "executive", "premium", "priority"]
    assert body["default_lane"] == "basic"
    assert body["pricing_tiers"]["priority"] == 0.15
