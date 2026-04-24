from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402 import settlement_ledger


def test_x402_settlement_status_endpoint(monkeypatch, tmp_path):
    log_path = tmp_path / "x402_settlements.jsonl"
    monkeypatch.setattr(settlement_ledger, "SETTLEMENT_LOG_PATH", log_path)
    monkeypatch.setenv("X402_NETWORK", "base")
    settlement_ledger.write_settlement_record({"trace_id": "trace-1"})

    client = TestClient(app)
    response = client.get("/internal/x402/settlements/status")
    assert response.status_code == 200
    body = response.json()
    assert body["settlement_log_path"] == str(log_path)
    assert body["count_estimate"] == 1
    assert body["network"] == "base"
