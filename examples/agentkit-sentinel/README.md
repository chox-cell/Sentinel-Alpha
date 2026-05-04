# AgentKit-style Sentinel Example

This folder shows an **AgentKit-style** integration pattern for calling Sentinel Alpha before a contract interaction.

It is **not** an official live Coinbase AgentKit provider. Provider wiring is coming next.

## Install

```bash
cd examples/agentkit-sentinel
npm install
```

Package used:

```bash
npm install @beezshield/sentinel
```

## Configure

Copy `.env.example` values into your runtime environment:

- `SENTINEL_API_URL=https://api.beezshield.com`
- `SENTINEL_LANE=basic`
- `X402_PAYMENT=` (set when you have a valid payment settlement header)

## Run

```bash
npm run build
node dist/index.js 0x1111111111111111111111111111111111111111
```

## Behavior

- Calls `decideBeforeExecution()` using `@beezshield/sentinel`.
- If `shouldExecute === true`, runs a placeholder execute function.
- If `shouldExecute === false`, routes to block/review path.
- Catches `SentinelPaymentRequiredError` and surfaces the x402 challenge.

## Safety notes

- Sentinel provides pre-execution risk decisions; it does not guarantee protection.
- This example does not perform automatic x402 settlement.
- This example does not contain wallet keys or on-chain transaction execution.
