# Sentinel Scanner Engine v0

## Current Status
Sentinel Alpha now uses a scanner engine boundary (`services/scanner_engine`) as a safe foundation for future chain-read evolution.

## What Is Real Now
- Deterministic risk scoring and action decisions through current signal extraction and Mycelium engine logic.
- Stable `/contracts/risk-score` response contract used by existing clients.
- x402 payment middleware and billing propagation path remains active.

## What Is Fallback
- Viem and WhatsABI integrations are represented by readiness adapters only.
- **Chain read adapter v0** (`chain_read_adapter.py`): JSON-RPC **`eth_getCode` only**, when **`SENTINEL_CHAIN_READ_ENABLED=true`** **and** `BASE_RPC_URL` is set for a supported chain (currently **base**). **Chain reads default off**, even if `BASE_RPC_URL` exists for payments or other subsystems—so missing or disabled reads **degrade gracefully** without claiming live deep analysis.
- If the provider URL is unset, reads are opted out, the chain is unsupported, or RPC returns errors, **`/contracts/risk-score` still returns**: evaluation continues with degraded `meta.chain_read` and signal hints—**no crashing the public endpoint**.
- **`meta.fallback_mode`** and **`meta.chain_read`** summarize posture (`chain_read_status`, `account_type`, `adapter_mode`, `contract_code_available`). Do **not** treat this as confirmation of deep WhatsABI or bytecode semantics yet.

## What Is Not Live Yet
- Deep bytecode intelligence, ABI decoding, or WhatsABI-driven analysis (**not live**; v0 reads detect bytecode **presence** only when the chain-read adapter is explicitly enabled).
- Full ABI interpretation through WhatsABI readiness beyond today’s scaffolding.
- Production-grade chain data enrichment pipeline in the scanner boundary.

## Path To Viem/WhatsABI Integration
1. Keep JSON-RPC/Viem-aligned boundaries in TS workers or reuse this adapter contract from SDKs where appropriate.
2. Map additional read results into new/validated signals without changing `/contracts/risk-score` top-level keys.
3. Keep endpoint compatibility while increasing confidence only when real data is available.
4. Add adapter integration tests per network/provider failure mode.

See `docs/16_launch/SENTINEL_CHAIN_READ_ADAPTER_V0.md` for chain-read specifics.
