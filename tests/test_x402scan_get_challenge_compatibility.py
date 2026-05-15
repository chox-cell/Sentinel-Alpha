import base64
import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api import main as api_main
from apps.api.main import app
from services.x402.payment import BASE_MAINNET_USDC_CONTRACT

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def _challenge_assertions(body: dict, *, pay_to: str, resource_url: str = "https://api.beezshield.com/contracts/risk-score") -> None:
    assert body["x402_version"] == "0.2"
    assert body["payment_method"] == "x402"
    assert body["network"] == "eip155:8453"
    assert body["pay_to"] == pay_to
    assert body["amount_usdc"] == "0.02"
    assert body["asset"] == "USDC"
    assert body["resource"] == "/contracts/risk-score"
    assert body["instructions"] == "Submit X402-PAYMENT header to access this resource."
    assert body["lane"] == "basic"
    assert body["x402Version"] == 1
    assert isinstance(body["accepts"], list) and len(body["accepts"]) == 1
    a0 = body["accepts"][0]
    assert a0["scheme"] == "exact"
    assert a0["network"] == "eip155:8453"
    assert a0["maxAmountRequired"] == "20000"
    assert a0["amount"] == "20000"
    assert a0["payTo"] == pay_to
    assert a0["asset"] == BASE_MAINNET_USDC_CONTRACT
    assert a0["resource"] == resource_url
    assert a0["mimeType"] == "application/json"
    assert a0["maxTimeoutSeconds"] == 60
    assert a0["extra"] == {"name": "USDC", "version": "2"}


def test_get_contracts_risk_score_returns_402_x402_challenge(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xwallet_get_test")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    response = client.get("/contracts/risk-score")
    assert response.status_code == 402
    assert response.headers.get("payment-required")
    expose = response.headers.get("access-control-expose-headers", "")
    assert "payment-required".lower() in expose.lower()

    body = response.json()
    _challenge_assertions(body, pay_to="0xwallet_get_test")

    hdr = response.headers["payment-required"]
    dec = json.loads(base64.standard_b64decode(hdr).decode("utf-8"))
    assert dec["x402Version"] == 1
    assert dec["accepts"][0]["maxAmountRequired"] == "20000"


def test_get_does_not_require_contract_address_or_run_scoring(monkeypatch):
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xwallet_get_test")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    calls: list = []

    def _no_eval(**_kwargs):
        calls.append(True)
        return {"response": {}, "outcome_record": None}

    monkeypatch.setattr(api_main, "evaluate_contract_with_meta", _no_eval)

    client = TestClient(app)
    response = client.get("/contracts/risk-score")
    assert response.status_code == 402
    assert calls == []


def test_post_without_payment_still_returns_402_challenge(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xpost_wallet")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")

    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "context": {},
        },
    )
    assert response.status_code == 402
    detail = response.json()["detail"]
    assert detail["payment_method"] == "x402"
    assert detail["network"] == "eip155:8453"
    assert detail["resource"] == "/contracts/risk-score"
    assert detail["lane"] == "basic"
    assert detail["x402Version"] == 1
    assert detail["accepts"][0]["scheme"] == "exact"
    assert response.headers.get("payment-required")
    expose = response.headers.get("access-control-expose-headers", "")
    assert "payment-required".lower() in expose.lower()


def test_outreach_and_claims_record_x402scan_attempt_without_success_claim():
    ot = OUTREACH.read_text(encoding="utf-8").lower()
    assert "x402scan" in ot
    assert "attempted_validation_failed" in ot
    assert "expected 402" in ot or "402" in ot
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "x402scan registration attempt" in cl
    assert "fourth" in cl or "requirements schema" in cl
    assert "attempted_validation_failed_requirements_schema" in ot
    assert "attempted_validation_failed_schema" in ot
    assert "validation failed" in cl
    assert "no listing" in cl or "no listing claim" in cl


def test_submission_pack_notes_x402scan_expects_402_on_probe():
    pack = PACK.read_text(encoding="utf-8").lower()
    assert "x402scan" in pack
    assert "402" in pack
    assert "get" in pack


def test_env_hash_unchanged_during_x402scan_compatibility_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PACK.read_bytes()
    _ = OUTREACH.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
