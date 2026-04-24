from fastapi.testclient import TestClient

from apps.api.main import app


def test_quicknode_webhook_health_dev_disabled(monkeypatch):
    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)

    client = TestClient(app)
    response = client.get("/webhooks/quicknode/health")

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "service": "quicknode-webhook",
        "signature_verification": "dev-disabled",
    }


def test_quicknode_webhook_health_enabled(monkeypatch):
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", "secret")

    client = TestClient(app)
    response = client.get("/webhooks/quicknode/health")

    assert response.status_code == 200
    assert response.json()["signature_verification"] == "enabled"
