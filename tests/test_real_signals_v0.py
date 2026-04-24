from services.signals.extractor import extract_signals


def test_extract_signals_flags_invalid_evm_address():
    result = extract_signals(contract_address="0x123", chain="base", context={})
    signals = result["signals"]

    assert signals["invalid_address"] == 1
    assert signals["unverified_address_shape"] == 1


def test_extract_signals_sets_insufficient_data_without_evidence():
    result = extract_signals(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={},
    )
    signals = result["signals"]

    assert signals["insufficient_data"] == 1
    assert signals["new_deploy"] == 0
    assert signals["first_liquidity"] == 0


def test_extract_signals_applies_bytecode_stub_findings():
    result = extract_signals(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"owner_privileges_detected": True},
    )
    signals = result["signals"]

    assert signals["owner_privileges"] == 1
    assert signals["insufficient_data"] == 0
