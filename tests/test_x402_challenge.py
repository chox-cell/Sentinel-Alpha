from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402.payment import build_x402_challenge


def test_build_x402_challenge_uses_lane_and_addresses(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xtreasury")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_EXECUTIVE", "0.07")

    challenge = build_x402_challenge("executive")
    assert challenge == {
        "x402_version": "0.2",
        "payment_method": "x402",
        "network": "eip155:8453",
        "pay_to": "0xtreasury",
        "amount_usdc": "0.07",
        "asset": "USDC",
        "resource": "/contracts/risk-score",
        "instructions": "Submit X402-PAYMENT header to access this resource.",
        "lane": "executive",
    }


def test_internal_x402_challenge_endpoint(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xtreasury")
    monkeypatch.setenv("X402_REVENUE_ADDRESS", "0xrevenue")
    monkeypatch.setenv("PRICE_PRIORITY", "0.23")

    client = TestClient(app)
    response = client.get("/internal/x402/challenge?lane=priority")
    assert response.status_code == 200
    body = response.json()
    assert body["x402_version"] == "0.2"
    assert body["payment_method"] == "x402"
    assert body["network"] == "eip155:8453"
    assert body["pay_to"] == "0xrevenue"
    assert body["amount_usdc"] == "0.23"
    assert body["asset"] == "USDC"
    assert body["resource"] == "/contracts/risk-score"
