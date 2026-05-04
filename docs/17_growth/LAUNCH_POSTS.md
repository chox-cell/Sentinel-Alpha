# Launch Posts (v4.0)

All copy in this file keeps product truth:
- npm SDK live: `@beezshield/sentinel`
- AgentKit-style example available
- official provider coming next (not live)
- no safety overclaims

## X / Twitter

Sentinel Alpha is live:
- API: https://api.beezshield.com/contracts/risk-score
- npm: `npm install @beezshield/sentinel`
- AgentKit-style example: `examples/agentkit-sentinel`

Use it as a pre-execution decision gate before bots touch contracts.
Official AgentKit provider wiring is coming next.

## LinkedIn

We shipped BeezShield Sentinel Alpha for builders who run autonomous onchain agents.

What is live now:
- Production risk decision API
- npm SDK: `@beezshield/sentinel` (v0.1.0)
- AgentKit-style integration example in repo

What is not live yet:
- official AgentKit provider (coming next)
- built-in x402 settlement in SDK

Goal: help teams add a practical pre-execution decision layer in minutes.

## Farcaster

Sentinel Alpha update:
- npm SDK live: `@beezshield/sentinel`
- call `decideBeforeExecution()` with `contract_address`
- AgentKit-style example in repo
- official provider coming next

## Short DM (builder)

Saw your bot repo - we built a lightweight pre-execution risk gate you can drop in quickly.
SDK is live on npm (`@beezshield/sentinel`) and we have an AgentKit-style example.
If useful, I can open a small PR showing where to call `decideBeforeExecution()`.

## Technical builder version

Before a contract call:
1) `npm install @beezshield/sentinel`
2) call `decideBeforeExecution({ contract_address, chain })`
3) route allow/review/block in your policy layer

Includes x402 challenge handling via `SentinelPaymentRequiredError`.
No automatic settlement in SDK; official AgentKit provider is coming next.

## Investor update version

BeezShield Sentinel Alpha now has:
- live API
- live npm SDK (`@beezshield/sentinel`)
- public AgentKit-style integration example

Near-term focus: first 10 builder integrations and official provider wiring.
Positioning remains practical: pre-execution risk decisions with clear policy trade-offs.
