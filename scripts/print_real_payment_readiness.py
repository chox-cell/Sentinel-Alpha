import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.x402.onchain_verifier import get_onchain_verification_status
from services.x402.payment_config import get_payment_status


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in {"1", "true", "yes", "on"}


def build_readiness_report() -> dict:
    payment_status = get_payment_status()
    onchain_status = get_onchain_verification_status()

    treasury_configured = bool(
        (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
        or (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    )
    x402_enabled = _env_bool("X402_ENABLED", default=False)

    readiness = (
        payment_status["payment_mode"] == "real"
        and x402_enabled
        and onchain_status["onchain_verify_enabled"]
        and onchain_status["rpc_configured"]
        and treasury_configured
        and payment_status["wallet_address_configured"]
        and payment_status["pricing_valid"]
    )

    return {
        "payment_mode": payment_status["payment_mode"],
        "x402_enabled": x402_enabled,
        "onchain_verify_enabled": onchain_status["onchain_verify_enabled"],
        "base_rpc_configured": onchain_status["rpc_configured"],
        "treasury_configured": treasury_configured,
        "wallet_address_configured": payment_status["wallet_address_configured"],
        "pricing_tiers": payment_status["pricing_tiers"],
        "readiness_verdict": "ready" if readiness else "not_ready",
    }


if __name__ == "__main__":
    print(json.dumps(build_readiness_report(), ensure_ascii=True, indent=2))
