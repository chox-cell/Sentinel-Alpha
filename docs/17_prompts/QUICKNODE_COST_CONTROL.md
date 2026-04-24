# QUICKNODE COST / VOLUME CONTROL v0.1

Goal:
- Limit webhook ingestion and evaluation volume to control compute and logging cost.

Implementation:
- `shared/config/limits.py`
- `services/scout_cell/hunter.py`
- `GET /internal/ingestion/status`

Limits:
- `SENTINEL_MAX_CANDIDATES_PER_WEBHOOK` default 50
- `SENTINEL_MAX_EVALUATIONS_PER_WEBHOOK` default 10
- `SENTINEL_MAX_PAYLOAD_BYTES_WARN` default 500000
- `SENTINEL_MAX_PAYLOAD_BYTES_HARD` default 3000000

Rules:
- Cap candidate and evaluation counts per webhook.
- Warn on large payloads over warn threshold.
- Hard-stop and return ignored result over hard threshold.

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public response schema unchanged.
