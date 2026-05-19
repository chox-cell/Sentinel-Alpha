"""Bazaar / x402 v2 discovery on POST /contracts/risk-score-v2 (separate from x402scan v1)."""

import base64
import json

from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402.payment import BASE_MAINNET_USDC_CONTRACT


def _real_unpaid(monkeypatch, wallet: str = "0x_bazaar_v2_probe") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def _decode_payment_required(header: str) -> dict:
    return json.loads(base64.b64decode(header.encode("ascii")).decode("utf-8"))


def test_v1_endpoint_still_body_first_without_payment_required_header(monkeypatch):
    _real_unpaid(monkeypatch)
    r = TestClient(app).post("/contracts/risk-score", content=b"")
    assert r.status_code == 402
    assert r.headers.get("payment-required") is None
    body = r.json()
    assert body["x402Version"] == 1
    assert set(body.keys()) == {"x402Version", "error", "accepts"}


def test_v2_unpaid_post_has_payment_required_header_and_payload(monkeypatch):
    _real_unpaid(monkeypatch)
    r = TestClient(app).post("/contracts/risk-score-v2", content=b"")
    assert r.status_code == 402

    header_raw = r.headers.get("PAYMENT-REQUIRED") or r.headers.get("payment-required")
    assert header_raw is not None
    decoded = _decode_payment_required(header_raw)
    body = r.json()

    for payload in (decoded, body):
        assert payload["x402Version"] == 2
        assert payload["error"] == "X-PAYMENT header is required"
        assert "resource" in payload
        assert payload["resource"]["url"].endswith("/contracts/risk-score-v2")
        assert payload["resource"]["method"] == "POST"
        assert "extensions" in payload
        assert "bazaar" in payload["extensions"]
        a0 = payload["accepts"][0]
        assert a0["amount"] == "20000"
        assert a0["network"] == "base"
        assert a0["asset"] == BASE_MAINNET_USDC_CONTRACT
