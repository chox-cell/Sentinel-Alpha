from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402.payment import (
    BASE_MAINNET_USDC_CONTRACT,
    X402_V1_DISCOVERY_ERROR,
    build_x402_challenge,
)


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
        "x402Version": 1,
        "error": X402_V1_DISCOVERY_ERROR,
        "accepts": [
            {
                "scheme": "exact",
                "network": "base",
                "asset": BASE_MAINNET_USDC_CONTRACT,
                "maxAmountRequired": "70000",
                "payTo": "0xtreasury",
                "maxTimeoutSeconds": 60,
                "resource": "https://api.beezshield.com/contracts/risk-score",
                "description": "BeezShield Sentinel Alpha risk score",
                "mimeType": "application/json",
                "extra": {"name": "USD Coin", "version": "2"},
                "outputSchema": {
                    "input": {
                        "type": "http",
                        "method": "POST",
                        "discoverable": True,
                        "bodyType": "json",
                        "bodyFields": {
                            "contract_address": {
                                "type": "string",
                                "description": "Contract address to evaluate",
                                "required": True,
                            },
                            "chain": {
                                "type": "string",
                                "description": "Target chain, e.g. base",
                                "required": True,
                            },
                        },
                    }
                },
            }
        ],
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
    assert body["x402Version"] == 1
    assert body["accepts"][0]["scheme"] == "exact"
    assert body["accepts"][0]["maxAmountRequired"] == "230000"
    assert "amount" not in body["accepts"][0]
    assert body["accepts"][0]["outputSchema"]["input"]["method"] == "POST"
    assert body["accepts"][0]["asset"] == BASE_MAINNET_USDC_CONTRACT
    assert body["accepts"][0]["maxTimeoutSeconds"] == 60
    assert body["accepts"][0]["network"] == "base"
    assert body["error"] == X402_V1_DISCOVERY_ERROR
    assert body["accepts"][0]["extra"] == {"name": "USD Coin", "version": "2"}
