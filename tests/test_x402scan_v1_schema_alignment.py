"""x402scan v1 discovery schema: top-level error, accepts network ``base``, legacy CAIP-2 network preserved."""

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


def _real_unpaid(monkeypatch, wallet: str = "0x_v1_schema") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def test_get_402_v1_top_level_schema(monkeypatch):
    _real_unpaid(monkeypatch)
    client = TestClient(app)
    r = client.get("/contracts/risk-score")
    assert r.status_code == 402

    body = r.json()
    assert body["x402Version"] == 1
    assert body["error"] == X402_V1_DISCOVERY_ERROR
    assert isinstance(body["accepts"], list) and len(body["accepts"]) == 1
    assert body["network"] == "eip155:8453"

    a0 = body["accepts"][0]
    assert a0["network"] == "base"
    assert a0["asset"] == BASE_MAINNET_USDC_CONTRACT
    assert a0["maxAmountRequired"] == "20000"
    assert a0["payTo"] == "0x_v1_schema"
    assert a0["maxTimeoutSeconds"] == 60
    assert a0["extra"]["name"] == "USD Coin"
    assert a0["extra"]["version"] == "2"

    assert r.headers.get("payment-required") is None


def test_post_unpaid_pure_v1_no_legacy_keys(monkeypatch):
    _real_unpaid(monkeypatch, wallet="0x_v1_post")
    r = TestClient(app).post("/contracts/risk-score", content=b"")
    assert r.status_code == 402
    body = r.json()
    assert set(body.keys()) == {"x402Version", "error", "accepts"}
    assert body["error"] == X402_V1_DISCOVERY_ERROR


def test_head_options_patch_put_delete_and_openapi_unchanged(monkeypatch):
    _real_unpaid(monkeypatch)
    c = TestClient(app)
    head = c.head("/contracts/risk-score")
    assert head.status_code == 402
    assert head.content == b""
    assert head.headers.get("payment-required") is None

    assert c.options("/contracts/risk-score").status_code in (200, 204)
    assert c.patch("/contracts/risk-score").status_code == 402
    assert c.put("/contracts/risk-score").status_code == 402
    assert c.delete("/contracts/risk-score").status_code == 402

    paths = c.get("/openapi.json").json().get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score"]
    assert list(paths["/contracts/risk-score"].keys()) == ["post"]


def test_docs_eighth_attempt_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_x402scan_v1_schema" in ol
    assert "eighth" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3h" in pt or "3h)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "eighth" in cl and "v1" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo


def test_env_unchanged_v1_schema_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
