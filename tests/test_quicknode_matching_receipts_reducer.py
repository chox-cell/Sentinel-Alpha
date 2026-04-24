from services.scout_cell.event_reducer import reduce_quicknode_event


def test_matching_receipts_reducer_extracts_candidates():
    payload = {
        "matchingReceipts": [
            {
                "contractAddress": "0x1111111111111111111111111111111111111111",
                "transactionHash": "0xtx1",
                "blockNumber": 123,
                "from": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "to": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "logs": [
                    {
                        "address": "0x2222222222222222222222222222222222222222",
                        "transactionHash": "0xtxlog1",
                        "blockNumber": 123,
                        "topics": [
                            "0xddf252ad00000000000000000000000000000000000000000000000000000000"
                        ],
                    },
                    {
                        "address": "0x3333333333333333333333333333333333333333",
                        "topics": ["MintLiquidityEvent"],
                    },
                ],
            }
        ]
    }

    candidates = reduce_quicknode_event(payload)
    assert len(candidates) >= 3

    # first_liquidity should be prioritized ahead of new_token and contract_event.
    assert candidates[0]["event_type"] == "first_liquidity"
    event_types = [c["event_type"] for c in candidates]
    assert "new_token_candidate" in event_types
    assert "contract_event" in event_types

    first = candidates[0]
    assert first["context"]["source"] == "quicknode"
    assert "receipt_index" in first["context"]
    assert "log_index" in first["context"]
    assert "transaction_hash" in first["context"]
    assert "block_number" in first["context"]
    assert "topic0" in first["context"]
    assert "receipt_from" in first["context"]
    assert "receipt_to" in first["context"]
