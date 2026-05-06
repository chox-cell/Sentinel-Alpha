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

## Notes

- AgentKit-style example available in this repo.
- official provider coming next.
- local fixture evaluation: 8 fixtures / 8 passed / 0 review.
- regression evidence only, not a security guarantee.
- demo is local/example only.
- no wallet action is executed.
- no transaction is signed.
