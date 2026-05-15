"""POST /contracts/risk-score: unpaid probes return 402 before JSON validation (scanner / x402scan 422 avoidance)."""

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


def _lower(resp) -> dict[str, str]:
    return {str(k).lower(): str(v) for k, v in resp.headers.items()}


def _real_monkey(monkeypatch, wallet: str = "0x_post_empty_probe") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def test_post_unpaid_empty_raw_body_402(monkeypatch):
    _real_monkey(monkeypatch)
    client = TestClient(app)
    r = client.post("/contracts/risk-score", content=b"", headers={"Content-Type": "application/json"})
    assert r.status_code == 402
    h = _lower(r)
    assert h.get("payment-required")
    assert "payment-required" in (h.get("access-control-expose-headers") or "").lower()
    d = r.json()["detail"]
    assert d["x402Version"] == 1
    assert d["accepts"][0]["asset"] == BASE_MAINNET_USDC_CONTRACT


def test_post_unpaid_no_content_type_402(monkeypatch):
    _real_monkey(monkeypatch)
    r = TestClient(app).post("/contracts/risk-score", content=b"")
    assert r.status_code == 402


def test_post_unpaid_empty_json_object_402(monkeypatch):
    _real_monkey(monkeypatch)
    r = TestClient(app).post("/contracts/risk-score", json={})
    assert r.status_code == 402


def test_post_unpaid_missing_contract_returns_402_not_422(monkeypatch):
    _real_monkey(monkeypatch)
    r = TestClient(app).post("/contracts/risk-score", json={"chain": "base"})
    assert r.status_code == 402


def test_post_unpaid_text_plain_invalid_402(monkeypatch):
    _real_monkey(monkeypatch)
    r = TestClient(app).post(
        "/contracts/risk-score",
        content=b"not-json-at-all",
        headers={"Content-Type": "text/plain"},
    )
    assert r.status_code == 402


def test_post_unpaid_does_not_run_scoring(monkeypatch):
    _real_monkey(monkeypatch, wallet="0x_no_eval_post")
    calls: list[bool] = []

    def _no_eval(**_kw):
        calls.append(True)
        return {"response": {}, "outcome_record": None}

    monkeypatch.setattr(api_main, "evaluate_contract_with_meta", _no_eval)
    TestClient(app).post(
        "/contracts/risk-score",
        content=b"{}",
        headers={"Content-Type": "application/json"},
    )
    assert calls == []


def test_paid_real_malformed_json_still_422(monkeypatch):
    _real_monkey(monkeypatch)
    tx = "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    r = TestClient(app).post(
        "/contracts/risk-score",
        content=b"{not json",
        headers={"Content-Type": "application/json", "X402-PAYMENT": tx},
    )
    assert r.status_code == 422


def test_discovery_methods_remain(monkeypatch):
    _real_monkey(monkeypatch)
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xm")
    c = TestClient(app)
    assert c.get("/contracts/risk-score").status_code == 402
    assert c.head("/contracts/risk-score").status_code == 402
    assert c.options("/contracts/risk-score").status_code in (200, 204)
    assert c.patch("/contracts/risk-score").status_code == 402
    assert c.put("/contracts/risk-score").status_code == 402
    assert c.delete("/contracts/risk-score").status_code == 402


def test_docs_record_sixth_diagnosis_without_listing_claim():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_post_422" in ol
    assert "sixth" in ol
    pk = PACK.read_text(encoding="utf-8").lower()
    assert "§3f" in PACK.read_text(encoding="utf-8") or "3f)" in pk
    assert "422" in pk
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "sixth" in cl
    combo = OUTREACH.read_text(encoding="utf-8").lower() + cl
    assert "listing_success_claim: true" not in combo


def test_env_stable_post_empty_compat():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    _ = OUTREACH.read_bytes()
    _ = CLAIMS.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
