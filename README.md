# Sentinel Alpha

Sentinel Alpha is the production Execution Fidelity Layer for Bots and Agents, under the BeezShield umbrella brand.

## What Problem It Solves

Bots and autonomous agents need a deterministic risk gate before execution, but most stacks still rely on ad hoc heuristics, dashboards, or manual reviews. Sentinel Alpha provides one machine-native API decision path that can be used directly in trading, policy, and automation loops.

## API Endpoint

- `POST /contracts/risk-score`
- Use your deployed `PUBLIC_BASE_URL` in production.
- Production endpoint: `https://api.beezshield.com/contracts/risk-score`
- Optional lane header: `X-SENTINEL-LANE` (`basic`, `executive`, `premium`, `priority`)
- Default lane: `basic`

## Product and Brand

- Product/agent: `Sentinel Alpha`
- Umbrella brand: `BeezShield`

## 🚀 Live Demo & Growth

- **Forensic Lab Demo:** [beezshield.com/demo.html](https://beezshield.com/demo.html) (Developer Preview)
- **Public Website:** [beezshield.com](https://beezshield.com)
- **ERC-8004 Agent Identity:** [8004scan - Agent 45967](https://8004scan.io/agents/base/45967)
- **API Endpoint:** `https://api.beezshield.com/contracts/risk-score`
- **GitHub:** [chox-cell/Sentinel-Alpha](https://github.com/chox-cell/Sentinel-Alpha)

## ERC-8004 Identity

- Sentinel Alpha is registered on 8004scan.
- Agent ID: `45967`
- Network: `Base`
- Agent URL: `https://8004scan.io/agents/base/45967`
- BeezShield remains the umbrella brand, while Sentinel Alpha is the product agent.

## What The API Returns

The response is built for machine enforcement and includes:
- `score`
- `confidence`
- `action`
- `emergency_signal`
- `attestation`

## Payments

- Payment method: `x402`
- Network: Base (`eip155:8453`)

Pricing tiers (USDC):
- `basic`: `0.02`
- `executive`: `0.05`
- `premium`: `0.10`
- `priority`: `0.15`

## Marketplace / Discovery

- Agentic Market submission-ready metadata is published.
- ERC-8004 registered on 8004scan (`Agent ID: 45967`).
- API live: `https://api.beezshield.com/contracts/risk-score`
- x402 enabled on Base Mainnet (`eip155:8453`)
- Pricing lanes: `basic 0.02`, `executive 0.05`, `premium 0.10`, `priority 0.15` USDC

## Clean Distribution Engine

- Public risk intelligence: publish useful machine-readable signals and integration evidence.
- Demo risk feed: safe illustrative feed at `apps/website/risk-feed.html` and `data/demo-risk-feed.json`.
- Agent discovery assets: `llms.txt`, `llms-full.txt`, and `.well-known` metadata.
- Policy: no coercive outreach or fear-selling language.
- Links:
  - Website: `https://beezshield.com`
  - API: `https://api.beezshield.com/contracts/risk-score`
  - ERC-8004: `https://8004scan.io/agents/base/45967`

## Proof Points

- Verified production payment proof: Real Base USDC payment verified
- x402 replay protection active
- settlement ledger active
- smoke test pass
- release tag `v1.5.0`

## Quickstart cURL (x402 tx header)

Example tx hashes below are placeholders for integration examples only.

```bash
curl -X POST "${PUBLIC_BASE_URL}/contracts/risk-score" \
  -H "Content-Type: application/json" \
  -H "X-SENTINEL-LANE: priority" \
  -H "X402-PAYMENT: tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
  -d '{"contract_address":"0x1111111111111111111111111111111111111111","chain":"base","context":{}}'
```

## Python SDK Quickstart

```python
import os

from sdk.python.client import SentinelAlphaClient

client = SentinelAlphaClient(
    base_url=os.environ["PUBLIC_BASE_URL"],
    payment_header="tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
)

result = client.scan("0x1111111111111111111111111111111111111111", chain="base")
print(result)
```

## TypeScript SDK Quickstart

```ts
import { SentinelAlphaClient } from "./sdk/typescript/client";

const client = new SentinelAlphaClient(
  process.env.PUBLIC_BASE_URL!,
  "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
);

const result = await client.scan("0x1111111111111111111111111111111111111111", "base");
console.log(result);
```

Lane-aware examples:
- Python: `client.scan("0x...", chain="base", lane="priority")`
- TypeScript: `client.scan("0x...", "base", "priority")`

## Marketplace Files

- `agentic-market.json`
- `marketplace-submission.json`
- `identity-manifest.json`

## Identity Status

- local DID active (`did:sentinel-alpha:local`)
- ERC-8004 registered on 8004scan (Agent ID `45967`)
- Registration URL: `https://8004scan.io/agents/base/45967`

## Production Warning

Real payment test is required before launch. Validate end-to-end Base USDC verification behavior in your deployment environment before enabling production payment enforcement.
- Do not enable mock verification in production.
- Never commit `.env`.

## Public Smoke Test

```bash
python3 scripts/public_smoke_test.py
```

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
