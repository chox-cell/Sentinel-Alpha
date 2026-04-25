# Sentinel Alpha Python SDK

Lightweight Python client for Sentinel Alpha.

## Install

Use this repository directly, or copy `sdk/python/client.py` into your project.

## Quickstart

```python
from sdk.python.client import SentinelAlphaClient

client = SentinelAlphaClient(
    base_url="http://localhost:8000",
    payment_header="tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
)

result = client.scan("0x1111111111111111111111111111111111111111", chain="base")
print(result)
```

## Client API

- `SentinelAlphaClient(base_url, payment_header=None, payment_signature="demo")`
- `scan(contract_address, chain="base", context=None)`
- `risk_score(contract_address, chain="base", context=None)` (alias for `scan`)
- `health()`
- `manifest()`

## Headers

- If `payment_header` is set, the client sends `X402-PAYMENT`.
- Otherwise it sends `PAYMENT-SIGNATURE` (default `demo`).
