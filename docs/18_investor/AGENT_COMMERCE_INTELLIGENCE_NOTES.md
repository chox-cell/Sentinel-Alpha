# Agent Commerce Intelligence Notes (internal)

## 1) Executive thesis

Agentic commerce increases the need for pre-execution trust/risk gates, especially where autonomous agents can trigger irreversible financial or contract actions.

## 2) Verified / source-backed observations

- Google UCP exists as an open standard initiative for agentic commerce interoperability.
- Google AP2 uses signed mandates / verifiable authorization style controls in the commerce-agent flow.
- Salesforce reported 119% agent creation growth in H1 2025 among early adopters (source-backed claim to retain citation discipline).
- Belgium B2B e-invoicing mandate began Jan 1, 2026.
- Peppol is primarily structured document exchange, not an open RFQ marketplace.

## 3) Unsupported or risky claims (do not use)

- Claim that every company already exposes a `/.well-known/ucp` endpoint.
- Claim that UCP v2.1 is universal across all B2B systems.
- Claim that Citi/JPM automatically fund any agent.
- Claim that Peppol exposes internal RFQ marketplaces by default.
- Claim that Sentinel should immediately shift to global B2B arbitrage as the core product path.

## 4) Product implication

Sentinel stays focused on:

- BeezShield builds guardians, not traders.
- BeezShield agents verify, score, explain, block, review, and attest before autonomous execution.
- Sentinel Alpha protects onchain contract/asset execution.
- pre-execution risk decision for autonomous agents
- contracts/assets first
- x402/ERC-8004/Base first

Future expansion candidates:

- Agent Commerce Trust Object
- payment mandate risk
- supplier identity risk
- invoice/PO document risk
- commerce action risk

## 5) Trust Object concept (roadmap only)

Future generic object concept (not live):

- `target_type`: `contract` | `asset` | `agent_identity` | `payment_mandate` | `supplier` | `invoice` | `purchase_order`
- `target`
- `intent`
- `context`
- `risk decision`

This is roadmap only, not live runtime behavior.

## 6) B2B deal scout note

- B2B deal scout is a separate future product idea.
- Ema-Bee is a future commerce safety gate concept, not a B2B arbitrage/trading agent.
- Do not mix it into Sentinel execution roadmap now.
- First priority remains onchain/agent builder adoption.

## 7) Public doctrine pack update

- Public Manifesto created for truthful human/LLM/machine positioning.
- UCP/AP2 are roadmap context, not runtime integration.
- Trust Object Model is roadmap only.
- Ema-Bee is a future concept only.

## 8) Useful vision retained

- agentic commerce increases need for pre-execution trust gates.
- autonomous agents need policy layers before contracts/assets/payments/tools.
- BeezShield builds guardians, not traders.
- Sentinel Alpha starts with onchain contract/asset execution safety.
- Trust Objects are future commerce safety roadmap.
- UCP/AP2 are roadmap commerce context only.

## 9) Unsafe claim corrections

| Unsafe claim | Safe wording |
|---|---|
| Prompt injection defense | future middleware/intent-boundary context; not live prevention claim |
| Honeypot detection | simulation/heuristic roadmap; no detection guarantee |
| Central Bank of Trust | guardian layer for autonomous execution |
| tax every autonomous action | usage-based risk decision pricing |
| UCP/AP2 native integration | roadmap context, not runtime integration |
| global reputation registry | ERC-8004 identity live; broader reputation/validation roadmap |
