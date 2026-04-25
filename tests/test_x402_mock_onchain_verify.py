from fastapi import HTTPException

from services.x402 import replay_guard, settlement_ledger
from services.x402.payment import require_x402_payment


def test_valid_mock_tx_returns_verified_billing(monkeypatch, tmp_path):
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", tmp_path / "x402_payments.jsonl")
    monkeypatch.setattr(settlement_ledger, "SETTLEMENT_LOG_PATH", tmp_path / "x402_settlements.jsonl")
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("X402_MOCK_ONCHAIN_VERIFY", "true")
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    monkeypatch.setenv("PRICE_BASIC", "0.02")

    billing = require_x402_payment(
        {"X402-PAYMENT": "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
        lane="basic",
    )
    assert billing["status"] == "verified"
    assert billing["method"] == "x402"
    assert billing["amount"] == "0.02"


def test_invalid_tx_still_fails(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("X402_MOCK_ONCHAIN_VERIFY", "true")

    try:
        require_x402_payment({"X402-PAYMENT": "tx:0x1234"}, lane="basic")
        assert False, "Expected HTTPException for invalid payment header"
    except HTTPException as exc:
        assert exc.status_code == 402
        assert exc.detail == {"error": "invalid_x402_payment"}
