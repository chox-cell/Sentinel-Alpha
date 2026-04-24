# OUTCOME VERIFIER v0.1

Goal:
- Verify stored Outcome Memory predictions into local truth-like records for later Adaptive Phi training loops.

Implementation:
- `services/outcome_memory/verifier.py`
- `services/outcome_memory/outcome_states.py`
- `workers/outcome_verifier/run.py`
- output file: `logs/verified_outcomes.jsonl`

Required API:
- `verify_outcome(record: dict) -> dict`
- `verify_recent_outcomes(limit: int = 50) -> list`
- `classify_stub_outcome(record: dict) -> str`

Outcome States v0.1 constants:
- `RUGGED`
- `HONEYPOT`
- `PRIVILEGE_ABUSE`
- `LEGIT`
- `UNKNOWN`
- `SAFE_SO_FAR`
- `BLOCKED_HIGH_RISK`
- `EMERGENCY_RISK_CONFIRMED`
- `MISSED_RISK_CANDIDATE`

Stub verification rules:
- `BLOCK` and `score >= 85` -> `blocked_high_risk` with confidence `0.7`
- `EXIT_NOW` -> `emergency_risk_confirmed` with confidence `0.75`
- `ALLOW` and `threat_class == normal` -> `safe_so_far` with confidence `0.55`
- `ALLOW` and `threat_class != normal` -> `missed_risk_candidate` with confidence `0.65`
- else -> `unknown` with confidence `0.4`

Constraints:
- No public schema changes.
- Keep `/contracts/risk-score` unchanged.
