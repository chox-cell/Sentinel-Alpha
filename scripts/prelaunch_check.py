import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env", override=False)


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in {"1", "true", "yes", "on"}


def build_prelaunch_report() -> dict:
    payment_mode = (os.getenv("PAYMENT_MODE") or "demo").strip().lower() or "demo"
    x402_enabled = _env_bool("X402_ENABLED", default=False)
    mock_onchain_verify = _env_bool("X402_MOCK_ONCHAIN_VERIFY", default=False)

    base_rpc_configured = bool((os.getenv("BASE_RPC_URL") or "").strip())
    revenue_wallet = (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
    treasury_wallet = (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    agent_wallet = (os.getenv("AGENT_WALLET_ADDRESS") or "").strip()

    treasury_configured = bool(revenue_wallet or treasury_wallet)
    wallet_configured = bool(agent_wallet or revenue_wallet or treasury_wallet)

    agentic_market_exists = (ROOT / "agentic-market.json").exists()
    readme_exists = (ROOT / "README.md").exists()
    sdk_docs_exist = all(
        [
            (ROOT / "sdk/python/README.md").exists(),
            (ROOT / "sdk/typescript/README.md").exists(),
        ]
    )
    launch_docs_exist = all(
        [
            (ROOT / "docs/14_distribution/API_QUICKSTART.md").exists(),
            (ROOT / "docs/14_distribution/BOT_INTEGRATION_GUIDE.md").exists(),
            (ROOT / "docs/14_distribution/PRE_LAUNCH_CHECKLIST.md").exists(),
        ]
    )

    ready = all(
        [
            payment_mode == "real",
            x402_enabled,
            not mock_onchain_verify,
            base_rpc_configured,
            wallet_configured,
            treasury_configured,
            agentic_market_exists,
            readme_exists,
            sdk_docs_exist,
            launch_docs_exist,
        ]
    )

    return {
        "pytest_command_reminder": "python3 -m pytest tests/ -q --tb=no",
        "env_source": ".env",
        "payment_mode": payment_mode,
        "x402_enabled": x402_enabled,
        "x402_mock_onchain_verify_is_false": not mock_onchain_verify,
        "base_rpc_url_configured": base_rpc_configured,
        "wallet_configured": wallet_configured,
        "treasury_configured": treasury_configured,
        "agentic_market_json_exists": agentic_market_exists,
        "readme_exists": readme_exists,
        "sdk_docs_exist": sdk_docs_exist,
        "launch_docs_exist": launch_docs_exist,
        "readiness_verdict": "ready" if ready else "not_ready",
    }


def format_prelaunch_report(report: dict) -> str:
    return "\n".join(
        [
            "Sentinel Alpha Pre-launch Check v1.3",
            f"pytest command reminder: {report['pytest_command_reminder']}",
            f"env source: {report['env_source']}",
            f"PAYMENT_MODE: {report['payment_mode']}",
            f"X402_ENABLED: {str(report['x402_enabled']).lower()}",
            "X402_MOCK_ONCHAIN_VERIFY must be false: "
            f"{str(report['x402_mock_onchain_verify_is_false']).lower()}",
            f"BASE_RPC_URL configured: {str(report['base_rpc_url_configured']).lower()}",
            f"wallet configured: {str(report['wallet_configured']).lower()}",
            f"treasury configured: {str(report['treasury_configured']).lower()}",
            f"agentic-market.json exists: {str(report['agentic_market_json_exists']).lower()}",
            f"README exists: {str(report['readme_exists']).lower()}",
            f"SDK docs exist: {str(report['sdk_docs_exist']).lower()}",
            f"launch docs exist: {str(report['launch_docs_exist']).lower()}",
            f"readiness verdict: {report['readiness_verdict']}",
        ]
    )


def main() -> int:
    report = build_prelaunch_report()
    print(format_prelaunch_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
