from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_attestation_status_stub(monkeypatch):
    monkeypatch.delenv("SENTINEL_ATTESTATION_PRIVATE_KEY", raising=False)
    monkeypatch.delenv("SENTINEL_ATTESTATION_PUBLIC_KEY", raising=False)

    client = TestClient(app)
    response = client.get("/internal/attestation/status")

    assert response.status_code == 200
    body = response.json()
    assert body["attestation_version"] == "attestation-0.1"
    assert body["signing_mode"] == "stub"
    assert body["public_key_configured"] is False
    assert body["private_key_configured"] is False


def test_internal_attestation_status_real_key(monkeypatch):
    monkeypatch.setenv("SENTINEL_ATTESTATION_PRIVATE_KEY", "secret")
    monkeypatch.setenv("SENTINEL_ATTESTATION_PUBLIC_KEY", "pub")

    client = TestClient(app)
    response = client.get("/internal/attestation/status")

    assert response.status_code == 200
    body = response.json()
    assert body["signing_mode"] == "real_key"
    assert body["public_key_configured"] is True
    assert body["private_key_configured"] is True
    assert "SENTINEL_ATTESTATION_PRIVATE_KEY" not in body
