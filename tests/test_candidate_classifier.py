from services.scout_cell.candidate_classifier import classify_candidate


def test_classify_first_liquidity():
    result = classify_candidate({"event_type": "first_liquidity", "context": {}})
    assert result["candidate_type"] == "first_liquidity"
    assert result["priority_score"] == 100
    assert result["should_evaluate"] is True


def test_classify_new_token_candidate():
    result = classify_candidate({"event_type": "new_token_candidate", "context": {}})
    assert result["candidate_type"] == "new_token_candidate"
    assert result["priority_score"] == 90
    assert result["should_evaluate"] is True


def test_classify_transfer_skips_without_force():
    result = classify_candidate(
        {
            "event_type": "contract_event",
            "context": {"topic0": "0xddf252ad00000000000000000000000000000000000000000000000000000000"},
        }
    )
    assert result["candidate_type"] == "token_transfer"
    assert result["priority_score"] == 40
    assert result["should_evaluate"] is False


def test_classify_approval_skips():
    result = classify_candidate(
        {
            "event_type": "contract_event",
            "context": {"topic0": "0x8c5be1e500000000000000000000000000000000000000000000000000000000"},
        }
    )
    assert result["candidate_type"] == "approval"
    assert result["priority_score"] == 20
    assert result["should_evaluate"] is False
