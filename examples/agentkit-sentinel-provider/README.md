# AgentKit Sentinel Action Provider Prototype (Local)

Prototype only.

- Not an official Coinbase AgentKit provider.
- Not submitted upstream.
- Does not execute transactions.
- Does not sign wallet actions.
- Does not guarantee protection.
- Does not claim honeypot detection.

This example shows an Action Provider-style prototype for using Sentinel as a pre-execution risk decision policy assistant before high-risk onchain actions.

## Install

```bash
cd examples/agentkit-sentinel-provider
npm install
```

## Usage sketch

```ts
import { sentinelRiskCheckAction } from "./src/index.js";

const result = await sentinelRiskCheckAction({
  contract_address: "0x1111111111111111111111111111111111111111",
  chain: "base",
  requested_action: "contract_call",
  intent: "pre-trade safety check",
});

// allow / review / block
console.log(result.action, result.reason);
```

## Run local demo

```bash
cd examples/agentkit-sentinel-provider
npm install
npm run demo
```

Demo output is policy assistance (`allow` / `review` / `block`) only.

## Sample output fixture

Sample output fixture path:

`examples/sample-output.json`

This sample output is illustrative only.
It is not live scan proof.
It is not a security guarantee.

Output shape includes:

- `action`
- `reason`
- `confidence`
- `explanation`
- `notSecurityGuarantee`
- `sentinel_decision_ref`
- `action_ref`
- `payment_decision_link_ref`
- `payment_protocol`
- `payment_status`
- `automatic_settlement_claimed`
- `sampleOnly`

## Minimum Verifiable Loop Output

This local demo now shows a minimum verifiable loop output shape:

- Sentinel decision policy result (`allow` / `review` / `block`)
- Decision receipt references (`sentinel_decision_ref`, `action_ref`)
- Payment decision link reference (`payment_decision_link_ref`) with optional payment context markers

Boundaries:

- no real x402 settlement is performed by this demo
- no wallet execution/signing
- not a security guarantee
- local example only

## Notes

- AgentKit-style example available in this repo.
- official provider coming next.
- local fixture evaluation: 8 fixtures / 8 passed / 0 review.
- regression evidence only, not a security guarantee.
- demo is local/example only.
- no wallet action is executed.
- no transaction is signed.

## Mini landing doc

See:

`docs/17_growth/AGENTKIT_SENTINEL_MINI_LANDING.md`
