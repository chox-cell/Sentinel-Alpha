from services.x402.onchain_verifier import (
    BASE_USDC_ADDRESS,
    USDC_DECIMALS,
    get_onchain_verification_status,
    usdc_to_units,
    verify_usdc_transfer_tx,
)


def test_usdc_to_units():
    assert USDC_DECIMALS == 6
    assert usdc_to_units(0.02) == 20000


def test_verify_usdc_transfer_tx_disabled_by_default(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "false")
    result = verify_usdc_transfer_tx(
        tx_hash="0x" + ("a" * 64),
        expected_amount=0.02,
        treasury_wallet="0x" + ("b" * 40),
    )
    assert result == {"verified": False, "status": "onchain_verification_disabled"}


def test_verify_usdc_transfer_tx_requires_rpc_when_enabled(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    result = verify_usdc_transfer_tx(
        tx_hash="0x" + ("a" * 64),
        expected_amount=0.02,
        treasury_wallet="0x" + ("b" * 40),
    )
    assert result == {"verified": False, "status": "rpc_not_configured"}


def test_get_onchain_verification_status_no_secrets(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base-rpc.example")
    monkeypatch.setenv("X402_NETWORK", "base")
    status = get_onchain_verification_status()
    assert status["onchain_verify_enabled"] is True
    assert status["rpc_configured"] is True
    assert status["network"] == "base"
    assert status["base_usdc_address"] == BASE_USDC_ADDRESS
    assert "BASE_RPC_URL" not in status
