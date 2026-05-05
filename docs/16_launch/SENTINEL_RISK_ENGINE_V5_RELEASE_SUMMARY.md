# Sentinel Risk Engine v5 release summary

This release summary describes what Sentinel Alpha v5 risk intelligence does today, what is boundary-only, and what remains roadmap.

## 1) What is real today

- `/contracts/risk-score` API is live and returns deterministic risk decisions.
- Access is x402-gated.
- npm SDK is live: `@beezshield/sentinel@0.1.0`.
- Asset classification metadata is returned in response metadata.
- Source/proxy/admin conservative signals are returned as metadata.
- ERC20 heuristic boundary is active as conservative metadata/signals.
- NFT/Zora heuristic boundary is active as conservative metadata/signals.
- Simulation adapter boundary is present (interface and status fields).
- Risk explanation metadata is present (`security_explanation`).
- Chain support metadata is present (Base primary, others conservative).
- Intent alignment policy assistance metadata is present.
- Mempool/MEV boundary metadata is present.

## 2) What is boundary-only today

- Boundary-only components are present but not fully wired to deep external providers by default.
- Simulation is not live by default.
- Mempool/MEV monitoring is not live by default.
- ABI/source external lookup is not fully wired.
- No paid provider enabled by default.
- Honeypot confirmation remains unknown unless a future adapter provides evidence.

## 3) What is not claimed

- No safety-outcome guarantee.
- No all-contract coverage.
- No broad bytecode-trap coverage claim.
- No deterministic honeypot-confirmation guarantee.
- No claim of MEV blocking.
- No prompt-injection prevention.
- No complete intent-verification claim.
- No automatic x402 settlement.

## 4) What unlocks next

- ABI/source provider integration.
- verified source check rollout.
- proxy implementation resolver.
- local/managed Postgres when needed for durable normalized history.
- simulation provider integration after revenue/demand gate.
- mempool feed integration after budget gate.

## 5) Public-safe positioning

- fallback-aware pre-execution risk decision layer
- asset-aware risk metadata
- simulation-readiness and mempool-readiness boundaries
- uncertainty-aware explanations
