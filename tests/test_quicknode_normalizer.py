from services.scout_cell.quicknode_normalizer import normalize_quicknode_payload


def test_normalize_contract_address_shape():
    payload = {"contract_address": "0xabc", "chain": "base"}
    result = normalize_quicknode_payload(payload)

    assert result["contract_address"] == "0xabc"
    assert result["chain"] == "base"
    assert result["event_type"] == "new_deploy"
    assert result["context"]["contract_address"] == "0xabc"


def test_normalize_address_alias_shape():
    payload = {"address": "0xdef", "chain": "BASE"}
    result = normalize_quicknode_payload(payload)

    assert result["contract_address"] == "0xdef"
    assert result["chain"] == "base"
    assert result["event_type"] == "new_deploy"
    assert result["context"]["address"] == "0xdef"


def test_normalize_event_type_shape():
    payload = {"event_type": "FIRST_LIQUIDITY", "contract_address": "0x123"}
    result = normalize_quicknode_payload(payload)

    assert result["contract_address"] == "0x123"
    assert result["chain"] == "base"
    assert result["event_type"] == "first_liquidity"
    assert result["context"]["event_type"] == "first_liquidity"


def test_normalize_nested_data_shape():
    payload = {"data": {"address": "0xaaa", "chain": "base", "event_type": "new_deploy"}}
    result = normalize_quicknode_payload(payload)

    assert result["contract_address"] == "0xaaa"
    assert result["chain"] == "base"
    assert result["event_type"] == "new_deploy"


def test_normalize_nested_event_shape():
    payload = {"event": {"contract_address": "0xbbb", "event_type": "liquidity_added"}}
    result = normalize_quicknode_payload(payload)

    assert result["contract_address"] == "0xbbb"
    assert result["chain"] == "base"
    assert result["event_type"] == "liquidity_added"
