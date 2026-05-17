"""Unpaid POST: pure x402scan v1 body (x402Version/error/accepts only); GET keeps legacy fields."""

import base64
import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402.payment import BASE_MAINNET_USDC_CONTRACT, X402_V1_DISCOVERY_ERROR

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"

_PURE_KEYS = frozenset({"x402Version", "error", "accepts"})
_LEGACY_KEYS = frozenset(
    {
        "x402_version",
        "payment_method",
        "network",
        "pay_to",
        "amount_usdc",
        "asset",
        "resource",
        "instructions",
        "lane",
        "detail",
    }
)
_OPENAPI_SAMPLE = {
    "contract_address": "0x1111111111111111111111111111111111111111",
    "chain": "base",
}


def _real_unpaid(monkeypatch, wallet: str = "0x_pure_post_v1") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def _assert_pure_post_body(body: dict) -> None:
    assert set(body.keys()) == _PURE_KEYS
    assert _LEGACY_KEYS.isdisjoint(body.keys())
    assert body["x402Version"] == 1
    assert body["error"] == X402_V1_DISCOVERY_ERROR
    a0 = body["accepts"][0]
    assert a0["network"] == "base"
    assert a0["asset"] == BASE_MAINNET_USDC_CONTRACT
    assert a0["maxAmountRequired"] == "20000"


def test_unpaid_post_pure_v1_variants(monkeypatch):
    _real_unpaid(monkeypatch)
    client = TestClient(app)
    calls = [
        lambda: client.post("/contracts/risk-score", content=b""),
        lambda: client.post("/contracts/risk-score", json={}),
        lambda: client.post(
            "/contracts/risk-score",
            content=b"not-json",
            headers={"Content-Type": "text/plain"},
        ),
        lambda: client.post("/contracts/risk-score", json=_OPENAPI_SAMPLE),
    ]
    for call in calls:
        r = call()
        assert r.status_code == 402
        _assert_pure_post_body(r.json())
        hdr = json.loads(base64.standard_b64decode(r.headers["payment-required"]).decode("utf-8"))
        assert set(hdr.keys()) == _PURE_KEYS
        assert hdr["accepts"][0]["network"] == "base"


def test_get_legacy_preserved_openapi_post_only(monkeypatch):
    _real_unpaid(monkeypatch)
    c = TestClient(app)
    get_body = c.get("/contracts/risk-score").json()
    assert get_body["x402_version"] == "0.2"
    assert get_body["payment_method"] == "x402"
    assert get_body["network"] == "eip155:8453"
    assert get_body["x402Version"] == 1
    assert get_body["error"] == X402_V1_DISCOVERY_ERROR

    paths = c.get("/openapi.json").json().get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score"]
    assert list(paths["/contracts/risk-score"].keys()) == ["post"]


def test_docs_eleventh_attempt_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_post_extra_fields" in ol
    assert "eleventh" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3k" in pt or "3k)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "eleventh" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo


def test_env_unchanged_pure_post_v1_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
