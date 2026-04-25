import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from apps.api.main import app


def test_quicknode_signature_required_rejects_missing_signature(monkeypatch):
    monkeypatch.setenv("QUICKNODE_SIGNATURE_REQUIRED", "true")
    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        content=b'{"contract_address":"0x1","chain":"base"}',
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 401


def test_quicknode_signature_required_rejects_invalid_signature(monkeypatch):
    monkeypatch.setenv("QUICKNODE_SIGNATURE_REQUIRED", "true")
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", "secret")

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        content=b'{"contract_address":"0x1","chain":"base"}',
        headers={"content-type": "application/json", "x-qn-signature": "invalid"},
    )
    assert response.status_code == 401


def test_quicknode_signature_required_accepts_valid_signature(monkeypatch):
    from apps.webhooks import quicknode

    secret = "secret"
    monkeypatch.setenv("QUICKNODE_SIGNATURE_REQUIRED", "true")
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", secret)
    monkeypatch.setattr(quicknode, "handle_new_contract", lambda payload: {"status_code": 200, "body": payload})

    payload = {"contract_address": "0x1111111111111111111111111111111111111111", "chain": "base"}
    raw_body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        content=raw_body,
        headers={"content-type": "application/json", "x-qn-signature": signature},
    )
    assert response.status_code == 200
