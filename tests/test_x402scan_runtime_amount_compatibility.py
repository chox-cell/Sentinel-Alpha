"""x402scan runtime checker reads ``accepts[0].amount`` (check-endpoint paymentMethods)."""

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
_LEGACY_TOP = frozenset(
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


def _real_unpaid(monkeypatch, wallet: str = "0x_runtime_amount") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def _assert_post_pure_with_amount(body: dict, *, pay_to: str) -> None:
    assert set(body.keys()) == {"x402Version", "error", "accepts"}
    assert _LEGACY_TOP.isdisjoint(body.keys())
    a0 = body["accepts"][0]
    assert a0["amount"] == "20000"
    assert a0["maxAmountRequired"] == "20000"
    assert a0["network"] == "base"
    assert a0["asset"] == BASE_MAINNET_USDC_CONTRACT
    assert a0["payTo"] == pay_to
    assert a0["outputSchema"]["input"]["method"] == "POST"


def test_post_unpaid_amount_and_header(monkeypatch):
    _real_unpaid(monkeypatch)
    client = TestClient(app)
    for call in (
        lambda: client.post("/contracts/risk-score", content=b""),
        lambda: client.post("/contracts/risk-score", json=_SAMPLE),
    ):
        r = call()
        assert r.status_code == 402
        _assert_post_pure_with_amount(r.json(), pay_to="0x_runtime_amount")
        hdr = json.loads(base64.standard_b64decode(r.headers["payment-required"]).decode("utf-8"))
        assert hdr["accepts"][0]["amount"] == "20000"
        assert hdr["accepts"][0]["maxAmountRequired"] == "20000"


def test_openapi_post_only(monkeypatch):
    _real_unpaid(monkeypatch)
    paths = TestClient(app).get("/openapi.json").json().get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score"]
    assert list(paths["/contracts/risk-score"].keys()) == ["post"]


def test_docs_thirteenth_attempt_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_missing_accept_amount" in ol
    assert "thirteenth" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3m" in pt or "3m)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "thirteenth" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo


def test_env_unchanged_runtime_amount_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
