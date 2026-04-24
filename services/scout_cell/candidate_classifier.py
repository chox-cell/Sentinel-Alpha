TRANSFER_TOPIC0_PREFIX = "0xddf252ad"
APPROVAL_TOPIC0_PREFIX = "0x8c5be1e5"


def classify_candidate(candidate: dict) -> dict:
    context = candidate.get("context") or {}
    topic0 = str(context.get("topic0") or "").lower()
    force_evaluate = bool(context.get("force_evaluate"))
    event_type = str(candidate.get("event_type") or "").lower()

    if event_type == "first_liquidity":
        return {
            "candidate_type": "first_liquidity",
            "priority_score": 100,
            "should_evaluate": True,
            "reason": "high_value_liquidity_signal",
        }

    if event_type == "new_token_candidate":
        return {
            "candidate_type": "new_token_candidate",
            "priority_score": 90,
            "should_evaluate": True,
            "reason": "new_contract_candidate",
        }

    if topic0.startswith(TRANSFER_TOPIC0_PREFIX):
        return {
            "candidate_type": "token_transfer",
            "priority_score": 40,
            "should_evaluate": force_evaluate,
            "reason": "transfer_event_skipped_without_force" if not force_evaluate else "forced_transfer_evaluation",
        }

    if topic0.startswith(APPROVAL_TOPIC0_PREFIX):
        return {
            "candidate_type": "approval",
            "priority_score": 20,
            "should_evaluate": False,
            "reason": "approval_event_low_signal",
        }

    return {
        "candidate_type": "unknown",
        "priority_score": 10,
        "should_evaluate": False,
        "reason": "unknown_low_signal",
    }
