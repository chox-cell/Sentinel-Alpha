import os


def get_payment_status() -> dict:
    payment_mode = (os.getenv("PAYMENT_MODE") or "demo").strip().lower() or "demo"
    cdp_project = (os.getenv("CDP_PROJECT_ID") or "").strip()
    cdp_api_key_name = (os.getenv("CDP_API_KEY_NAME") or "").strip()
    cdp_api_key_private_key = (os.getenv("CDP_API_KEY_PRIVATE_KEY") or "").strip()
    wallet_address = (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    network = (os.getenv("X402_NETWORK") or "base").strip().lower() or "base"

    cdp_project_configured = bool(cdp_project)
    cdp_api_key_configured = bool(cdp_api_key_name) and bool(cdp_api_key_private_key)
    wallet_address_configured = bool(wallet_address)
    real_payments_enabled = (
        payment_mode == "real"
        and cdp_project_configured
        and cdp_api_key_configured
        and wallet_address_configured
    )

    return {
        "payment_mode": "real" if payment_mode == "real" else "demo",
        "payment_method": "x402",
        "cdp_project_configured": cdp_project_configured,
        "cdp_api_key_configured": cdp_api_key_configured,
        "wallet_address_configured": wallet_address_configured,
        "network": network,
        "real_payments_enabled": real_payments_enabled,
    }
