# OUTCOME MEMORY v0.1

Goal:
- Record every non-cached Sentinel Alpha decision so future learning loops can update Adaptive Phi.

Implementation:
- `services/outcome_memory/memory.py`
- File storage: `logs/outcome_memory.jsonl`

Required API:
- `record_decision(record: dict) -> dict`
- `get_recent_decisions(limit: int = 50) -> list`

Required record fields:
- `trace_id`
- `contract_address`
- `chain`
- `score`
- `confidence`
- `action`
- `threat_class`
- `signals`
- `attestation`
- `created_at`

Integration rule:
- Record after response is built in `services/risk_service/service.py`.
- Do not write duplicate records for cache hits.

Constraints:
- No public schema changes.
- Keep `/contracts/risk-score` unchanged.
