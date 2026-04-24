from services.risk_service import service


def test_extract_maps_known_rug_deployer_to_shadow_link_signal():
    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"known_rug_deployer": True, "event_type": "new_deploy"},
    )
    assert result["signals"]["shadow_link"] == 1


def test_extract_maps_bad_cluster_to_bad_cluster_signal():
    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"bad_cluster": True, "event_type": "new_deploy"},
    )
    assert result["signals"]["bad_cluster"] == 1
