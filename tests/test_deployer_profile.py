from services.profiler.deployer_profile import build_deployer_profile


def test_profile_marks_cluster_risk_high_from_context():
    profile = build_deployer_profile(
        contract_address="0xABC",
        chain="BASE",
        context={"bad_cluster": True},
    )

    assert profile["cluster_risk"] == "high"
    assert profile["contract_address"] == "0xabc"
    assert profile["chain"] == "base"


def test_profile_owner_privileges_passthrough():
    profile = build_deployer_profile(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"owner_privileges": True},
    )

    assert profile["owner_privileges"] is True
