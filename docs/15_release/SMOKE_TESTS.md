# Smoke Tests v1.5

## Command

```bash
python3 scripts/smoke_test.py
```

## Covered Endpoints

- `GET /health`
- `GET /internal/manifest`
- `GET /internal/env/source`
- `GET /internal/x402/status`
- `GET /internal/x402/onchain/status`
- `GET /internal/x402/challenge?lane=basic`
- `POST /contracts/risk-score` without payment must return `402`

## Pass Criteria

- Each check returns the expected status code.
- Final line prints `smoke test verdict: pass`.

## Notes

- Script does not print secrets.
- Base URL can be set with `SENTINEL_API_BASE_URL`; default is `http://127.0.0.1:8000`.
