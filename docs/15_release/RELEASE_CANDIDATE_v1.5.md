# Release Candidate v1.5

## Goal
Freeze Sentinel Alpha for external review before public launch, with deterministic smoke checks and release documentation.

## Scope

- Runtime endpoint contract remains unchanged.
- No `/contracts/risk-score` schema changes.
- No renames.

## Release Candidate Checks

- Core API live checks pass:
  - `GET /health`
  - `GET /internal/manifest`
  - `GET /internal/env/source`
  - `GET /internal/x402/status`
  - `GET /internal/x402/onchain/status`
  - `GET /internal/x402/challenge?lane=basic`
- Guard check:
  - `POST /contracts/risk-score` without payment returns `402`

## Script

- `scripts/smoke_test.py`
- Run:

```bash
python3 scripts/smoke_test.py
```

## Security

- Smoke output is secret-safe.
- Script reports status booleans/status codes only.
