from fastapi.testclient import TestClient

from apps.api.main import app


def test_quicknode_dry_run_logs_source_and_flag(monkeypatch):
    from apps.webhooks import quicknode

    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)
    monkeypatch.setenv("QUICKNODE_DRY_RUN", "true")
    monkeypatch.setattr(quicknode, "handle_new_contract", lambda payload: {"status_code": 200, "body": payload})

    captured = {}

    def fake_log_event(event_type, payload):
        captured["event_type"] = event_type
        captured["payload"] = payload

    monkeypatch.setattr(quicknode, "log_event", fake_log_event)

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        json={"contract_address": "0x1111111111111111111111111111111111111111", "chain": "base"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert captured["event_type"] == "webhook_received"
    assert captured["payload"]["source"] == "quicknode"
    assert captured["payload"]["dry_run"] is True
