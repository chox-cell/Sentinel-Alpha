import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from apps.api.main import app


def test_webhook_signature_dev_mode_allows_request(monkeypatch):
    from apps.webhooks import quicknode

    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)
    monkeypatch.setattr(quicknode, "handle_new_contract", lambda payload: {"status_code": 200, "body": payload})

    body = b'{"contract_address":"0x1111111111111111111111111111111111111111","chain":"base"}'
    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        content=body,
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_webhook_signature_invalid_returns_401(monkeypatch):
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", "secret")

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        content=b'{"contract_address":"0x1","chain":"base"}',
        headers={
            "content-type": "application/json",
            "x-qn-signature": "invalid",
        },
    )

    assert response.status_code == 401


def test_webhook_signature_valid_returns_200(monkeypatch):
    from apps.webhooks import quicknode

    secret = "secret"
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", secret)
    monkeypatch.setattr(quicknode, "handle_new_contract", lambda payload: {"status_code": 200, "body": payload})

    payload = {
        "contract_address": "0x1111111111111111111111111111111111111111",
        "chain": "base",
        "event_type": "new_deploy",
    }
    raw_body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        content=raw_body,
        headers={
            "content-type": "application/json",
            "x-qn-signature": signature,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
