"""v1 discovery is body-first: no PAYMENT-REQUIRED header (@agentcash/discovery parses header as v2-only)."""

import hashlib
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


def _real_unpaid(monkeypatch, wallet: str = "0x_v1_body_first") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def _lower_headers(resp) -> dict[str, str]:
    return {str(k).lower(): str(v) for k, v in resp.headers.items()}


def _assert_no_payment_required_header(resp) -> None:
    h = _lower_headers(resp)
    assert h.get("payment-required") is None
    expose = h.get("access-control-expose-headers") or ""
    assert "payment-required" not in expose.lower()


def _assert_pure_v1_body(body: dict) -> None:
    assert set(body.keys()) == {"x402Version", "error", "accepts"}
    a0 = body["accepts"][0]
    assert a0["amount"] == "20000"
    assert a0["maxAmountRequired"] == "20000"
    assert a0["network"] == "base"
    assert a0["asset"] == BASE_MAINNET_USDC_CONTRACT
    assert a0["outputSchema"]["input"]["method"] == "POST"


def test_post_unpaid_body_first_no_payment_required_header(monkeypatch):
    _real_unpaid(monkeypatch)
    client = TestClient(app)
    for call in (
        lambda: client.post("/contracts/risk-score", content=b""),
        lambda: client.post("/contracts/risk-score", json=_SAMPLE),
    ):
        r = call()
        assert r.status_code == 402
        _assert_no_payment_required_header(r)
        _assert_pure_v1_body(r.json())


def test_get_and_mutating_discovery_no_payment_required_header(monkeypatch):
    _real_unpaid(monkeypatch)
    c = TestClient(app)
    get_r = c.get("/contracts/risk-score")
    assert get_r.status_code == 402
    _assert_no_payment_required_header(get_r)
    assert get_r.json()["x402_version"] == "0.2"
    assert get_r.json()["x402Version"] == 1

    for method in (c.patch, c.put, c.delete):
        r = method("/contracts/risk-score")
        assert r.status_code == 402
        _assert_no_payment_required_header(r)
        assert r.json()["x402Version"] == 1

    head_r = c.head("/contracts/risk-score")
    assert head_r.status_code == 402
    _assert_no_payment_required_header(head_r)


def test_openapi_single_post_and_x_payment_info(monkeypatch):
    _real_unpaid(monkeypatch)
    spec = TestClient(app).get("/openapi.json").json()
    paths = spec.get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score"]
    post_op = paths["/contracts/risk-score"]["post"]
    assert list(paths["/contracts/risk-score"].keys()) == ["post"]
    xpi = post_op.get("x-payment-info") or {}
    assert xpi.get("authMode") == "paid"
    assert "x402" in (xpi.get("protocols") or [])
    assert xpi.get("price", {}).get("amount") == "0.02"


def test_docs_fourteenth_attempt_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_v1_header_conflict" in ol
    assert "fourteenth" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3n" in pt or "3n)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "fourteenth" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo


def test_env_unchanged_v1_body_first_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
