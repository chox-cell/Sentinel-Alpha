from fastapi.testclient import TestClient

from apps.api.main import app


def test_webhook_uses_reducer_and_returns_summary(monkeypatch):
    from services.scout_cell import hunter

    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)

    def fake_evaluate(contract_address: str, chain: str, context: dict | None = None) -> dict:
        return {
            "api_version": "2026.8.0",
            "decision": {"action": "ALLOW", "emergency_signal": "NONE", "confidence": 0.6},
            "risk_metrics": {"score": 15, "threat_class": "normal"},
            "signals": {},
            "attestation": {},
            "latency": {"lane": "standard", "latency_ms": 1},
            "meta": {"ttl_seconds": 300, "trace_id": "test-trace"},
            "billing": {"amount": "0.02", "method": "x402", "status": "demo"},
        }

    monkeypatch.setattr(hunter, "evaluate_contract", fake_evaluate)

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        json={
            "receipt": {
                "logs": [
                    {"address": "0x1111111111111111111111111111111111111111", "topics": ["token"]}
                ]
            },
            "transactionHash": "0xabc",
            "blockNumber": 123,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["result"]["status"] == "ok"
    assert body["result"]["candidates"] == 1
    assert len(body["result"]["results"]) == 1
    assert body["result"]["results"][0]["status_code"] == 200
