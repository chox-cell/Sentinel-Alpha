# Outcome Verifier v0.1

## Purpose
Outcome Verifier converts predicted decisions from Outcome Memory into local verified outcome records so Adaptive Phi can later learn from outcome truth signals.

## Module
- `services/outcome_memory/verifier.py`
- `services/outcome_memory/outcome_states.py`

## Functions
- `verify_outcome(record: dict) -> dict`
- `verify_recent_outcomes(limit: int = 50) -> list`
- `classify_stub_outcome(record: dict) -> str`

## Outcome States v0.1
Formal constants are defined in `outcome_states.py`:
- `RUGGED`
- `HONEYPOT`
- `PRIVILEGE_ABUSE`
- `LEGIT`
- `UNKNOWN`
- `SAFE_SO_FAR`
- `BLOCKED_HIGH_RISK`
- `EMERGENCY_RISK_CONFIRMED`
- `MISSED_RISK_CANDIDATE`

## Storage
- Verified outcomes file: `logs/verified_outcomes.jsonl`

## Verified record fields
- `original_trace_id`
- `contract_address`
- `chain`
- `predicted_score`
- `predicted_action`
- `threat_class`
- `signals`
- `actual_outcome`
- `verifier_confidence`
- `verified_at`

## Worker
- `workers/outcome_verifier/run.py`
- Reads recent outcome memory records and writes verified outcomes.

## Constraints
- No public API schema changes.
- No changes to `/contracts/risk-score`.
