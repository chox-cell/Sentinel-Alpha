# SDK HARDENING v0.1

Goal:
- Provide a stable Python SDK for bots/agents to call Sentinel Alpha safely.

Implementation:
- `sdk/python/client.py`
- class: `SentinelAlphaClient`

Constructor:
- `SentinelAlphaClient(base_url: str, payment_signature: str = "demo")`

Methods:
- `risk_score(contract_address: str, chain: str = "base", context: dict | None = None) -> dict`
- `health() -> dict`
- `manifest() -> dict`

Error handling:
- timeout
- request failures
- non-200 response
- non-JSON response

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public risk response schema unchanged.
- Use only `requests` (no extra dependencies).
