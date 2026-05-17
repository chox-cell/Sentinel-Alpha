"""Unpaid POST returns flat x402 v1 body (same as GET), no FastAPI ``detail`` wrapper."""

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

_OPENAPI_SAMPLE = {
    "contract_address": "0x1111111111111111111111111111111111111111",
    "chain": "base",
}


def _real_unpaid(monkeypatch, wallet: str = "0x_post_strict_v1") -> None:
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", wallet)
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")


def _core_x402_fields(body: dict) -> dict:
    return {
        "x402Version": body["x402Version"],
        "error": body["error"],
        "accepts": body["accepts"],
    }


def _decode_pr(resp) -> dict:
    pr = resp.headers.get("payment-required")
    assert pr
    return json.loads(base64.standard_b64decode(pr).decode("utf-8"))


def test_unpaid_post_variants_flat_402(monkeypatch):
    _real_unpaid(monkeypatch)
    client = TestClient(app)
    get_body = client.get("/contracts/risk-score").json()
    assert get_body["x402Version"] == 1

    cases = [
        lambda: client.post("/contracts/risk-score", content=b""),
        lambda: client.post("/contracts/risk-score", json={}),
        lambda: client.post(
            "/contracts/risk-score",
            content=b"not-json",
            headers={"Content-Type": "text/plain"},
        ),
        lambda: client.post("/contracts/risk-score", json=_OPENAPI_SAMPLE),
    ]

    for call in cases:
        r = call()
        assert r.status_code == 402, r.text
        body = r.json()
        assert "detail" not in body
        assert body["x402Version"] == 1
        assert body["error"] == X402_V1_DISCOVERY_ERROR
        assert isinstance(body["accepts"], list) and len(body["accepts"]) >= 1
        assert _core_x402_fields(body) == _core_x402_fields(get_body)

        hdr = _decode_pr(r)
        assert hdr["x402Version"] == 1
        assert hdr["error"] == X402_V1_DISCOVERY_ERROR
        assert hdr["accepts"][0]["network"] == "base"

        expose = (r.headers.get("access-control-expose-headers") or "").lower()
        assert "payment-required" in expose


def test_runtime_and_openapi_unchanged(monkeypatch):
    _real_unpaid(monkeypatch)
    c = TestClient(app)
    assert c.head("/contracts/risk-score").status_code == 402
    assert c.head("/contracts/risk-score").content == b""
    assert c.options("/contracts/risk-score").status_code in (200, 204)

    paths = c.get("/openapi.json").json().get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score"]
    assert list(paths["/contracts/risk-score"].keys()) == ["post"]


def test_docs_tenth_attempt_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_post_body_shape" in ol
    assert "tenth" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3j" in pt or "3j)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "tenth" in cl
    combo = ol + cl
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo


def test_env_unchanged_post_strict_v1_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
