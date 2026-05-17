"""x402scan strict ``accepts[]``: ``amount`` + ``maxAmountRequired``, ``outputSchema.input``."""

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

_SAMPLE = {
    "contract_address": "0x1111111111111111111111111111111111111111",
    "chain": "base",
}


def _real_unpaid(monkeypatch, wallet: str = "0x_accepts_strict") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def _assert_strict_accepts(a0: dict, *, pay_to: str) -> None:
    assert a0["scheme"] == "exact"
    assert a0["network"] == "base"
    assert a0["asset"] == BASE_MAINNET_USDC_CONTRACT
    assert a0["amount"] == "20000"
    assert a0["maxAmountRequired"] == "20000"
    assert a0["payTo"] == pay_to
    assert a0["maxTimeoutSeconds"] == 60
    assert a0["resource"].endswith("/contracts/risk-score")
    assert a0["description"] == "BeezShield Sentinel Alpha risk score"
    assert a0["mimeType"] == "application/json"
    assert a0["extra"] == {"name": "USD Coin", "version": "2"}
    inp = a0["outputSchema"]["input"]
    assert inp["type"] == "http"
    assert inp["method"] == "POST"
    assert inp["discoverable"] is True
    assert inp["bodyType"] == "json"
    fields = inp["bodyFields"]
    assert "contract_address" in fields and fields["contract_address"]["required"] is True
    assert "chain" in fields and fields["chain"]["required"] is True


def test_post_unpaid_strict_accepts_and_header(monkeypatch):
    _real_unpaid(monkeypatch)
    client = TestClient(app)
    for call in (
        lambda: client.post("/contracts/risk-score", content=b""),
        lambda: client.post("/contracts/risk-score", json=_SAMPLE),
    ):
        r = call()
        assert r.status_code == 402
        body = r.json()
        assert set(body.keys()) == {"x402Version", "error", "accepts"}
        _assert_strict_accepts(body["accepts"][0], pay_to="0x_accepts_strict")

        assert r.headers.get("payment-required") is None


def test_get_402_and_openapi_post_only(monkeypatch):
    _real_unpaid(monkeypatch)
    c = TestClient(app)
    assert c.get("/contracts/risk-score").status_code == 402
    get_a0 = c.get("/contracts/risk-score").json()["accepts"][0]
    assert get_a0["amount"] == "20000"
    assert "outputSchema" in get_a0

    paths = c.get("/openapi.json").json().get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score"]
    assert list(paths["/contracts/risk-score"].keys()) == ["post"]


def test_docs_twelfth_attempt_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_accepts_schema" in ol
    assert "twelfth" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3l" in pt or "3l)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "twelfth" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo


def test_env_unchanged_accepts_strict_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
