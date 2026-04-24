# Cache Metrics v0.1

## Purpose
Track local cache efficiency and potential Redis profit impact without changing the public risk-score schema.

## Module
- `services/cache/metrics.py`

## Functions
- `record_cache_hit(cache_key: str) -> None`
- `record_cache_miss(cache_key: str) -> None`
- `get_cache_metrics() -> dict`
- `reset_cache_metrics() -> None`

## Storage
- `logs/cache_metrics.json`

## Integration
- `services/risk_service/service.py`
  - cache hit path records `record_cache_hit(cache_key)`
  - cache miss path records `record_cache_miss(cache_key)`
- `apps/api/main.py`
  - internal endpoint: `GET /internal/cache-metrics`

## Constraints
- No changes to `/contracts/risk-score`
- No public risk response schema changes
