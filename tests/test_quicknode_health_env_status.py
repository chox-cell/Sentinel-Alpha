from fastapi.testclient import TestClient

from apps.api.main import app


def test_quicknode_health_includes_env_status(monkeypatch):
    monkeypatch.setenv("QUICKNODE_WEBHOOK_URL", "https://example.com/webhook")
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", "secret")
    monkeypatch.setenv("QUICKNODE_DRY_RUN", "true")

    client = TestClient(app)
    response = client.get("/webhooks/quicknode/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "quicknode-webhook"
    assert body["signature_verification"] == "enabled"
    assert "quicknode_env_status" in body
    assert body["quicknode_env_status"] == {
        "webhook_url_configured": True,
        "webhook_secret_configured": True,
        "dry_run": True,
        "signature_mode": "enabled",
    }
