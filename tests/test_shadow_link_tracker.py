from services.shadow_link_tracker.tracker import compute_shadow_link_score


def test_shadow_link_score_high_for_known_rug_deployer():
    score = compute_shadow_link_score(
        {
            "known_rug_deployer": True,
            "cluster_risk": "low",
            "owner_privileges": False,
        }
    )
    assert score >= 0.8


def test_shadow_link_score_lower_without_known_rug_flag():
    score = compute_shadow_link_score(
        {
            "known_rug_deployer": False,
            "cluster_risk": "low",
            "owner_privileges": False,
        }
    )
    assert score < 0.75
