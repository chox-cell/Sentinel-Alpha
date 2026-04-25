# Post Deployment Smoke Test v2.2

Run after deployment to verify public API availability via your real base URL.

## Required Env

- `PUBLIC_BASE_URL` must be set.

## Command

```bash
python3 scripts/public_smoke_test.py
```

## Checks

- `GET /health`
- `GET /internal/manifest`
- `GET /internal/x402/status`
- `GET /internal/x402/onchain/status`
- `GET /internal/x402/challenge?lane=basic`
- `POST /contracts/risk-score` without payment returns `402`

## Expected Result

- Final line prints `smoke test verdict: pass`.
- Script output contains status codes and pass/fail only; no secret values are printed.
