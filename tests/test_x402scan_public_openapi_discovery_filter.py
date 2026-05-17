"""Public /openapi.json must not advertise internal/health/webhook paths (x402scan OpenAPI discovery)."""

from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def _openapi_paths(client: TestClient) -> dict:
    r = client.get("/openapi.json")
    assert r.status_code == 200
    return r.json().get("paths") or {}


def test_openapi_excludes_internal_health_and_webhooks():
    paths = _openapi_paths(TestClient(app))
    for path in paths:
        assert not path.startswith("/internal/"), path
        assert path != "/health", path
        assert not path.startswith("/webhooks/"), path
    assert "/webhooks/quicknode" not in paths
    assert "/webhooks/quicknode/health" not in paths


def test_openapi_includes_risk_score_post_only():
    paths = _openapi_paths(TestClient(app))
    assert list(paths.keys()) == ["/contracts/risk-score"]
    rs = paths.get("/contracts/risk-score")
    assert rs is not None
    assert list(rs.keys()) == ["post"]


def test_runtime_health_and_internal_still_work():
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json().get("ok") is True

    x402 = client.get("/internal/x402/status")
    assert x402.status_code == 200
    assert "payment_mode" in x402.json()


def test_risk_score_discovery_unchanged_after_openapi_filter(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0x_openapi_filter_probe")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    assert client.get("/contracts/risk-score").status_code == 402
    assert client.post("/contracts/risk-score", content=b"").status_code == 402


def test_docs_seventh_attempt_recorded_without_listing_success():
    ol = OUTREACH.read_text(encoding="utf-8").lower()
    assert "attempted_validation_failed_openapi_internal_resources" in ol
    assert "seventh" in ol
    pt = PACK.read_text(encoding="utf-8")
    assert "§3g" in pt or "3g)" in pt.lower()
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "seventh" in cl and "openapi" in cl
    combo = ol + cl + pt.lower()
    assert "listing_success_claim: true" not in combo
    assert "x402scan listing verified" not in combo
