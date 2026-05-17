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
- v9.9 Provider Config Audit and `.env.example` Placeholders (config/doc/test-only; provider remains disabled by default)
- v10.0 Controlled Free ABI/Source Provider Trial Plan (docs/test-only gate; controlled trial planned; live provider not enabled by default)
- v10.1 Known Base Contracts Trial Dataset (docs/test-only placeholder table; no live lookup; provider remains disabled by default)
- v10.2 ABI/Source Provider Trial Result Schema (docs-only sanitized evidence shape; trial not run; provider not activated)
- v10.3 Sourcify / Blockscout Dry-Run Adapter Skeleton (no HTTP by default; dry_run_only gated; defaults unchanged)
- v10.4 ABI/Source Provider Trial Runbook + Founder Approval Gate (docs-only operational checklist; trial not run; defaults unchanged)
- v10.5 ABI/Source Trial Evidence Placeholder (`not_run` static sample bundle; no live activation)
- v10.6 ABI/Source Provider Trial Approval Record — Not Approved (explicit hold + founder phrase gate; no runtime change)
- v10.7 Founder Approval Recorded + Real Public Base Trial Targets (founder phrase received; sourced target candidates prepared; trial not run; provider not active)
- v10.8A Record Aborted Sourcify Trial Attempt Due to Network Error (attempted read-only evidence only; all rows network_error; provider remains disabled)
- v10.9 VPS Sourcify Connectivity Preflight Plan (docs/test-only; preflight not run; no provider rerun)
- v11.0 Sentinel Alpha Technical Status Report (SSOT snapshot; docs-only; no runtime activation)
- v11.1 Public-Safe Sentinel Alpha Technical Summary (public-safe shareable summary; no runtime activation)
- v11.2 VPS Sourcify Connectivity Preflight Result (manual one-shot reachability record; HTTP 404; not trial rerun; provider remains disabled)
- v11.3 Sourcify Endpoint Correction Plan (docs/test-only; no network calls; endpoint strategy before rerun)
- v11.4 VPS Sourcify Endpoint Validation — One Target Only (one GET for T01; endpoint validation artifact; not trial rerun; provider remains disabled)
- v11.5 Sourcify Endpoint Validation Failure Consolidation (docs/test-only status note; no new network; full trial remains blocked until usable metadata)
- v11.6 ABI/Source Provider Pivot Review (docs/test-only; Sourcify unresolved; Blockscout prep vs retry options; no provider activation)
- v11.7 Blockscout Endpoint Validation Plan (docs/test-only; one-target path planned; no network; no provider activation)
- v11.8 Blockscout Base Endpoint Source Pack (docs/test-only; candidate URL slots; no selection; no network)
- v11.9 Blockscout Base Source-Backed Endpoint Candidate (B01 public docs URLs documented; not selected; not validated; no network)
- v12.0 Blockscout Candidate Selection Record (B01 selected for future one-target validation; phrase gate; no network; no provider activation)
- v12.x x402 Directory Submission Pack (docs/test-only; community directory copy after ecosystem-page sunset signal; no auto-submit)
- v12.x Mycelium directory cross-reference signal (giskard09 community alignment; optional future directory copy cross-reference after both listings live; no partnership/integration)
- v12.x x402scan GET challenge compatibility (`GET /contracts/risk-score` returns 402 discovery challenge; POST unchanged; directory listing not claimed)
- v12.x x402scan schema/header compatibility (`x402Version` + `accepts[]` + `PAYMENT-REQUIRED` on 402 discovery responses; unpaid POST aligns; legacy body keys preserved; no listing claim)
- v12.x x402scan HEAD/OPTIONS compatibility (`HEAD` discovery 402 + payment headers empty body; `OPTIONS` preflight **204** with allow-methods/Headers/Expose headers on `/contracts/risk-score`; no listing claim)
- v12.x x402 exact-EVM accepts alignment (Base USDC contract + `amount` + `maxTimeoutSeconds` + `extra` in **`accepts[]`** / `PAYMENT-REQUIRED`; legacy top-level `asset: USDC` unchanged; no listing claim)
- v12.x x402scan multi-verb discovery (PATCH/PUT/DELETE return same **402** challenge as GET, **exclude** from OpenAPI schema; OPTIONS allow-methods expanded; no listing claim)
- v12.x x402scan POST prepayment gate (unpaid **POST** returns **402** before JSON/Pydantic validation; paid path unchanged; OpenAPI **POST** body schema preserved; no listing claim)
- v12.x x402scan public OpenAPI discovery filter (default **`/openapi.json`** hides **`/internal/*`**, **`/health`**, **`/webhooks/*`**; runtime unchanged; **`/contracts/risk-score`** remains documented; no listing claim)
- v12.x x402scan v1 schema alignment (**`accepts[0].network: base`**, top-level **`error`**, legacy **`network: eip155:8453`**; **POST** top-level + **`detail`**; **PAYMENT-REQUIRED** includes **`error`**; no listing claim)
- v12.x x402scan single OpenAPI operation (public **`/openapi.json`** documents **POST only** on **`/contracts/risk-score`**; **GET**/**HEAD**/**OPTIONS** runtime unchanged; no listing claim)
- v12.x x402scan POST body strict v1 (unpaid **POST** flat challenge same as **GET**, no **`detail`** wrapper; OpenAPI sample body; no listing claim)
- v12.x x402scan pure POST v1 body (unpaid **POST** returns only **x402Version**/**error**/**accepts**; **GET** legacy preserved; no listing claim)
- v12.x x402scan accepts strict schema (**`outputSchema.input`** on discovery **accepts**; no listing claim)
- v12.x x402scan runtime amount compatibility (restore **`accepts[0].amount`** = **`maxAmountRequired`** for x402scan **`check-endpoint`**; pure **POST** body preserved; no listing claim)
- v12.x x402scan v1 body-first discovery (omit **`PAYMENT-REQUIRED`** on **v1** **402** so @agentcash/discovery parses JSON body; **x-payment-info** on OpenAPI **POST**; no listing claim)
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

- tests passed count: 611 (baseline at v11.0 status report authoring; re-run `pytest -q` for current)
- npm package version: `@beezshield/sentinel@0.1.0`
- current HEAD: `97b39e3`
- outreach targets: 20 planned (T01-T20 structure)
- builders contacted: 3 verified (x402 Foundation / x402, Coinbase AgentKit, elizaOS / eliza issue outreach logged)
- community/adjacent outreach signals: 5 observed (AgentKit thread + Sentinel/Mycelium documentation alignment + ATCP boundary-layer discussion signal + Mycelium community documentation contribution signal + Mycelium post_action_trail field validation signal; no official AgentKit/x402/Stripe/Mycelium/ATCP acceptance)
- outreach follow-ups sent: 1 verified (AgentKit local demo follow-up comment)
- SDK installs reported: not tracked yet (add when reliable source exists)
- integrations started: 0 verified (no integration proof from outreach issue closures)
