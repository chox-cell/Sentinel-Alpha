from fastapi.testclient import TestClient

from apps.api.main import app


def test_large_zero_candidate_payload_logs_inspection(monkeypatch):
    from apps.webhooks import quicknode

    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)
    monkeypatch.setenv("QUICKNODE_DRY_RUN", "true")
    monkeypatch.setattr(
        quicknode,
        "handle_new_contract",
        lambda payload: {"status": "ok", "candidates": 0, "results": []},
    )

    captured = []

    def fake_log_event(event_type, payload):
        captured.append((event_type, payload))

    monkeypatch.setattr(quicknode, "log_event", fake_log_event)

    client = TestClient(app)
    large_payload = {"blob": "x" * 120000}
    response = client.post("/webhooks/quicknode", json=large_payload)

    assert response.status_code == 200
    inspected = [e for e in captured if e[0] == "quicknode_payload_inspected"]
    assert len(inspected) == 1
    inspection_payload = inspected[0][1]
    assert inspection_payload["payload_size_bytes"] > 100000
    assert "inspection" in inspection_payload
    # Key names are allowed in summary; raw large values must not be logged.
    assert "x" * 1000 not in str(inspection_payload["inspection"])
