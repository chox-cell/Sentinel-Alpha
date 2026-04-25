from fastapi.testclient import TestClient

from apps.api.main import app


def test_x402_onchain_status_endpoint(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "false")
    monkeypatch.setenv("X402_MOCK_ONCHAIN_VERIFY", "false")
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("X402_NETWORK", "base")

    client = TestClient(app)
    response = client.get("/internal/x402/onchain/status")
    assert response.status_code == 200
    body = response.json()
    assert body["onchain_verify_enabled"] is False
    assert body["mock_onchain_verify_enabled"] is False
    assert body["rpc_configured"] is False
    assert body["network"] == "base"
    assert "BASE_RPC_URL" not in body
