"""PATCH/PUT/DELETE on `/contracts/risk-score` return discovery 402 (x402scan all-method probing)."""

import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api import main as api_main
from apps.api.main import app
from services.x402.payment import BASE_MAINNET_USDC_CONTRACT

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def _lower_headers(resp) -> dict[str, str]:
    return {str(k).lower(): str(v) for k, v in resp.headers.items()}


def _discovery_env(monkeypatch, *, wallet: str) -> None:
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def _assert_402_discovery_response(response, *, pay_to: str) -> dict:
    assert response.status_code == 402
    h = _lower_headers(response)
    assert h.get("payment-required") is None
    body = response.json()
    assert body["x402Version"] == 1
    assert body["asset"] == "USDC"
    assert body["pay_to"] == pay_to
    a0 = body["accepts"][0]
    assert a0["scheme"] == "exact"
    assert a0["payTo"] == pay_to
    assert a0["asset"] == BASE_MAINNET_USDC_CONTRACT
    return body


def test_patch_put_delete_return_402_with_payment_required(monkeypatch):
    wallet = "0x_all_method_payto"
    _discovery_env(monkeypatch, wallet=wallet)

    client = TestClient(app)
    for client_call in (
        lambda: client.patch("/contracts/risk-score"),
        lambda: client.put("/contracts/risk-score"),
        lambda: client.delete("/contracts/risk-score"),
    ):
        resp = client_call()
        _assert_402_discovery_response(resp, pay_to=wallet)


def test_patch_put_delete_without_contract_address_no_scoring(monkeypatch):
    wallet = "0x_no_contract_needed"
    _discovery_env(monkeypatch, wallet=wallet)

    calls: list[bool] = []

    def _no_eval(**_kw):
        calls.append(True)
        return {"response": {}, "outcome_record": None}

    monkeypatch.setattr(api_main, "evaluate_contract_with_meta", _no_eval)

    client = TestClient(app)
    for path, method in (("PATCH", client.patch), ("PUT", client.put), ("DELETE", client.delete)):
        r = method("/contracts/risk-score?ignored=1")
        assert r.status_code == 402, path
        _assert_402_discovery_response(r, pay_to=wallet)
    assert calls == []


def test_get_head_options_post_unpaid_unchanged(monkeypatch):
    wallet = "0x_regression_wallet"
    _discovery_env(monkeypatch, wallet=wallet)
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")

    client = TestClient(app)
    g = client.get("/contracts/risk-score")
    assert g.status_code == 402
    _assert_402_discovery_response(g, pay_to=wallet)

    hd = client.head("/contracts/risk-score")
    assert hd.status_code == 402
    assert hd.content == b""
    assert _lower_headers(hd).get("payment-required") is None

    assert client.options("/contracts/risk-score").status_code in (200, 204)

    pu = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "context": {},
        },
    )
    assert pu.status_code == 402


def test_openapi_does_not_list_patch_put_delete_on_risk_score():
    """include_in_schema=False on compatibility handlers keeps OpenAPI truthful (POST is the mutation API)."""
    from fastapi.openapi.utils import get_openapi

    schema = get_openapi(
        title=app.title,
        version="0",
        openapi_version="3.0.3",
        routes=app.routes,
    )
    paths = schema.get("paths") or {}
    rs = paths.get("/contracts/risk-score")
    assert rs is not None
    assert list(rs.keys()) == ["post"]


def test_docs_fifth_attempt_recorded_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_unsupported_methods" in ol
    assert "fifth" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3e" in pt or "3e)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "fifth" in cl and "unsupported" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo


def test_env_stable_for_all_method_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    _ = OUTREACH.read_bytes()
    _ = CLAIMS.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
