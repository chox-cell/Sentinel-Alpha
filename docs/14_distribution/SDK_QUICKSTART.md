# SDK Quickstart Pack v1.1

## Goal
Help bot builders integrate Sentinel Alpha quickly with minimal client code and no runtime behavior changes.

## Python

- Client: `sdk/python/client.py`
- Guide: `sdk/python/README.md`
- Example: `sdk/python/examples/paid_scan.py`

Supported constructor and method:
- `SentinelAlphaClient(base_url, payment_header=None, payment_signature="demo")`
- `scan(contract_address, chain="base")`

## TypeScript

- Client stub: `sdk/typescript/client.ts`
- Guide: `sdk/typescript/README.md`

Supported constructor and method:
- `new SentinelAlphaClient(baseUrl, paymentHeader?)`
- `scan(contractAddress, chain="base")`

## Safety

- No secrets are committed.
- `/contracts/risk-score` is unchanged.
- Public response schema is unchanged.
