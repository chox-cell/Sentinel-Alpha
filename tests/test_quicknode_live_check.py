from fastapi.testclient import TestClient

from apps.api.main import app


def test_quicknode_live_check_not_ready_in_dry_run(monkeypatch):
    monkeypatch.setenv("QUICKNODE_WEBHOOK_URL", "https://example.ngrok-free.app/webhooks/quicknode")
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", "secret")
    monkeypatch.setenv("QUICKNODE_DRY_RUN", "true")
    monkeypatch.setenv("QUICKNODE_CHAIN", "base")

    client = TestClient(app)
    response = client.get("/internal/quicknode-live-check")

    assert response.status_code == 200
    body = response.json()
    assert body["ready_for_live"] is False
    assert body["checks"] == {
        "webhook_url_configured": True,
        "webhook_secret_configured": True,
        "dry_run": True,
        "chain": "base",
    }


def test_quicknode_live_check_ready_when_all_requirements_met(monkeypatch):
    monkeypatch.setenv("QUICKNODE_WEBHOOK_URL", "https://example.ngrok-free.app/webhooks/quicknode")
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", "secret")
    monkeypatch.setenv("QUICKNODE_DRY_RUN", "false")
    monkeypatch.setenv("QUICKNODE_CHAIN", "base")

    client = TestClient(app)
    response = client.get("/internal/quicknode-live-check")

    assert response.status_code == 200
    body = response.json()
    assert body["ready_for_live"] is True
    assert body["checks"]["webhook_url_configured"] is True
    assert body["checks"]["webhook_secret_configured"] is True
    assert body["checks"]["dry_run"] is False
    assert body["checks"]["chain"] == "base"
