import os

from shared.config.env import get_env_bool


def _registry_configured() -> bool:
    return bool((os.getenv("ERC8004_REGISTRY_ADDRESS") or "").strip())


def _agent_id_configured() -> bool:
    return bool((os.getenv("ERC8004_AGENT_ID") or "").strip())


def _derive_status(enabled: bool, registry: bool, agent_id: bool) -> str:
    """Offline-only status; does not assert on-chain registration or verification."""
    if not enabled:
        return "planned"
    if not registry and not agent_id:
        return "planned"
    if registry != agent_id:
        return "configured_not_registered"
    return "registered_unverified"


def get_erc8004_status() -> dict:
    enabled = get_env_bool("ERC8004_ENABLED", default=False)
    registry_configured = _registry_configured()
    agent_id_configured = _agent_id_configured()
    return {
        "enabled": enabled,
        "registry_configured": registry_configured,
        "agent_id_configured": agent_id_configured,
        "status": _derive_status(enabled, registry_configured, agent_id_configured),
    }


def build_agent_identity_payload() -> dict:
    st = get_erc8004_status()
    did = (os.getenv("SENTINEL_AGENT_DID") or "did:sentinel-alpha:local").strip() or "did:sentinel-alpha:local"
    return {
        "agent_name": "Sentinel Alpha",
        "engine_name": "Mycelium Engine",
        "agent_system": "Sentinel Cells",
        "primary_endpoint": "/contracts/risk-score",
        "identity_version": "identity-0.1",
        "did": did,
        "erc8004_adapter": {
            "enabled": st["enabled"],
            "status": st["status"],
            "registry_configured": st["registry_configured"],
            "agent_id_configured": st["agent_id_configured"],
            "chain_verification": "stub_offline",
        },
    }
