from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_x402_pricing_endpoint(monkeypatch):
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("PRICE_EXECUTIVE", "0.05")
    monkeypatch.setenv("PRICE_PREMIUM", "0.10")
    monkeypatch.setenv("PRICE_PRIORITY", "0.15")
    monkeypatch.setenv("X402_DEFAULT_PRICE_USDC", "0.05")

    client = TestClient(app)
    response = client.get("/internal/x402/pricing")

    assert response.status_code == 200
    body = response.json()
    assert body["default_lane"] == "basic"
    assert body["pricing_tiers"] == {
        "basic": 0.02,
        "executive": 0.05,
        "premium": 0.10,
        "priority": 0.15,
        "default": 0.05,
    }
