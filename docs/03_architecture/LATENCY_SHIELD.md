# Latency Shield v0.1

## Purpose
Move non-critical side effects out of the request critical path using FastAPI background tasks while preserving response schema and endpoint behavior.

## Scope
- `/contracts/risk-score` schedules non-critical work after response build.
- Core risk computation remains synchronous and deterministic.

## Implementation
- `apps/api/main.py`
  - accepts `BackgroundTasks` in `risk_score`
  - schedules `log_event(...)` and `record_decision(...)` post-response
- `services/risk_service/service.py`
  - `evaluate_contract(...)` remains the primary deterministic evaluator
  - `evaluate_contract_with_meta(...)` returns response plus internal side-effect metadata
- `services/latency_shield/background.py`
  - helper to schedule safe post-response tasks

## Cache Safety
- Cache hits do not generate new outcome records.
- Non-cached evaluations produce an `outcome_record` that is persisted in background.

## Constraints
- No public response schema changes.
- No changes to `/contracts/risk-score`.
