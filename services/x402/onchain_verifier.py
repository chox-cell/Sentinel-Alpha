import os


BASE_USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDC_DECIMALS = 6


def usdc_to_units(amount: float) -> int:
    return int(round(float(amount) * (10 ** USDC_DECIMALS)))


def _is_valid_tx_hash(tx_hash: str) -> bool:
    value = (tx_hash or "").strip()
    if not value.startswith("0x") or len(value) != 66:
        return False
    return all(ch in "0123456789abcdefABCDEF" for ch in value[2:])


def _is_valid_wallet(wallet: str) -> bool:
    value = (wallet or "").strip()
    if not value.startswith("0x") or len(value) != 42:
        return False
    return all(ch in "0123456789abcdefABCDEF" for ch in value[2:])


def get_onchain_verification_status() -> dict:
    enabled = (os.getenv("X402_ONCHAIN_VERIFY", "false") or "false").strip().lower() in {"1", "true", "yes", "on"}
    rpc_url = (os.getenv("BASE_RPC_URL") or "").strip()
    network = (os.getenv("X402_NETWORK", "base") or "base").strip().lower() or "base"
    return {
        "onchain_verify_enabled": enabled,
        "rpc_configured": bool(rpc_url),
        "network": network,
        "base_usdc_address": BASE_USDC_ADDRESS,
        "usdc_decimals": USDC_DECIMALS,
    }


def verify_usdc_transfer_tx(tx_hash: str, expected_amount: float, treasury_wallet: str) -> dict:
    enabled = (os.getenv("X402_ONCHAIN_VERIFY", "false") or "false").strip().lower() in {"1", "true", "yes", "on"}
    if not enabled:
        return {"verified": False, "status": "onchain_verification_disabled"}

    if not _is_valid_tx_hash(tx_hash):
        return {"verified": False, "status": "invalid_tx_hash"}
    if not _is_valid_wallet(treasury_wallet):
        return {"verified": False, "status": "invalid_treasury_wallet"}
    if float(expected_amount) <= 0:
        return {"verified": False, "status": "invalid_expected_amount"}

    rpc_url = (os.getenv("BASE_RPC_URL") or "").strip()
    if not rpc_url:
        return {"verified": False, "status": "rpc_not_configured"}

    # v0.7 adapter-only behavior: wiring exists, live RPC verification not yet enabled.
    return {
        "verified": False,
        "status": "verification_adapter_not_implemented",
        "expected_amount_units": usdc_to_units(float(expected_amount)),
        "asset": BASE_USDC_ADDRESS,
    }
