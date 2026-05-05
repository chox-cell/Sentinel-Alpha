# Sentinel risk capability matrix (v5.0)

Internal capability map for product, GTM, and investor consistency.
This document separates **live**, **fallback**, **roadmap**, and **forbidden** claims for Sentinel Alpha risk intelligence.

## 1) Current live capabilities

Sentinel Alpha is a **pre-execution risk decision layer** with fallback-aware behavior.

- Accepts EVM contract addresses as input for risk decision requests.
- Validates address format before scoring paths.
- Can classify address state through chain-read adapter when enabled:
  - bytecode exists (contract),
  - EOA (no bytecode),
  - unknown/provider unavailable.
- If provider is unavailable, the system returns fallback-aware behavior instead of pretending deep onchain analysis.
- Exposes a generic risk decision API for contract execution gating.
- API access is x402-gated.
- npm SDK is live: `@beezshield/sentinel` (install: `npm install @beezshield/sentinel`).
- AgentKit-style example is available in-repo.

Current limitation statement (must remain true in public copy):
- Sentinel **does not deeply analyze all contract types** today.
- Sentinel **does not guarantee honeypot detection** today.

## 2) Contract type coverage

| Contract/target type | Current support | Confidence level | Current public-safe wording | Roadmap need |
|---|---|---|---|---|
| EOA | Live: identifiable as non-contract when chain-read is available | Medium | "EOA vs contract distinction available when provider data is available." | Better chain redundancy and confidence details |
| Generic contract with bytecode | Live: bytecode presence classification and generic risk decision | Medium | "Contract risk signal is available for execution gating." | Deeper semantic bytecode analysis |
| Unknown / provider unavailable | Live fallback | Low | "Fallback-aware confidence applies when provider data is unavailable." | Multi-provider failover and degraded-mode explanations |
| ERC20 basic | Partial/generic | Low-Medium | "Generic contract risk signal available; token-specific depth is roadmap." | Token semantic checks and transfer behavior analysis |
| New deployments | Partial/generic | Low | "New contracts can be scored with limited history context." | Fresh-deploy heuristics and launch-risk models |
| Zora creator coins | Partial/generic | Low | "Zora creator coins currently receive generic contract-level assessment." | Zora-specific parsing and behavior heuristics |
| Honeypots | Not deeply supported today | Low | "Does not guarantee honeypot detection; deeper simulation is roadmap." | Buy/sell simulation engine and heuristics |
| Upgradeable proxies | Limited detection | Low | "Proxy-aware depth is limited today." | Robust proxy detection + implementation tracing |
| DeFi pools | Partial/generic | Low | "Pool contracts are currently evaluated via generic signal paths." | Pool/router protocol classifiers |
| Routers | Partial/generic | Low | "Router contracts are not yet deeply profiled in v0." | Router recognition + risk policy rules |
| NFT contracts | Partial/generic | Low | "NFT contracts currently use generic contract scoring paths." | ERC721/ERC1155-specific risk features |
| Custom malicious bytecode | Limited | Low | "Advanced bytecode-trap coverage is roadmap." | Opcode/selector pattern engine + simulation coupling |

## 3) Asset coverage

| Asset type | Current detection status | Desired signals | Risk examples | Roadmap priority |
|---|---|---|---|---|
| ERC20 token | Partial/generic | verified source check, mint/blacklist/tax behavior, holder concentration | hidden tax logic, admin abuse | High |
| ERC721 NFT | Partial/generic | metadata integrity, operator/admin controls, transfer restrictions | metadata rug, freeze controls | Medium |
| ERC1155 NFT | Partial/generic | multi-token permission map, mint controls, URI mutability | selective freeze/mint abuse | Medium |
| Zora creator coin | Partial/generic | launch config decoding, transfer behavior, admin controls | creator-coin specific transfer surprises | High |
| LP/pool token | Limited | pair composition, liquidity depth, pool age, lock signals | shallow liquidity / rug risk | High |
| Router contract | Limited | router/pair recognition, routing permissions, known router mapping | malicious routing / spoof router | High |
| Vault contract | Limited | strategy transparency, withdrawal controls, admin powers | withdrawal lock / strategy risk | Medium-High |
| Wallet/EOA | Basic (EOA vs contract) | transaction pattern context, sanction/risk overlays (policy-dependent) | compromised operator wallet | Medium |
| Unknown asset | Fallback | confidence explanation + required manual review signal | unclassified execution target | High |

## 4) Required v1 signals

Required v1 enrichment signals for moving beyond v0 generic coverage:

- verified source check
- ABI availability
- proxy detection
- implementation address extraction
- owner/admin permissions mapping
- pause/blacklist/maxTx/maxWallet flags
- mint ability and supply control flags
- ERC20 tax/transfer behavior analysis
- honeypot buy/sell simulation
- router/pair recognition
- malicious selector heuristics
- confidence explanation per decision
- chain-specific support matrix (per network/provider quality)

## 5) Safe public wording

Use wording that is accurate under current capability:

- "pre-execution risk decision layer"
- "contract risk signal"
- "fallback-aware confidence"
- "deeper bytecode and simulation checks are roadmap"

## 6) Forbidden wording

Do not use these claims in public or investor-facing material:

- "catches nearly all bytecode-level traps"
- "guarantees safety outcomes"
- "detects every honeypot"
- "covers every contract type"
- "AgentKit provider live"
- "automatic x402 settlement"
