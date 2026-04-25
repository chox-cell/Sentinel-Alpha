import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env", override=True)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def build_production_report() -> dict:
    app_env_production = (os.getenv("APP_ENV") or "").strip().lower() == "production"
    public_base_url_configured = bool((os.getenv("PUBLIC_BASE_URL") or "").strip())
    payment_mode_real = (os.getenv("PAYMENT_MODE") or "").strip().lower() == "real"
    x402_enabled = _env_bool("X402_ENABLED", default=False)
    mock_disabled = not _env_bool("X402_MOCK_ONCHAIN_VERIFY", default=False)
    onchain_enabled = _env_bool("X402_ONCHAIN_VERIFY", default=False)
    base_rpc_configured = bool((os.getenv("BASE_RPC_URL") or "").strip())
    quicknode_signature_required = _env_bool("QUICKNODE_SIGNATURE_REQUIRED", default=False)
    rate_limit_enabled = _env_bool("RATE_LIMIT_ENABLED", default=False)

    wallet_configured = bool((os.getenv("AGENT_WALLET_ADDRESS") or "").strip())
    treasury_configured = bool(
        (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
        or (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    )

    ready = all(
        [
            app_env_production,
            public_base_url_configured,
            payment_mode_real,
            x402_enabled,
            mock_disabled,
            onchain_enabled,
            base_rpc_configured,
            quicknode_signature_required,
            rate_limit_enabled,
            wallet_configured,
            treasury_configured,
        ]
    )

    return {
        "app_env_production": app_env_production,
        "public_base_url_configured": public_base_url_configured,
        "payment_mode_real": payment_mode_real,
        "x402_enabled": x402_enabled,
        "x402_mock_onchain_verify_disabled": mock_disabled,
        "x402_onchain_verify_enabled": onchain_enabled,
        "base_rpc_url_configured": base_rpc_configured,
        "quicknode_signature_required": quicknode_signature_required,
        "rate_limit_enabled": rate_limit_enabled,
        "wallet_configured": wallet_configured,
        "treasury_configured": treasury_configured,
        "production_ready": ready,
    }


def format_report(report: dict) -> str:
    return "\n".join(
        [
            "Sentinel Alpha Production Env Check v2.1",
            f"APP_ENV=production: {str(report['app_env_production']).lower()}",
            f"PUBLIC_BASE_URL configured: {str(report['public_base_url_configured']).lower()}",
            f"PAYMENT_MODE=real: {str(report['payment_mode_real']).lower()}",
            f"X402_ENABLED=true: {str(report['x402_enabled']).lower()}",
            f"X402_MOCK_ONCHAIN_VERIFY=false: {str(report['x402_mock_onchain_verify_disabled']).lower()}",
            f"X402_ONCHAIN_VERIFY=true: {str(report['x402_onchain_verify_enabled']).lower()}",
            f"BASE_RPC_URL configured: {str(report['base_rpc_url_configured']).lower()}",
            f"QUICKNODE_SIGNATURE_REQUIRED=true: {str(report['quicknode_signature_required']).lower()}",
            f"RATE_LIMIT_ENABLED=true: {str(report['rate_limit_enabled']).lower()}",
            f"wallet configured: {str(report['wallet_configured']).lower()}",
            f"treasury configured: {str(report['treasury_configured']).lower()}",
            f"production ready: {str(report['production_ready']).lower()}",
        ]
    )


def main() -> int:
    report = build_production_report()
    print(format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
