# Sentinel Alpha

Sentinel Alpha is the Execution Fidelity Layer for Bots and Agents, designed to score execution risk with machine-native outputs for automated policy decisions.

## API Endpoint

- `POST /contracts/risk-score`

## Payments

- Payment method: `x402`
- Network: Base (`eip155:8453`)

Pricing tiers (USDC):
- `basic`: `0.02`
- `executive`: `0.05`
- `premium`: `0.10`
- `priority`: `0.15`

## Python SDK Quickstart

```python
from sdk.python.client import SentinelAlphaClient

client = SentinelAlphaClient(
    base_url="http://localhost:8000",
    payment_header="tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
)

result = client.scan("0x1111111111111111111111111111111111111111", chain="base")
print(result)
```

## TypeScript SDK Quickstart

```ts
import { SentinelAlphaClient } from "./sdk/typescript/client";

const client = new SentinelAlphaClient(
  "http://localhost:8000",
  "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
);

const result = await client.scan("0x1111111111111111111111111111111111111111", "base");
console.log(result);
```

## Safety Note

Real payment test is required before launch. Validate end-to-end Base USDC verification behavior in your deployment environment before enabling production payment enforcement.

## Additional Docs

- `docs/14_distribution/API_QUICKSTART.md`
- `docs/14_distribution/BOT_INTEGRATION_GUIDE.md`
- `docs/14_distribution/PRE_LAUNCH_CHECKLIST.md`
- `docs/14_distribution/SDK_QUICKSTART.md`
- `docs/14_distribution/AGENTIC_MARKET_LISTING.md`

## Project Naming

Do not rename:
- Sentinel Alpha
- Mycelium Engine
- Sentinel Cells
