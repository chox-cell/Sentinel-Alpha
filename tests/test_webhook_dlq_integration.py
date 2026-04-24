from fastapi.testclient import TestClient

from apps.api.main import app


def test_failed_candidate_goes_to_dlq_and_webhook_continues(monkeypatch):
    from services.scout_cell import hunter

    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)
    monkeypatch.setattr(
        hunter,
        "reduce_quicknode_event",
        lambda payload: [
            {
                "contract_address": "0x1111111111111111111111111111111111111111",
                "chain": "base",
                "event_type": "contract_event",
                "transaction_hash": "0xtx1",
                "block_number": 1,
                "log_count": 1,
                "context": {"event_type": "contract_event"},
            },
            {
                "contract_address": "0x2222222222222222222222222222222222222222",
                "chain": "base",
                "event_type": "contract_event",
                "transaction_hash": "0xtx2",
                "block_number": 2,
                "log_count": 1,
                "context": {"event_type": "contract_event"},
            },
        ],
    )

    def fake_evaluate(contract_address: str, chain: str, context: dict | None = None):
        if contract_address.endswith("2222"):
            raise RuntimeError("sim failure")
        return {
            "api_version": "2026.8.0",
            "decision": {"action": "ALLOW", "emergency_signal": "NONE", "confidence": 0.6},
            "risk_metrics": {"score": 15, "threat_class": "normal"},
            "signals": {},
            "attestation": {},
            "latency": {"lane": "standard", "latency_ms": 1},
            "meta": {"ttl_seconds": 300, "trace_id": "trace"},
            "billing": {"amount": "0.02", "method": "x402", "status": "demo"},
        }

    captured = {"count": 0}

    def fake_write_dlq(record: dict):
        captured["count"] += 1
        return {**record, "created_at": "2026-01-01T00:00:00+00:00"}

    monkeypatch.setattr(hunter, "evaluate_contract", fake_evaluate)
    monkeypatch.setattr(hunter, "write_dlq", fake_write_dlq)

    client = TestClient(app)
    response = client.post("/webhooks/quicknode", json={"any": "payload"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["result"]["status"] == "ok"
    assert body["result"]["candidates"] == 2
    assert len(body["result"]["results"]) == 2
    assert captured["count"] == 1
