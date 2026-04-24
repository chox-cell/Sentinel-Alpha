from services.outcome_memory import outcome_states
from services.outcome_memory.verifier import classify_stub_outcome


def test_outcome_state_constants_defined():
    assert outcome_states.RUGGED == "rugged"
    assert outcome_states.HONEYPOT == "honeypot"
    assert outcome_states.PRIVILEGE_ABUSE == "privilege_abuse"
    assert outcome_states.LEGIT == "legit"
    assert outcome_states.UNKNOWN == "unknown"
    assert outcome_states.SAFE_SO_FAR == "safe_so_far"
    assert outcome_states.BLOCKED_HIGH_RISK == "blocked_high_risk"
    assert outcome_states.EMERGENCY_RISK_CONFIRMED == "emergency_risk_confirmed"
    assert outcome_states.MISSED_RISK_CANDIDATE == "missed_risk_candidate"


def test_classify_stub_outcome_branches():
    assert classify_stub_outcome({"action": "BLOCK", "score": 85}) == outcome_states.BLOCKED_HIGH_RISK
    assert classify_stub_outcome({"action": "EXIT_NOW", "score": 10}) == outcome_states.EMERGENCY_RISK_CONFIRMED
    assert classify_stub_outcome({"action": "ALLOW", "threat_class": "normal"}) == outcome_states.SAFE_SO_FAR
    assert classify_stub_outcome({"action": "ALLOW", "threat_class": "oracle_dislocation"}) == outcome_states.MISSED_RISK_CANDIDATE
    assert classify_stub_outcome({"action": "REDUCE", "score": 10}) == outcome_states.UNKNOWN
