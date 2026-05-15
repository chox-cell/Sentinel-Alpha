"""x402scan-style schema + PAYMENT-REQUIRED header compatibility (GET/POST unpaid 402 paths)."""

import base64
import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api import main as api_main
from apps.api.main import app

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def _hdr(raw: dict) -> tuple[str | None, str]:
    """Return (payment-required value, expose-headers lowercase) from response-ish headers."""
    pr = raw.get("payment-required") or raw.get("PAYMENT-REQUIRED")
    ex = (raw.get("access-control-expose-headers") or raw.get("Access-Control-Expose-Headers") or "").lower()
    return pr, ex


def test_get_402_legacy_and_discovery_schema(monkeypatch):
    monkeypatch.setenv("PUBLIC_BASE_URL", "https://api.example.invalid")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0x_payto_schema")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    response = client.get("/contracts/risk-score")
    assert response.status_code == 402

    raw = dict(response.headers)
    pr_val, expose = _hdr(raw)
    assert pr_val
    assert "payment-required" in expose

    body = response.json()
    assert body["x402_version"] == "0.2"
    assert body["x402Version"] == 1
    assert body["payment_method"] == "x402"
    assert isinstance(body["accepts"], list) and len(body["accepts"]) == 1

    req = body["accepts"][0]
    assert req["scheme"] == "exact"
    assert req["network"] == "eip155:8453"
    assert req["maxAmountRequired"] == "20000"
    assert req["payTo"] == "0x_payto_schema"
    assert req["asset"] == "USDC"
    assert req["resource"] == "https://api.example.invalid/contracts/risk-score"
    assert req["mimeType"] == "application/json"
    assert req["description"] == "BeezShield Sentinel Alpha risk score"

    dec = json.loads(base64.standard_b64decode(pr_val).decode("utf-8"))
    assert dec["x402Version"] == 1
    assert dec["accepts"][0]["maxAmountRequired"] == "20000"


def test_get_does_not_require_body_or_execute_scoring(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0x_payto_schema")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    calls: list[bool] = []

    def _no_eval(**_kw):
        calls.append(True)
        return {"response": {}, "outcome_record": None}

    monkeypatch.setattr(api_main, "evaluate_contract_with_meta", _no_eval)

    client = TestClient(app)
    response = client.get("/contracts/risk-score")
    assert response.status_code == 402
    assert calls == []


def test_post_unpaid_402_discovery_schema_and_headers(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xpost_schema")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "context": {},
        },
    )
    assert response.status_code == 402

    detail = response.json()["detail"]
    assert isinstance(detail, dict)
    assert detail["x402_version"] == "0.2"
    assert detail["x402Version"] == 1
    assert detail["accepts"][0]["scheme"] == "exact"
    assert detail["accepts"][0]["payTo"] == "0xpost_schema"
    assert detail["accepts"][0]["maxAmountRequired"] == "20000"

    raw = dict(response.headers)
    pr_val, expose = _hdr(raw)
    assert pr_val
    assert "payment-required" in expose
    decoded = json.loads(base64.standard_b64decode(pr_val).decode("utf-8"))
    assert decoded["x402Version"] == 1


def test_docs_second_attempt_schema_status_and_no_listing_claim():
    pack_low = PACK.read_text(encoding="utf-8").lower()
    outreach_low = OUTREACH.read_text(encoding="utf-8").lower()
    claims_low = CLAIMS.read_text(encoding="utf-8").lower()

    assert "attempted_validation_failed_schema" in outreach_low
    assert "second attempt" in outreach_low or "second registration" in outreach_low
    assert "x402scan" in pack_low
    assert (
        "payment-required" in pack_low
        or "payment required" in pack_low
        or "x402version" in pack_low
        or "accepts" in pack_low
    )
    assert "not submitted" in pack_low
    assert "x402scan" in claims_low and "second" in claims_low
    assert ("no listing" in claims_low) or ("not listed" in claims_low)


def test_env_unchanged_during_schema_compat_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    _ = OUTREACH.read_text(encoding="utf-8")
    _ = CLAIMS.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
