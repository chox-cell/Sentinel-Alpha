from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402 import replay_guard


def test_x402_replay_status_endpoint(monkeypatch, tmp_path):
    log_path = tmp_path / "x402_payments.jsonl"
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", log_path)
    replay_guard.record_payment_fingerprint("tx:0x" + ("d" * 64))

    client = TestClient(app)
    response = client.get("/internal/x402/replay/status")
    assert response.status_code == 200
    body = response.json()
    assert body["payment_log_path"] == str(log_path)
    assert body["count_estimate"] == 1
