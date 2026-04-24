def compute_shadow_link_score(profile: dict) -> float:
    """
    Shadow Link Tracker v0.1

    Stub scoring rules:
    - known_rug_deployer=True -> score >= 0.8
    - cluster_risk=high increases baseline risk
    - owner_privileges adds incremental risk
    """
    profile = profile or {}

    if profile.get("known_rug_deployer"):
        return 0.85

    score = 0.1
    if profile.get("cluster_risk") == "high":
        score += 0.4
    if profile.get("owner_privileges"):
        score += 0.15

    return min(1.0, score)
