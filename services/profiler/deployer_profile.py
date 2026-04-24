from services.signals.validators import normalize_address, normalize_chain


def build_deployer_profile(contract_address, chain, context=None) -> dict:
    """
    Deployer Profile Stub v0.1

    Returns deterministic profile placeholders sourced from context so Signal Cell
    can evolve incrementally without public schema changes.
    """
    context = context or {}

    cluster_risk = "high" if bool(context.get("bad_cluster")) else "low"
    owner_privileges = bool(
        context.get("owner_privileges")
        or context.get("owner_privileges_detected")
    )

    return {
        "profile_version": "deployer-profile-stub-v0.1",
        "contract_address": normalize_address(contract_address),
        "chain": normalize_chain(chain),
        "cluster_risk": cluster_risk,
        "owner_privileges": owner_privileges,
        "known_rug_deployer": bool(context.get("known_rug_deployer")),
    }
