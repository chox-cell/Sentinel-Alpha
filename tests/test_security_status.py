from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_security_status_defaults(monkeypatch):
    monkeypatch.delenv("QUICKNODE_SIGNATURE_REQUIRED", raising=False)
    monkeypatch.delenv("RATE_LIMIT_ENABLED", raising=False)
    monkeypatch.delenv("RATE_LIMIT_PER_MINUTE", raising=False)

    client = TestClient(app)
    response = client.get("/internal/security/status")
    assert response.status_code == 200
    body = response.json()
    assert body["quicknode_signature_required"] is False
    assert body["rate_limit_enabled"] is False
    assert body["rate_limit_per_minute"] == 60


def test_internal_security_status_enabled(monkeypatch):
    monkeypatch.setenv("QUICKNODE_SIGNATURE_REQUIRED", "true")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "120")

    client = TestClient(app)
    response = client.get("/internal/security/status")
    assert response.status_code == 200
    body = response.json()
    assert body["quicknode_signature_required"] is True
    assert body["rate_limit_enabled"] is True
    assert body["rate_limit_per_minute"] == 120
