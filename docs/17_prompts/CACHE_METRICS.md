# CACHE METRICS v0.1

Goal:
- Record local cache hit/miss metrics to estimate cache impact and operational value.

Implementation:
- `services/cache/metrics.py`
- file storage: `logs/cache_metrics.json`

Required functions:
- `record_cache_hit(cache_key: str) -> None`
- `record_cache_miss(cache_key: str) -> None`
- `get_cache_metrics() -> dict`
- `reset_cache_metrics() -> None`

Required integration:
- In `services/risk_service/service.py`
  - cache hit -> `record_cache_hit(cache_key)`
  - cache miss -> `record_cache_miss(cache_key)`
- Add internal endpoint:
  - `GET /internal/cache-metrics`

Constraints:
- Do not change `/contracts/risk-score`
- Do not change public risk response schema
