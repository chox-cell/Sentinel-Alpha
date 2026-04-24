from fastapi.testclient import TestClient

from apps.api.main import app


def test_webhook_skips_transfer_candidates(monkeypatch):
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
                "context": {
                    "topic0": "0xddf252ad00000000000000000000000000000000000000000000000000000000",
                },
            }
        ],
    )

    called = {"count": 0}

    def fake_evaluate(contract_address: str, chain: str, context: dict | None = None):
        called["count"] += 1
        return {}

    monkeypatch.setattr(hunter, "evaluate_contract", fake_evaluate)

    client = TestClient(app)
    response = client.post("/webhooks/quicknode", json={"any": "payload"})

    assert response.status_code == 200
    body = response.json()
    assert body["result"]["status"] == "ok"
    assert body["result"]["candidates"] == 1
    assert body["result"]["evaluated"] == 0
    assert body["result"]["skipped"] == 1
    assert body["result"]["results"][0]["status"] == "skipped"
    assert called["count"] == 0
