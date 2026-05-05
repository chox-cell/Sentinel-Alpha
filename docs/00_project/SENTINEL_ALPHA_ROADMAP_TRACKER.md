# Sentinel Alpha roadmap tracker (SSOT)

This file is the single source of truth for Sentinel Alpha roadmap status, claims discipline, and operating constraints.

## Product doctrine

- BeezShield builds guardians, not traders.
- BeezShield agents verify, score, explain, block, review, and attest before autonomous execution.
- Sentinel Alpha protects onchain contract/asset execution.
- Ema-Bee is a future commerce safety gate concept, not a B2B arbitrage/trading agent.
- No product pivot: contracts/assets first.

## 1) Current live product

- Website is live.
- API endpoint is live: `/contracts/risk-score`.
- Access model includes x402-gated flow.
- npm SDK is live: `@beezshield/sentinel@0.1.0`.
- AgentKit-style example is available.
- Public docs are live.
- ERC-8004 identity is published.

## 2) Completed roadmap

Status: **Done**

- v3.8 npm SDK live (`@beezshield/sentinel@0.1.0`)
- v3.9 AgentKit-style example
- v4.1 website brand refresh
- v4.2 public docs/trust pages
- v4.3 outreach tracker
- v4.4 target research prep
- v5.0 risk capability matrix
- v5.1 Asset Classification Engine
- v5.2 Source / Proxy / Admin Signal Layer
- v5.3 ERC20 Risk Heuristics
- v5.4 NFT / Zora Asset Heuristics
- v5.5 Simulation Adapter Boundary
- v5.6 Risk Explanation Engine
- v5.7 Chain Support Matrix
- v5.8 Intent Alignment Layer
- v5.9 Mempool / MEV Signal Boundary
- v5.10 risk engine release summary
- v6.0 data provider strategy
- v6.1 Local Bytecode Signal Analyzer
- v6.2 ABI / Source Provider Adapter
- Public Guardian Doctrine pack (manifesto + llms + doctrine JSON)

## 3) Current risk engine stack

### Real runtime metadata/signal layers
- asset classification metadata
- source/proxy/admin metadata
- ERC20 heuristic metadata
- NFT/Zora heuristic metadata
- chain support metadata
- intent alignment policy-assist metadata
- mempool/MEV boundary metadata
- security explanation metadata
- local bytecode signal analyzer metadata

### Boundary-only layers (not fully live providers)
- simulation adapter boundary (default not configured)
- mempool/MEV boundary (default not configured)
- external ABI/source lookup is not fully wired

### Local-only analysis
- local bytecode opcode/selector candidate extraction
- deterministic local rule-based signal composition

### Roadmap paid-provider lanes (not enabled by default)
- simulation provider integration
- mempool/MEV external feed
- expanded paid RPC redundancy

## 4) Next roadmap

- v6.1.1 Base Contract Fixture Dataset
- v6.2 ABI / Source Provider Adapter
- v6.3 Local Postgres Risk History Schema
- v6.3 Local Risk History DB Plan (docs-only)
- v6.3.1 Local Risk History SQL Schema (schema-only, manual/future execution)
- v6.3.2 Disabled Risk History DB Adapter Boundary
- v6.4 Source / ABI Cache Boundary
- v6.5 Simulation Provider Adapter
- v6.6 Evaluation Harness
- v7.0 Outreach Batch 1

## 5) Cost discipline

- <= $10/month pre-revenue
- no paid QuickNode by default
- no managed DB before need
- no paid simulation provider before demand
- local bytecode analysis first

## 6) Claims discipline

- no guaranteed protection
- no detects all honeypots
- no catches most bytecode traps
- no full multi-chain support
- no full intent verification
- no MEV prevention
- no automatic x402 settlement

## 7) Metrics

- tests passed count: 360
- npm package version: `@beezshield/sentinel@0.1.0`
- current HEAD: `97b39e3`
- outreach targets: 20 planned (T01-T20 structure)
- builders contacted: 0 verified in tracker placeholders
- SDK installs reported: not tracked yet (add when reliable source exists)
- integrations started: not tracked yet (add when verified)
