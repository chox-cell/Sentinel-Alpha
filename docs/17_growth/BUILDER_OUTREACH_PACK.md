# Builder Outreach Pack (v4.0)

## 30-second pitch

Sentinel Alpha is a pre-execution risk decision layer for bots and autonomous agents.
Before your bot touches a contract, you call Sentinel and get a machine-readable decision (`allow`, `review`, `block`) with score/confidence/attestation.
It is live as API + npm SDK and designed for quick integration.

## 5-minute integration path

1. Install SDK:
   - `npm install @beezshield/sentinel`
2. Create client.
3. Call `decideBeforeExecution()` with `contract_address`.
4. Execute only if `shouldExecute` is true.
5. Handle x402 payment challenge path for production payment flows.

```ts
import { createSentinelClient, SentinelPaymentRequiredError } from "@beezshield/sentinel";

const sentinel = createSentinelClient({ lane: "basic" });

try {
  const decision = await sentinel.decideBeforeExecution({
    contract_address: "0x1111111111111111111111111111111111111111",
    chain: "base",
  });

  if (decision.shouldExecute) {
    // your execute call
  } else {
    // review/block path
  }
} catch (err) {
  if (err instanceof SentinelPaymentRequiredError) {
    // integrate explicit x402 payment flow (not automatic)
  }
}
```

## x402 truth

- Sentinel SDK requires explicit x402 settlement handling in builder code.
- Builders must supply settlement headers/payment integration where required.

## What Sentinel does

- Returns pre-execution risk decisions for contract interactions.
- Provides machine-usable outputs for policy routing.
- Helps teams reduce blind execution risk in autonomous flows.

## What Sentinel does NOT do

- Does not guarantee protection.
- Does not replace your full security process.
- Does not provide an official live AgentKit provider yet.

## CTA

- Try SDK: `npm install @beezshield/sentinel`
- Try AgentKit-style example: `examples/agentkit-sentinel`
- If useful, request a tailored PR integration path for your bot repository.
