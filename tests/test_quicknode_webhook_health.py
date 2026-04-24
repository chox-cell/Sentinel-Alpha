from fastapi.testclient import TestClient

from apps.api.main import app


def test_quicknode_webhook_health_dev_disabled(monkeypatch):
    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)
    monkeypatch.delenv("QUICKNODE_WEBHOOK_URL", raising=False)
    monkeypatch.delenv("QUICKNODE_DRY_RUN", raising=False)

    client = TestClient(app)
    response = client.get("/webhooks/quicknode/health")

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "service": "quicknode-webhook",
        "signature_verification": "dev-disabled",
        "quicknode_env_status": {
            "webhook_url_configured": False,
            "webhook_secret_configured": False,
            "dry_run": False,
            "signature_mode": "dev-disabled",
        },
    }


def test_quicknode_webhook_health_enabled(monkeypatch):
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", "secret")
    monkeypatch.setenv("QUICKNODE_WEBHOOK_URL", "https://example.com")
    monkeypatch.setenv("QUICKNODE_DRY_RUN", "true")

    client = TestClient(app)
    response = client.get("/webhooks/quicknode/health")

    assert response.status_code == 200
    assert response.json()["signature_verification"] == "enabled"
    assert response.json()["quicknode_env_status"]["webhook_secret_configured"] is True
