from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_x402_status_endpoint(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("CDP_PROJECT_ID", "project")
    monkeypatch.setenv("CDP_API_KEY_NAME", "name")
    monkeypatch.setenv("CDP_API_KEY_PRIVATE_KEY", "private")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xabc")
    monkeypatch.setenv("X402_NETWORK", "base")

    client = TestClient(app)
    response = client.get("/internal/x402/status")

    assert response.status_code == 200
    body = response.json()
    assert body["payment_method"] == "x402"
    assert body["payment_mode"] == "real"
    assert "pricing_tiers" in body
    assert body["pricing_valid"] is True
    assert body["real_payments_enabled"] is True
    assert "CDP_API_KEY_PRIVATE_KEY" not in body
