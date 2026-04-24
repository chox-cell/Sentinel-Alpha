from services.scout_cell.event_reducer import reduce_quicknode_event


def test_reduce_quicknode_event_extracts_candidates_from_logs():
    payload = {
        "transactionHash": "0xabc",
        "blockNumber": 123,
        "receipt": {
            "logs": [
                {"address": "0x1111111111111111111111111111111111111111", "topics": ["liquidity"]},
                {"address": "0x2222222222222222222222222222222222222222", "topics": ["token"]},
            ]
        },
    }

    candidates = reduce_quicknode_event(payload)
    assert len(candidates) == 2
    assert candidates[0]["chain"] == "base"
    assert candidates[0]["transaction_hash"] == "0xabc"
    assert candidates[0]["log_count"] == 2
    assert candidates[0]["event_type"] == "first_liquidity"
    assert candidates[1]["event_type"] == "new_token_candidate"


def test_reduce_quicknode_event_ignores_payload_without_useful_address():
    payload = {"receipt": {"logs": [{"address": "not-an-address"}]}}
    assert reduce_quicknode_event(payload) == []


def test_reduce_quicknode_event_caps_candidates_at_50():
    logs = [
        {"address": f"0x{i:040x}"}
        for i in range(1, 80)
    ]
    payload = {"logs": logs}

    candidates = reduce_quicknode_event(payload)
    assert len(candidates) == 50
