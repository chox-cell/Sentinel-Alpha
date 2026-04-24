import os


def _read_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        return float(raw)
    except (TypeError, ValueError):
        return default


def _is_cdp_key_configured() -> bool:
    key_name = (os.getenv("CDP_API_KEY_NAME") or "").strip()
    key_private = (os.getenv("CDP_API_KEY_PRIVATE_KEY") or "").strip()
    if key_name and key_private:
        return True

    key_id = (os.getenv("CDP_API_KEY_ID") or "").strip()
    key_secret = (os.getenv("CDP_API_KEY_SECRET") or "").strip()
    return bool(key_id and key_secret)


def _build_pricing_tiers() -> dict:
    return {
        "basic": _read_float("PRICE_BASIC", 0.02),
        "executive": _read_float("PRICE_EXECUTIVE", 0.05),
        "premium": _read_float("PRICE_PREMIUM", 0.10),
        "priority": _read_float("PRICE_PRIORITY", 0.15),
        "default": _read_float("X402_DEFAULT_PRICE_USDC", 0.05),
    }


def _pricing_valid(pricing: dict) -> bool:
    basic = pricing["basic"]
    executive = pricing["executive"]
    premium = pricing["premium"]
    priority = pricing["priority"]
    default = pricing["default"]

    if any(v <= 0 for v in [basic, executive, premium, priority, default]):
        return False
    return basic <= executive <= premium <= priority


def get_payment_status() -> dict:
    payment_mode = (os.getenv("PAYMENT_MODE") or "demo").strip().lower() or "demo"
    cdp_project = (os.getenv("CDP_PROJECT_ID") or "").strip()
    wallet_address = (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    network = (os.getenv("X402_NETWORK") or "base").strip().lower() or "base"
    pricing_tiers = _build_pricing_tiers()
    pricing_valid = _pricing_valid(pricing_tiers)

    cdp_project_configured = bool(cdp_project)
    cdp_api_key_configured = _is_cdp_key_configured()
    wallet_address_configured = bool(wallet_address)
    real_payments_enabled = (
        payment_mode == "real"
        and cdp_project_configured
        and cdp_api_key_configured
        and wallet_address_configured
        and pricing_valid
    )

    return {
        "payment_mode": "real" if payment_mode == "real" else "demo",
        "payment_method": "x402",
        "cdp_project_configured": cdp_project_configured,
        "cdp_api_key_configured": cdp_api_key_configured,
        "wallet_address_configured": wallet_address_configured,
        "network": network,
        "pricing_tiers": pricing_tiers,
        "pricing_valid": pricing_valid,
        "real_payments_enabled": real_payments_enabled,
    }


def get_pricing_tiers() -> dict:
    tiers = _build_pricing_tiers()
    return {
        "basic": tiers["basic"],
        "executive": tiers["executive"],
        "premium": tiers["premium"],
        "priority": tiers["priority"],
        "default": tiers["default"],
    }
