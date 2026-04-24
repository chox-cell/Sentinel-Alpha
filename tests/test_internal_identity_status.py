from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_identity_status_endpoint(monkeypatch):
    monkeypatch.setenv("SENTINEL_IDENTITY_MODE", "real_key")
    monkeypatch.setenv("SENTINEL_AGENT_DID", "did:sentinel-alpha:test")
    monkeypatch.setenv("SENTINEL_ATTESTATION_PRIVATE_KEY", "private-key-only")
    monkeypatch.setenv("SENTINEL_ATTESTATION_PUBLIC_KEY", "public-key-only")
    monkeypatch.delenv("SENTINEL_ERC8004_CONTRACT_ADDRESS", raising=False)

    client = TestClient(app)
    response = client.get("/internal/identity/status")
    assert response.status_code == 200
    body = response.json()
    assert body["identity_mode"] == "real_key"
    assert body["did"] == "did:sentinel-alpha:test"
    assert body["real_key_enabled"] is True
    assert body["erc8004_enabled"] is False
    assert "SENTINEL_ATTESTATION_PUBLIC_KEY" not in body
