# Outreach Message Drafts Batch 1 (v7.3)

## 1) Purpose

These are draft messages only for internal review.
No outreach has been performed.

## 2) Evidence rules

Messages may mention only currently verified points:

- `@beezshield/sentinel`
- `npm install @beezshield/sentinel`
- `/contracts/risk-score`
- x402-gated API
- ERC-8004 identity
- AgentKit-style example available
- official provider coming next
- local fixture evaluation: 8 fixtures / 8 passed / 0 review
- regression evidence only, not a security guarantee

## 3) Target-specific drafts

### T01 — Coinbase AgentKit
- target_id: T01
- project_name: Coinbase AgentKit
- source_url: https://github.com/coinbase/agentkit
- why_this_message_fits: Public repository describes AgentKit wallet tooling for AI agents.
- GitHub issue draft:  
  Hi AgentKit team — we built `@beezshield/sentinel` as a pre-execution risk decision layer for contract/asset execution policy assistance.  
  If useful for your builders, they can try `npm install @beezshield/sentinel` and the AgentKit-style example available in-repo (official provider coming next).  
  Current evidence: local fixture evaluation is 8 fixtures / 8 passed / 0 review, as regression evidence only and not a security guarantee.  
  Happy to share an optional PR sketch for a minimal review/block/allow pattern.
- X/DM draft:  
  Sharing a relevant tooling option for AgentKit-style builders: `@beezshield/sentinel` (`npm install @beezshield/sentinel`).  
  AgentKit-style example is available; official provider coming next.  
  Fixture evaluation currently shows 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).  
  If helpful, we can draft an optional PR path.
- optional PR angle: Minimal wrapper before contract execution calling `/contracts/risk-score` and mapping to allow/review/block policy.
- safety disclaimer: Regression evidence only; not a security guarantee.
- status: not contacted

### T02 — Coinbase x402
- target_id: T02
- project_name: Coinbase x402
- source_url: https://github.com/coinbase/x402
- why_this_message_fits: Public repository describes x402 as a payments protocol built on HTTP.
- GitHub issue draft:  
  Hi x402 team — sharing `@beezshield/sentinel` for builders who need policy assistance around contract execution in x402-gated flows.  
  SDK is live (`npm install @beezshield/sentinel`) and can be paired with `/contracts/risk-score`; AgentKit-style example available, official provider coming next.  
  Local fixture evaluation is 8 fixtures / 8 passed / 0 review as regression evidence only, not a security guarantee.  
  We can propose an optional PR example for explicit payment + decision routing.
- X/DM draft:  
  For x402 builders, `@beezshield/sentinel` can be used as a pre-execution decision step before sensitive contract calls.  
  `npm install @beezshield/sentinel` + AgentKit-style example available; official provider coming next.  
  Evidence line: 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).
- optional PR angle: Example request flow that handles payment-required path and then evaluates policy via `/contracts/risk-score`.
- safety disclaimer: Regression evidence only; not a security guarantee.
- status: not contacted

### T03 — Zora Developer Docs
- target_id: T03
- project_name: Zora Developer Docs
- source_url: https://docs.zora.co/
- why_this_message_fits: Docs page highlights developer tooling and agent-ready skills in Zora ecosystem.
- GitHub issue draft:  
  Hi Zora developer relations team — sharing `@beezshield/sentinel` as a pre-execution risk decision layer for contract/asset execution safety assistance.  
  Builders can install with `npm install @beezshield/sentinel`; AgentKit-style example is available and official provider coming next.  
  Current local fixture evaluation reports 8 fixtures / 8 passed / 0 review as regression evidence only and not a security guarantee.  
  If useful, we can draft an optional PR-style integration example for agent-driven execution paths.
- X/DM draft:  
  Sharing a conservative safety-assist option for Zora ecosystem builders: `@beezshield/sentinel`.  
  Install: `npm install @beezshield/sentinel`; AgentKit-style example available, official provider coming next.  
  Evidence: 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).
- optional PR angle: Example “review before execute” helper around contract calls.
- safety disclaimer: Regression evidence only; not a security guarantee.
- status: not contacted

### T04 — modelcontextprotocol/servers
- target_id: T04
- project_name: modelcontextprotocol/servers
- source_url: https://github.com/modelcontextprotocol/servers
- why_this_message_fits: Public repository is an MCP server hub useful for execution-capable tool workflows.
- GitHub issue draft:  
  Hi MCP servers maintainers — sharing `@beezshield/sentinel` for teams that want an optional pre-execution decision checkpoint before contract calls.  
  SDK is available via `npm install @beezshield/sentinel`, with AgentKit-style example available and official provider coming next.  
  Current fixture evaluation is 8 fixtures / 8 passed / 0 review as regression evidence only, not a security guarantee.  
  Optional PR angle: a small policy adapter for Base-oriented execution tools.
- X/DM draft:  
  For MCP execution workflows, `@beezshield/sentinel` can add review/block/allow policy assistance before contract actions.  
  `npm install @beezshield/sentinel`; AgentKit-style example available; official provider coming next.  
  Evidence: local fixture evaluation 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).
- optional PR angle: Add an optional tool wrapper that checks `/contracts/risk-score` before execution.
- safety disclaimer: Regression evidence only; not a security guarantee.
- status: not contacted

### T05 — Safe Core SDK
- target_id: T05
- project_name: Safe Core SDK
- source_url: https://github.com/safe-global/safe-core-sdk
- why_this_message_fits: Public repository indicates account abstraction SDK where execution policy checks may be useful.
- GitHub issue draft:  
  Hi Safe Core SDK team — sharing `@beezshield/sentinel` for builders who want an optional pre-execution policy signal before contract actions.  
  Install path: `npm install @beezshield/sentinel`; AgentKit-style example available and official provider coming next.  
  Local fixture evaluation currently reports 8 fixtures / 8 passed / 0 review as regression evidence only, not a security guarantee.  
  If relevant, we can provide an optional PR-style example integration.
- X/DM draft:  
  For account-abstraction builders, `@beezshield/sentinel` offers optional pre-execution decision support.  
  `npm install @beezshield/sentinel` + AgentKit-style example available; official provider coming next.  
  Evidence: 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).
- optional PR angle: Optional account operation precheck calling `/contracts/risk-score`.
- safety disclaimer: Regression evidence only; not a security guarantee.
- status: not contacted

### T06 — Coinbase OnchainKit
- target_id: T06
- project_name: Coinbase OnchainKit
- source_url: https://github.com/coinbase/onchainkit
- why_this_message_fits: Public repository targets onchain app builders where execution safety policy assistance can complement tooling.
- GitHub issue draft:  
  Hi OnchainKit team — sharing `@beezshield/sentinel` as an optional pre-execution risk decision layer for builders doing contract interactions.  
  Install with `npm install @beezshield/sentinel`; AgentKit-style example available, official provider coming next.  
  Current fixture evaluation is 8 fixtures / 8 passed / 0 review as regression evidence only and not a security guarantee.  
  If useful, we can draft an optional PR flow for policy-assisted execution routing.
- X/DM draft:  
  Onchain builders may find `@beezshield/sentinel` useful for policy checks before contract execution.  
  `npm install @beezshield/sentinel`; AgentKit-style example available; official provider coming next.  
  Evidence line: 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).
- optional PR angle: Lightweight client helper that maps result to allow/review/block UI/logic.
- safety disclaimer: Regression evidence only; not a security guarantee.
- status: not contacted

### T07 — elizaOS/eliza
- target_id: T07
- project_name: elizaOS/eliza
- source_url: https://github.com/elizaOS/eliza
- why_this_message_fits: Public repository describes autonomous agent framework where pre-execution gating can be relevant.
- GitHub issue draft:  
  Hi elizaOS team — sharing `@beezshield/sentinel` for teams who want optional pre-execution policy assistance in autonomous execution loops.  
  SDK is live (`npm install @beezshield/sentinel`) with AgentKit-style example available; official provider coming next.  
  Current fixture evaluation reports 8 fixtures / 8 passed / 0 review as regression evidence only and not a security guarantee.  
  If helpful, we can provide an optional PR-style integration draft.
- X/DM draft:  
  For autonomous agent builders, `@beezshield/sentinel` can add review/block/allow assistance before contract calls.  
  Install: `npm install @beezshield/sentinel`; AgentKit-style example available; official provider coming next.  
  Evidence: 8 fixtures / 8 passed / 0 review (regression evidence only, not a security guarantee).
- optional PR angle: Optional pre-action middleware for contract-call tools.
- safety disclaimer: Regression evidence only; not a security guarantee.
- status: not contacted

## 4) Message quality rules

- short
- respectful
- technical
- non-spammy
- optional PR / feedback oriented
- no fear-selling
- no exploit accusation
- no "you are vulnerable" language

## 5) Forbidden copy

Do not use:

- guaranteed protection
- detects honeypots
- prevents MEV
- live simulation
- full contract coverage
- AgentKit provider live
- official AgentKit integration live

Use `status: not contacted` only as status metadata.

## 6) Tracker

`OUTREACH_TRACKER.md` remains not contacted.
Do not mark contacted or integrated.
