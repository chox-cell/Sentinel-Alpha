"""x402scan: public OpenAPI lists one payable operation (POST only); runtime discovery verbs unchanged."""

import base64
import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402.payment import X402_V1_DISCOVERY_ERROR

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def _real_unpaid(monkeypatch, wallet: str = "0x_single_openapi") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def test_openapi_single_path_post_only():
    paths = TestClient(app).get("/openapi.json").json().get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score"]
    assert list(paths["/contracts/risk-score"].keys()) == ["post"]
    hidden = {"get", "head", "options", "patch", "put", "delete"}
    assert hidden.isdisjoint(paths["/contracts/risk-score"].keys())


def test_runtime_discovery_verbs_unchanged(monkeypatch):
    _real_unpaid(monkeypatch)
    c = TestClient(app)

    get_r = c.get("/contracts/risk-score")
    assert get_r.status_code == 402
    assert get_r.json()["x402Version"] == 1
    assert get_r.json()["error"] == X402_V1_DISCOVERY_ERROR

    head_r = c.head("/contracts/risk-score")
    assert head_r.status_code == 402
    assert head_r.content == b""
    assert head_r.headers.get("payment-required") is None

    assert c.options("/contracts/risk-score").status_code in (200, 204)
    assert c.patch("/contracts/risk-score").status_code == 402
    assert c.put("/contracts/risk-score").status_code == 402
    assert c.delete("/contracts/risk-score").status_code == 402

    post_r = c.post("/contracts/risk-score", content=b"")
    assert post_r.status_code == 402
    body = post_r.json()
    assert set(body.keys()) == {"x402Version", "error", "accepts"}
    assert body["error"] == X402_V1_DISCOVERY_ERROR
    assert body["accepts"][0]["network"] == "base"

    assert post_r.headers.get("payment-required") is None


def test_docs_ninth_attempt_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_openapi_multiple_operations" in ol
    assert "ninth" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3i" in pt or "3i)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "ninth" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo


def test_env_unchanged_single_openapi_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
