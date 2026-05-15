"""HEAD / OPTIONS discovery compatibility for `/contracts/risk-score` (x402scan-style probes)."""

import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api import main as api_main
from apps.api.main import app

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def _lower_headers(resp) -> dict[str, str]:
    return {str(k).lower(): str(v) for k, v in resp.headers.items()}


def test_head_contracts_risk_score_402_headers_empty_body(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xhead_wallet")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    response = client.head("/contracts/risk-score")
    assert response.status_code == 402
    assert response.content == b""
    h = _lower_headers(response)
    assert h.get("payment-required")
    assert "payment-required" in (h.get("access-control-expose-headers") or "").lower()


def test_head_does_not_run_scoring(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xhead_wallet")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    calls: list[bool] = []

    def _no_eval(**_kw):
        calls.append(True)
        return {"response": {}, "outcome_record": None}

    monkeypatch.setattr(api_main, "evaluate_contract_with_meta", _no_eval)

    client = TestClient(app)
    assert client.head("/contracts/risk-score").status_code == 402
    assert calls == []


def test_options_preflight_cors_headers(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    response = client.options("/contracts/risk-score")
    assert response.status_code in (200, 204)
    h = _lower_headers(response)
    methods = (h.get("access-control-allow-methods") or "").upper()
    for m in ("GET", "HEAD", "POST", "OPTIONS", "PATCH", "PUT", "DELETE"):
        assert m in methods
    allow_hdrs = (h.get("access-control-allow-headers") or "").lower()
    assert "x402-payment" in allow_hdrs
    assert "content-type" in allow_hdrs
    assert "x-sentinel-lane" in allow_hdrs
    assert "payment-required" in allow_hdrs
    assert "payment-required" in (h.get("access-control-expose-headers") or "").lower()


def test_options_does_not_run_scoring(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    calls: list[bool] = []

    def _no_eval(**_kw):
        calls.append(True)
        return {"response": {}, "outcome_record": None}

    monkeypatch.setattr(api_main, "evaluate_contract_with_meta", _no_eval)

    client = TestClient(app)
    assert client.options("/contracts/risk-score").status_code in (200, 204)
    assert calls == []


def test_get_still_402_with_schema_fields(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xget_wallet")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    r = client.get("/contracts/risk-score")
    assert r.status_code == 402
    body = r.json()
    assert body["x402Version"] == 1
    assert body["accepts"][0]["scheme"] == "exact"
    assert _lower_headers(r).get("payment-required")


def test_post_unpaid_still_402(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xpost_wallet")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    r = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "context": {},
        },
    )
    assert r.status_code == 402
    assert r.json()["detail"]["x402Version"] == 1


def test_docs_third_attempt_and_no_listing_success_claim():
    ot = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_head_options" in ot
    assert "third attempt" in ot
    text_pack = PACK.read_text(encoding="utf-8")
    pk = text_pack.lower()
    assert "3c)" in text_pack or "§3c" in text_pack
    assert "head" in pk and "options" in pk
    assert "x402scan" in pk
    assert "not submitted" in pk
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "third attempt" in cl
    assert "no verified directory listing claim" in cl or "no listing" in cl
    combo = OUTREACH.read_text(encoding="utf-8").lower() + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan submission approved" not in combo


def test_env_hash_unchanged_head_options_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    _ = OUTREACH.read_bytes()
    _ = CLAIMS.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
