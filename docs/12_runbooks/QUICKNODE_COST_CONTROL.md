# QuickNode Cost / Volume Control v0.1

## Purpose
Protect Sentinel Alpha ingestion from high-volume delivery spikes, excessive evaluations, and log/cost explosion.

## Configured limits (env-backed)
- `SENTINEL_MAX_CANDIDATES_PER_WEBHOOK` (default: `50`)
- `SENTINEL_MAX_EVALUATIONS_PER_WEBHOOK` (default: `10`)
- `SENTINEL_MAX_PAYLOAD_BYTES_WARN` (default: `500000`)
- `SENTINEL_MAX_PAYLOAD_BYTES_HARD` (default: `3000000`)

## Behavior
- Candidate list is capped by max-candidates limit.
- Evaluations per webhook are capped by max-evaluations limit.
- Warn threshold triggers safe `cost_warning` log.
- Hard threshold returns ignored result and skips evaluation.

## Internal status endpoint
- `GET /internal/ingestion/status`
- returns current limits only (no secrets).

## Safety constraints
- `/contracts/risk-score` unchanged.
- Public response schema unchanged.
