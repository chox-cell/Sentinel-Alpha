# Outcome Memory v0.1

## Purpose
Outcome Memory stores evaluated decisions so Sentinel Alpha can later learn from real outcomes and calibrate Adaptive Phi.

## Module
- `services/outcome_memory/memory.py`

## Functions
- `record_decision(record: dict) -> dict`
- `get_recent_decisions(limit: int = 50) -> list`

## Storage
- Local JSONL file: `logs/outcome_memory.jsonl`

## Record fields
Each record includes:
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

## Integration
- `services/risk_service/service.py` builds one outcome record for each non-cached evaluation.
- `apps/api/main.py` records that outcome through BackgroundTasks (Latency Shield v0.1).
- Cache hits return cached responses and do not create duplicate memory records.

## Constraints
- No public API schema changes.
- `/contracts/risk-score` remains unchanged.
