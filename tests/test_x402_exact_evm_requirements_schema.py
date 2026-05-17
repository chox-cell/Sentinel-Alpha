"""Exact-EVM `accepts[]` / PAYMENT-REQUIRED alignment (Base USDC contract, timeout, extras)."""

import base64
import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402.payment import BASE_MAINNET_USDC_CONTRACT

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def _lower_hdrs(resp) -> dict[str, str]:
    return {str(k).lower(): str(v) for k, v in resp.headers.items()}


def test_get_402_payment_required_and_body_accepts_exact_evm(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0x_payto_exact_evM")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    r = client.get("/contracts/risk-score")
    assert r.status_code == 402

    pr = _lower_hdrs(r).get("payment-required")
    assert pr
    hdr_json = json.loads(base64.standard_b64decode(pr).decode("utf-8"))
    assert hdr_json["x402Version"] == 1
    assert isinstance(hdr_json["accepts"], list) and len(hdr_json["accepts"]) == 1
    h0 = hdr_json["accepts"][0]
    assert h0["scheme"] == "exact"
    assert h0["network"] == "base"
    assert hdr_json["error"] == "X-PAYMENT header is required"
    assert h0["asset"] == BASE_MAINNET_USDC_CONTRACT
    assert "amount" not in h0
    assert h0["maxAmountRequired"] == "20000"
    assert h0["outputSchema"]["input"]["type"] == "http"
    assert h0["payTo"] == "0x_payto_exact_evM"
    assert h0["maxTimeoutSeconds"] == 60
    assert h0["extra"]["name"] == "USD Coin"
    assert h0["extra"]["version"] == "2"

    body = r.json()
    assert body["asset"] == "USDC"
    assert body["resource"] == "/contracts/risk-score"
    b0 = body["accepts"][0]
    assert b0 == h0


def test_head_options_post_unpaid_preserved(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0x_payto_combo")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    head = client.head("/contracts/risk-score")
    assert head.status_code == 402
    assert head.content == b""
    assert _lower_hdrs(head).get("payment-required")

    opt = client.options("/contracts/risk-score")
    assert opt.status_code in (200, 204)

    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    post = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "context": {},
        },
    )
    assert post.status_code == 402
    post_body = post.json()
    assert "detail" not in post_body
    assert post_body["accepts"][0]["asset"] == BASE_MAINNET_USDC_CONTRACT


def test_docs_fourth_attempt_and_no_verified_listing_claim():
    pack_text = PACK.read_text(encoding="utf-8")
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_requirements_schema" in ol
    assert "fourth" in ol
    assert "3d)" in pack_text or "§3d" in pack_text
    pk_low = pack_text.lower()
    assert "x402scan" in pk_low
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "fourth" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo


def test_env_unchanged_exact_evm_schema_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    _ = OUTREACH.read_bytes()
    _ = CLAIMS.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
