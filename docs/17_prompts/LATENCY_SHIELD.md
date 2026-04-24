# LATENCY SHIELD v0.1

Goal:
- Reduce request-path latency by moving safe side effects to FastAPI BackgroundTasks.

Implementation targets:
- `apps/api/main.py`
- `services/risk_service/service.py`
- `services/latency_shield/background.py`

Rules:
- Keep `/contracts/risk-score` response schema unchanged.
- Compute and return risk response immediately.
- Schedule non-critical tasks in background:
  - request logging
  - outcome memory persistence (only for non-cached evaluations)
- Cache hits must not create duplicate outcome records.

Constraints:
- No renames.
- No changes to `/contracts/risk-score`.
