# Sentinel risk engine v5 roadmap (addendum)

Internal roadmap from v5.0 capability baseline toward asset + contract + execution risk intelligence.

## 1) v5 mission

Sentinel evolves from a generic contract risk-score endpoint into an asset + contract + execution risk decision engine, while preserving truthful confidence and fallback-aware behavior.

## 2) v5 roadmap table

| Version | Scope | Outcome target | Status |
|---|---|---|---|
| v5.0 Risk Capability Matrix | Capability truth map | Shared language for live/fallback/roadmap/forbidden claims | Defined |
| v5.1 Asset Classification Engine | Asset-type normalization (token/NFT/pool/router/vault/EOA/unknown) | Asset-aware risk signals | Roadmap (no-extra-cost target) |
| v5.2 Source / Proxy / Admin Signals | Source verification + admin-control extraction | Stronger structural risk context | Roadmap (no-extra-cost target) |
| v5.2.1 ERC-8004 Identity Signals | Identity-aware confidence modifiers | Better context confidence (not absolute verdict) | Roadmap |
| v5.3 ERC20 Risk Heuristics | Transfer/tax/mint/blacklist behavior checks | Better token execution safety signals | Roadmap (prefer cached/free reads first) |
| v5.4 NFT / Zora Asset Heuristics | ERC721/ERC1155/Zora parsing and controls | Better NFT and creator-coin risk context | Roadmap |
| v5.5 Simulation Adapter Boundary | Adapter contracts for simulation providers | Roadmap simulation checks with explicit limits | Roadmap (interface-first; no paid provider until demand) |
| v5.6 Explanation Engine | Confidence and signal provenance output | Clearer operator interpretation | Roadmap (no-extra-cost target) |
| v5.7 Chain Support Matrix | Per-chain/provider support declarations | Explicit chain-specific capability visibility | Roadmap (may require RPC budget) |
| v5.8 Intent Alignment Layer | Agent intent vs target capability comparison | Reduced mismatched execution attempts | Roadmap |
| v5.9 Mempool / MEV Signal Layer | Mempool/MEV context ingestion | Additional pre-trade/pre-execution context signals | Roadmap |

## 2.1) Cost discipline notes

- v5.1/v5.2 remain no-extra-cost on existing VPS + local stack.
- v5.3 should use cached/free chain reads where possible.
- v5.5 simulation adapter stays interface-first; no paid provider until demand.
- v5.6 explanation engine should not add paid infra.
- v5.7 chain support expansion may require explicit RPC budget approval.
- v6 provider rollout follows `SENTINEL_DATA_PROVIDER_STRATEGY.md` (local/free-first ladder).

## 3) Identity layer (ERC-8004)

- ERC-8004 identity can improve context confidence for risk interpretation.
- Registered identity is not a safety guarantee.
- Unregistered identity is not proof of malice.
- Identity signal should influence confidence bands, not absolute allow/deny certainty.

## 4) Intent alignment layer

- Intent alignment compares agent purpose/intent against target contract capabilities and permissions.
- This layer is roadmap, not live.
- It is useful for reducing mismatched execution flows (for example, wrong target class for agent objective).
- No claim of full intent verification today.

## 5) Mempool / MEV signal layer

- Mempool / MEV signal processing is roadmap.
- It requires external mempool and MEV data providers.
- Sentinel does not claim MEV prevention.
- Output is a signal to support decisions, not a deterministic guarantee.

## 6) Asset coverage scope (v5 direction)

v5 scope includes explicit coverage plans for:

- ERC20
- ERC721
- ERC1155
- Zora creator coins
- LP/pool tokens
- routers
- vaults
- EOA/wallet targets
- unknown assets

## 7) Safe claims

Use these claims for current-to-roadmap communication:

- pre-execution risk decision layer
- asset-aware risk signals
- fallback-aware confidence
- roadmap simulation checks

## 8) Forbidden claims

Do not use these as positive product claims:

- catches most bytecode-level traps
- detects all honeypots
- guaranteed protection
- covers all contract types
- prevents MEV
- AgentKit provider live
- automatic x402 settlement
