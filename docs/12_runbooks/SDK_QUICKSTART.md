# Python SDK Quickstart v0.1

## Install
The SDK client uses `requests` only.

## Client
Use `SentinelAlphaClient` from `sdk/python/client.py`.

```python
from sdk.python.client import SentinelAlphaClient

client = SentinelAlphaClient(base_url="http://127.0.0.1:8000", payment_signature="demo")
print(client.health())
print(client.manifest())
print(client.risk_score("0x1111111111111111111111111111111111111111", chain="base"))
```

## Methods
- `health() -> dict`
- `manifest() -> dict`
- `risk_score(contract_address, chain="base", context=None) -> dict`

## Error handling
The client raises `RuntimeError` for:
- request timeouts
- network/request failures
- non-200 responses
- non-JSON responses

## Compatibility
- Does not change API schema.
- Uses existing `/contracts/risk-score`, `/health`, and `/internal/manifest`.
