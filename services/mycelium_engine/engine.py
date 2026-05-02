from typing import Dict

WEIGHTS = {
    "invalid_address": 100,
    "zero_address": 100,
    "unverified_address_shape": 25,
    "new_deploy": 15,
    "first_liquidity": 20,
    "owner_privileges": 25,
    "liquidity_unlocked": 30,
    "oracle_dislocation": 40,
    "simulation_revert": 45,
    "bad_cluster": 35,
    "shadow_link": 35,
    "bad_bot_activity": 20,
    "insufficient_data": 10,
}

def compute_score(signals: Dict[str, int]) -> int:
    score = 0

    for signal_name, signal_value in signals.items():
        score += WEIGHTS.get(signal_name, 0) * int(signal_value)

    score = max(0, min(100, score))

    # Policy Calibration v0.1: enforce score floors for shadow-link risk.
    if signals.get("shadow_link"):
        score = max(score, 70)
    if signals.get("shadow_link") and signals.get("bad_cluster"):
        score = max(score, 85)

    return score

def compute_confidence(signals: Dict[str, int]) -> float:
    if signals.get("invalid_address"):
        return 0.95
    if signals.get("zero_address"):
        return 0.92

    evidence = 0
    evidence += signals.get("new_deploy", 0)
    evidence += signals.get("first_liquidity", 0)
    evidence += signals.get("owner_privileges", 0)
    evidence += signals.get("liquidity_unlocked", 0)
    evidence += signals.get("oracle_dislocation", 0)
    evidence += signals.get("simulation_revert", 0)
    evidence += signals.get("bad_cluster", 0)
    evidence += signals.get("shadow_link", 0)
    evidence += signals.get("bad_bot_activity", 0)

    if signals.get("insufficient_data"):
        return 0.45

    if evidence >= 3:
        return 0.9
    if evidence == 2:
        return 0.75
    if evidence == 1:
        return 0.6

    return 0.5

def decide(score: int, confidence: float, signals: Dict[str, int]) -> str:
    if signals.get("oracle_dislocation") or signals.get("liquidity_unlocked"):
        if score >= 80:
            return "EXIT_NOW"

    if confidence < 0.5:
        return "REVIEW"

    if score >= 85:
        return "BLOCK"

    if score >= 65:
        return "REDUCE"

    return "ALLOW"

def classify_threat(signals: Dict[str, int]) -> str:
    if signals.get("invalid_address"):
        return "invalid_contract_address"
    if signals.get("zero_address"):
        return "invalid_contract_address"
    if signals.get("oracle_dislocation"):
        return "oracle_dislocation"
    if signals.get("liquidity_unlocked"):
        return "liquidity_rug"
    if signals.get("simulation_revert"):
        return "execution_drift"
    if signals.get("bad_cluster") or signals.get("shadow_link"):
        return "behavioral_launch_syndicate"
    if signals.get("owner_privileges"):
        return "privilege_rug"
    if signals.get("insufficient_data"):
        return "insufficient_data"
    return "normal"
