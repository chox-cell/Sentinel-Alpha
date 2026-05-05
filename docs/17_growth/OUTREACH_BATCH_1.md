# Outreach Batch 1 With Evidence (v7.0)

## 1) Purpose

This is the first outreach batch for aligned builders using truthful, currently verified evidence only.
It prepares messaging and targeting structure; it does not claim any builder was contacted or integrated.

## 2) Current proof points

- npm SDK: `@beezshield/sentinel`
- install: `npm install @beezshield/sentinel`
- API: `/contracts/risk-score`
- x402-gated API
- ERC-8004 identity
- AgentKit-style example available
- official provider coming next
- Guardian Doctrine public
- local fixture evaluation report: 8 fixtures / 8 passed / 0 review
- disclaimer: local regression evaluation only, not a security guarantee

## 3) Outreach positioning

Use:

- pre-execution risk decision layer
- guardians, not traders
- contract/asset execution safety
- review/block/allow policy assistance

Avoid:

- security guarantees
- honeypot certainty
- catches most traps
- prevents MEV
- AgentKit provider live

## 4) Batch 1 target categories

- AgentKit/Base builders
- MCP trading/tool servers on Base
- x402 builders
- Zora/Base asset tools
- wallet automation projects
- security-minded bot builders

## 5) Message templates

### GitHub issue template

Hi team — we built `@beezshield/sentinel` as a pre-execution risk decision layer for contract/asset execution safety.  
Install: `npm install @beezshield/sentinel` and review the AgentKit-style example available in-repo (official provider coming next).  
Current local fixture evaluation: 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).  
If useful, we can open an optional small PR to wire review/block/allow policy assistance into your flow.

### Twitter/X DM template

Sharing `@beezshield/sentinel` for pre-execution risk decisioning on Base-aligned flows.  
`npm install @beezshield/sentinel` + AgentKit-style example available; official provider coming next.  
Evidence line: local fixture evaluation is 8 fixtures / 8 passed / 0 review (not a security guarantee).  
Happy to draft an optional PR path if relevant.

### Discord/Telegram intro template

We are building guardians, not traders: `@beezshield/sentinel` helps agents route execution via review/block/allow assistance.  
SDK is live (`npm install @beezshield/sentinel`), AgentKit-style example is available, and official provider coming next.  
Current evidence: local fixture evaluation 8 fixtures / 8 passed / 0 review; regression-only and not a security guarantee.  
Can share an optional integration PR sketch if helpful.

### AgentKit builder message template

If you are building with AgentKit-style flows, `@beezshield/sentinel` can add pre-execution risk policy assistance before contract calls.  
Install with `npm install @beezshield/sentinel`; AgentKit-style example available now, official provider coming next.  
Local fixture evaluation currently shows 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).  
Optional offer: we can propose a minimal PR integration path.

### x402 builder message template

For x402 builders, Sentinel adds risk policy assistance around `/contracts/risk-score` in an x402-gated API flow.  
SDK is live at `@beezshield/sentinel` (`npm install @beezshield/sentinel`), with an AgentKit-style example available and official provider coming next.  
Current evidence line: local fixture evaluation 8 fixtures / 8 passed / 0 review; this is not a security guarantee.  
If useful, we can open an optional PR for your payment + policy routing path.

## 6) Evidence snippet

Current local fixture evaluation covers 8 Base fixture patterns with 8 passed / 0 review. This is regression evidence, not a security guarantee.

## 7) Tracker update rule

Update `OUTREACH_TRACKER.md` only if adding a Batch column or evidence field.
Do not mark any target as contacted.
All statuses remain not contacted unless real outreach happened.
