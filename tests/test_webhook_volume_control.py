from fastapi.testclient import TestClient

from apps.api.main import app


def test_evaluations_capped_per_webhook(monkeypatch):
    from services.scout_cell import hunter

    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)
    monkeypatch.setenv("SENTINEL_MAX_EVALUATIONS_PER_WEBHOOK", "1")

    monkeypatch.setattr(
        hunter,
        "reduce_quicknode_event",
        lambda payload: [
            {
                "contract_address": "0x1111111111111111111111111111111111111111",
                "chain": "base",
                "event_type": "first_liquidity",
                "transaction_hash": "0xtx1",
                "block_number": 1,
                "log_count": 2,
                "context": {"event_type": "first_liquidity"},
            },
            {
                "contract_address": "0x2222222222222222222222222222222222222222",
                "chain": "base",
                "event_type": "new_token_candidate",
                "transaction_hash": "0xtx2",
                "block_number": 2,
                "log_count": 1,
                "context": {"event_type": "new_token_candidate"},
            },
        ],
    )

    calls = {"count": 0}

    def fake_eval(contract_address: str, chain: str, context: dict | None = None):
        calls["count"] += 1
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

    monkeypatch.setattr(hunter, "evaluate_contract", fake_eval)

    client = TestClient(app)
    response = client.post("/webhooks/quicknode", json={"any": "payload"})
    assert response.status_code == 200
    body = response.json()
    assert body["result"]["evaluated"] == 1
    assert body["result"]["skipped"] == 1
    assert calls["count"] == 1


def test_hard_payload_limit_ignores_processing(monkeypatch):
    from services.scout_cell import hunter

    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)
    monkeypatch.setenv("SENTINEL_MAX_PAYLOAD_BYTES_HARD", "100")

    called = {"count": 0}

    def fake_eval(contract_address: str, chain: str, context: dict | None = None):
        called["count"] += 1
        return {}

    monkeypatch.setattr(hunter, "evaluate_contract", fake_eval)

    client = TestClient(app)
    response = client.post("/webhooks/quicknode", json={"blob": "x" * 1000})
    assert response.status_code == 200
    body = response.json()
    assert body["result"]["status"] == "ignored"
    assert body["result"]["reason"] == "payload_too_large"
    assert called["count"] == 0
