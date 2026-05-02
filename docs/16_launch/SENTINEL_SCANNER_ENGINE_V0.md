# Sentinel Scanner Engine v0

## Current Status
Sentinel Alpha now uses a scanner engine boundary (`services/scanner_engine`) as a safe foundation for future chain-read evolution.

## What Is Real Now
- Deterministic risk scoring and action decisions through current signal extraction and Mycelium engine logic.
- Stable `/contracts/risk-score` response contract used by existing clients.
- x402 payment middleware and billing propagation path remains active.

## What Is Fallback
- Viem and WhatsABI integrations are represented by readiness adapters only.
- If providers/config are unavailable, risk evaluation does not crash and returns fallback decision flow.
- `meta.fallback_mode` indicates adapter availability posture.

## What Is Not Live Yet
- Full live bytecode intelligence through Viem reads.
- Full ABI interpretation through WhatsABI.
- Production-grade chain data enrichment pipeline in the scanner boundary.

## Path To Viem/WhatsABI Integration
1. Replace readiness adapters with real chain-read calls behind same interface.
2. Map real contract read results into new/validated signals.
3. Keep endpoint compatibility while increasing confidence only when real data is available.
4. Add adapter integration tests per network/provider failure mode.
