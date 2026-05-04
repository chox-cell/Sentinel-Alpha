import json
import os
import sys
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.x402.onchain_verifier import get_onchain_verification_status
from services.x402.payment_config import get_payment_status


def _parse_dotenv(path: Path) -> dict[str, str]:
    parsed: dict[str, str] = {}
    if not path.exists():
        return parsed
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _effective_env() -> dict[str, str]:
    # .env is the source of truth for this readiness report.
    env = dict(os.environ)
    env.update(_parse_dotenv(ROOT / ".env"))
    return env


@contextmanager
def _patched_environ(overrides: dict[str, str]):
    original = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(overrides)
        yield
    finally:
        os.environ.clear()
        os.environ.update(original)


def _env_bool(env: dict[str, str], name: str, default: bool = False) -> bool:
    raw = env.get(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in {"1", "true", "yes", "on"}


def build_readiness_report() -> dict:
    env = _effective_env()

    with _patched_environ(env):
        payment_status = get_payment_status()
        onchain_status = get_onchain_verification_status()

    revenue_wallet = (env.get("X402_REVENUE_ADDRESS") or "").strip()
    treasury_wallet = (env.get("SENTINEL_TREASURY_WALLET") or "").strip()
    agent_wallet = (env.get("AGENT_WALLET_ADDRESS") or "").strip()

    treasury_configured = bool(
        revenue_wallet or treasury_wallet
    )
    wallet_address_configured = bool(agent_wallet or treasury_wallet or revenue_wallet)
    x402_enabled = _env_bool(env, "X402_ENABLED", default=False)

    readiness = (
        payment_status["payment_mode"] == "real"
        and x402_enabled
        and onchain_status["onchain_verify_enabled"]
        and onchain_status["rpc_configured"]
        and treasury_configured
        and wallet_address_configured
        and payment_status["pricing_valid"]
    )

    return {
        "env_source": ".env",
        "payment_mode": payment_status["payment_mode"],
        "x402_enabled": x402_enabled,
        "onchain_verify_enabled": onchain_status["onchain_verify_enabled"],
        "base_rpc_configured": onchain_status["rpc_configured"],
        "treasury_configured": treasury_configured,
        "wallet_address_configured": wallet_address_configured,
        "pricing_tiers": payment_status["pricing_tiers"],
        "readiness_verdict": "ready" if readiness else "not_ready",
    }


if __name__ == "__main__":
    print(json.dumps(build_readiness_report(), ensure_ascii=True, indent=2))
