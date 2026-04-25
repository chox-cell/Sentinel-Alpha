# Launch Env Runbook v1.4

## Purpose
Provide a clear, non-secret pre-launch environment check for Sentinel Alpha external launch readiness.

## Command

```bash
python3 scripts/prelaunch_check.py
```

## Required Ready Conditions

`launch ready: true` is reported only when all conditions are true:

- `PAYMENT_MODE=real`
- `X402_ENABLED=true`
- `X402_MOCK_ONCHAIN_VERIFY=false` (mock mode disabled)
- `BASE_RPC_URL` is configured (value not printed)
- wallet is configured
- treasury is configured
- `agentic-market.json` exists
- `README.md` exists
- SDK docs exist (`sdk/python/README.md`, `sdk/typescript/README.md`)
- launch docs exist (`docs/14_distribution/API_QUICKSTART.md`, `docs/14_distribution/BOT_INTEGRATION_GUIDE.md`, `docs/14_distribution/PRE_LAUNCH_CHECKLIST.md`)

## Output Safety

- Script prints booleans and status labels only.
- Script never prints `BASE_RPC_URL` value or other secret values.
