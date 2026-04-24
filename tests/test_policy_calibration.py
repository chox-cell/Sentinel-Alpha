from services.risk_service import service


def test_shadow_link_alone_enforces_reduce_floor():
    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"known_rug_deployer": True, "event_type": "new_deploy"},
    )

    assert result["signals"]["shadow_link"] == 1
    assert result["risk_metrics"]["score"] >= 70
    assert result["decision"]["action"] in {"REDUCE", "BLOCK"}


def test_shadow_link_with_bad_cluster_enforces_block():
    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={
            "known_rug_deployer": True,
            "bad_cluster": True,
            "event_type": "new_deploy",
        },
    )

    assert result["signals"]["shadow_link"] == 1
    assert result["signals"]["bad_cluster"] == 1
    assert result["risk_metrics"]["score"] >= 85
    assert result["decision"]["action"] == "BLOCK"


def test_emergency_oracle_still_returns_exit_now():
    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={
            "known_rug_deployer": True,
            "bad_cluster": True,
            "oracle_dislocation": True,
            "event_type": "new_deploy",
        },
    )

    assert result["signals"]["shadow_link"] == 1
    assert result["signals"]["bad_cluster"] == 1
    assert result["signals"]["oracle_dislocation"] == 1
    assert result["decision"]["action"] == "EXIT_NOW"
