# Sentinel AgentKit-style Example (v3.9)

## Purpose

Provide a minimal, copy-paste integration path for builders who want to gate contract interactions with Sentinel Alpha before execution.

Path:

- `examples/agentkit-sentinel/`

## What this is

- A TypeScript **AgentKit-style** example that calls `@beezshield/sentinel`.
- A policy gate using `decideBeforeExecution()` before a placeholder execute call.
- Explicit handling of `SentinelPaymentRequiredError` for x402 challenge responses.

## What this is not

- Not an official live Coinbase AgentKit provider.
- Not automatic x402 settlement.
- Not wallet key management or real transaction execution.

## Environment

Example `.env.example`:

- `SENTINEL_API_URL=https://api.beezshield.com`
- `SENTINEL_LANE=basic`
- `X402_PAYMENT=`

## Builder flow

1. Create Sentinel client.
2. Call `decideBeforeExecution({ contract_address, chain })`.
3. If `shouldExecute` is true, proceed to your own execution implementation.
4. If false, block/review.
5. If x402 challenge occurs, handle payment path explicitly.
