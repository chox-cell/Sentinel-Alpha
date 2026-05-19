"""OpenAPI: x402scan default vs Bazaar v2 dedicated schema."""

from fastapi.testclient import TestClient

from apps.api.main import app


def test_default_openapi_still_risk_score_v1_post_only():
    paths = TestClient(app).get("/openapi.json").json().get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score"]
    assert list(paths["/contracts/risk-score"].keys()) == ["post"]
    assert "/contracts/risk-score-v2" not in paths


def test_bazaar_openapi_lists_v2_post_only():
    spec = TestClient(app).get("/openapi.bazaar.json").json()
    paths = spec.get("paths") or {}
    assert list(paths.keys()) == ["/contracts/risk-score-v2"]
    post = paths["/contracts/risk-score-v2"]["post"]
    assert post["operationId"] == "risk_score_v2"
    xpi = post.get("x-payment-info") or {}
    assert xpi.get("authMode") == "paid"
    assert xpi.get("protocols") == ["x402"]
    assert xpi.get("price") == {"amount": "0.02", "currency": "USDC"}
