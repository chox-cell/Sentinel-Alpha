from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_identity_erc8004_status_endpoint(monkeypatch):
    monkeypatch.delenv("ERC8004_ENABLED", raising=False)
    monkeypatch.delenv("ERC8004_REGISTRY_ADDRESS", raising=False)
    monkeypatch.delenv("ERC8004_AGENT_ID", raising=False)

    client = TestClient(app)
    response = client.get("/internal/identity/erc8004/status")
    assert response.status_code == 200
    body = response.json()
    assert body["enabled"] is False
    assert body["registry_configured"] is False
    assert body["agent_id_configured"] is False
    assert body["status"] == "planned"
    assert "ERC8004_REGISTRY_ADDRESS" not in body
    assert "ERC8004_AGENT_ID" not in body
