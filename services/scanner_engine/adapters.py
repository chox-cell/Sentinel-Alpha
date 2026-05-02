import os


def get_viem_readiness() -> dict:
    """Preparation-only readiness marker for future Viem integration."""
    configured = bool((os.getenv("BASE_RPC_URL") or "").strip())
    return {
        "adapter": "viem",
        "configured": configured,
        "status": "ready_for_integration" if configured else "not_configured",
    }


def get_whatsabi_readiness() -> dict:
    """Preparation-only readiness marker for future WhatsABI integration."""
    enabled = (os.getenv("SENTINEL_WHATSABI_ENABLED", "false") or "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    return {
        "adapter": "whatsabi",
        "configured": enabled,
        "status": "ready_for_integration" if enabled else "not_configured",
    }

