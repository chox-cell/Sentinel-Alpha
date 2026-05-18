"""Public growth endpoints: /public/status and /public/metrics."""

import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from services.growth.public_usage_metrics import reset_public_usage_metrics

REPO_ROOT = Path(__file__).resolve().parents[1]
FUNNEL = REPO_ROOT / "docs/17_growth/REVENUE_FUNNEL.md"
COPY_BLOCKS = REPO_ROOT / "docs/17_growth/API_INTEGRATION_COPY_BLOCKS.md"
AGENTIC = REPO_ROOT / "docs/17_growth/AGENTIC_MARKET_SUBMISSION_PACK.md"


def test_public_status_shape():
    reset_public_usage_metrics()
    client = TestClient(app)
    r = client.get("/public/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "BeezShield Sentinel Alpha"
    assert body["api_status"] == "live"
    assert body["x402_resource"] == "/contracts/risk-score"
    assert body["x402scan_registered"] is True
    assert body["payment_network"] == "base"
    assert body["asset"] == "USDC"
    assert body["basic_lane_amount_usdc"] == "0.02"
    assert body["no_guarantee"] is True
    text = r.text.lower()
    assert "app_env" not in text
    assert "cdp_" not in text
    assert "private_key" not in text


def test_public_metrics_increments_on_discovery_and_paid(monkeypatch):
    from apps.api import main

    reset_public_usage_metrics()
    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)

    client = TestClient(app)
    m0 = client.get("/public/metrics").json()
    assert m0["unpaid_discovery_402_count"] == 0
    assert m0["paid_request_count"] == 0

    assert client.get("/contracts/risk-score").status_code == 402
    m1 = client.get("/public/metrics").json()
    assert m1["unpaid_discovery_402_count"] >= 1
    assert m1["paid_request_count"] == 0
    assert m1["last_updated"] is not None
    assert m1["scope"] == "process_lifetime"

    paid = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
        },
        headers={"PAYMENT-SIGNATURE": "demo"},
    )
    assert paid.status_code == 200
    m2 = client.get("/public/metrics").json()
    assert m2["paid_request_count"] >= 1


def test_public_endpoints_excluded_from_filtered_openapi():
    paths = TestClient(app).get("/openapi.json").json().get("paths") or {}
    assert "/public/status" not in paths
    assert "/public/metrics" not in paths
    assert list(paths.keys()) == ["/contracts/risk-score"]


def test_growth_docs_exist():
    assert FUNNEL.exists()
    funnel = FUNNEL.read_text(encoding="utf-8").lower()
    assert "discovery" in funnel
    assert "do not claim" in funnel
    assert "agentic.market" in funnel

    assert COPY_BLOCKS.exists()
    blocks = COPY_BLOCKS.read_text(encoding="utf-8")
    assert "agent builders" in blocks.lower()
    assert "wallet automation" in blocks.lower()
    assert "x402 ecosystem" in blocks.lower()

    agentic = AGENTIC.read_text(encoding="utf-8").lower()
    assert "prepared_not_submitted" in agentic
    assert "submitted_pending" in agentic
    assert "listed_verified" in agentic
    assert "rejected_needs_fix" in agentic


def test_env_unchanged_public_growth():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = TestClient(app).get("/public/status").json()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
