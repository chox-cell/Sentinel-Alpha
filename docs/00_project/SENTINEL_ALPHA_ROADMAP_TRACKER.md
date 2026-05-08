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
- v7.0 Outreach Batch 1 With Evidence (truthful templates and categories only)

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
- v6.5 Simulation Provider Adapter Boundary
- v6.6 Evaluation Harness over Base fixtures (local/offline regression checks only)
- v6.6.1 Router / Pool Candidate Heuristics (local-only candidate hints)
- v6.6.2 Fixture Evaluation Report CLI (local regression report output)
- v6.6.3 Local Evaluation Report Artifact (internal regression evidence)
- v6.7 Provider Decision Gate (docs/test policy guardrail only; no provider activation)
- v7.0 Outreach Batch 1 With Evidence
- v7.1 Outreach Target Verification Pack (research-only, source-required structure)
- v7.2 Verified Target Research Batch (public-source candidate rows; not contacted)
- v7.3 Target-Specific Outreach Message Pack (drafts only; not contacted)
- v7.4 Manual Outreach Execution Checklist (manual-send protocol only; no outreach sent)
- v7.5 Integration PR Draft Pack (x402/AgentKit/eliza docs-only; not submitted)
- v7.6 Local Upstream PR Patch Sketches (docs/examples only; not submitted)
- v8.0 AgentKit Sentinel Action Provider Prototype (local prototype only; not official provider)
- v8.1 Pre/Post Agent Action Loop Reference Pattern (architecture sketch only; no integrations claimed)
- v8.2 Local AgentKit Sentinel Demo Script (local/test-only policy assistance demo)
- v8.3 AgentKit Demo Output Fixture (deterministic sample output; illustrative only)
- v8.4 AgentKit Mini Landing Doc (two-minute prototype summary)
- v8.5 Composability Reference Draft (reference architecture only; no integrations/partnership claims)
- v8.5 Sentinel / Mycelium Composability alignment update (external community draft alignment; docs-only)
- v8.6 Agent Trust Loop Reference Pattern (ATCP/Sentinel/x402/AgentKit/Mycelium composability map; docs-only)
- v8.7 Mycelium section contribution update (external community-contributed post-action section in Agent Trust Loop doc; docs-only)
- v9.0 Sentinel Decision Receipt Boundary (local deterministic decision receipt object; no persistence/integration activation)
- v9.1 Local Decision Receipt Store Boundary (disabled-by-default sanitized store boundary; no DB/Redis/filesystem writes by default)
- v9.2 x402 Payment Decision Link Boundary (local deterministic link object; no automatic settlement and no external integration activation)
- v9.3 AgentKit Demo Receipt + Payment Link Output (local/example-only minimum loop shape)
- v9.4 Trust Loop Report Fixture (local sample artifact for minimum verifiable loop shape; docs-only)
- v9.5 Trust Loop Field Alignment v1 (documentation-only owner/purpose/privacy/integration status map)
- v9.6 ABI/Source Provider Activation Plan v1 (gate/planning only; no provider activation or runtime default change)
- v9.7 ABI/Source Provider Contract Tests with Fake Backend (test-only contract scenarios; no live provider activation)
- v9.8 Disabled ABI/Source Provider Wiring Skeleton (disabled-by-default wiring/status skeleton; no live provider calls)
- Agent commerce vision truth-filter update (UCP/AP2/Trust Object remain roadmap context)

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
- builders contacted: 3 verified (x402 Foundation / x402, Coinbase AgentKit, elizaOS / eliza issue outreach logged)
- community/adjacent outreach signals: 5 observed (AgentKit thread + Sentinel/Mycelium documentation alignment + ATCP boundary-layer discussion signal + Mycelium community documentation contribution signal + Mycelium post_action_trail field validation signal; no official AgentKit/x402/Stripe/Mycelium/ATCP acceptance)
- outreach follow-ups sent: 1 verified (AgentKit local demo follow-up comment)
- SDK installs reported: not tracked yet (add when reliable source exists)
- integrations started: 0 verified (no integration proof from outreach issue closures)
