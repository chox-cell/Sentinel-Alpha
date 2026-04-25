# Agentic Market Listing Pack v1.0

## Purpose
Provide a strict, machine-readable market listing artifact for external agent discovery without changing Sentinel Alpha runtime behavior.

## Files
- `agentic-market.json` (repo root): external listing manifest
- `docs/01_manifest/manifest.json`: internal discovery manifest served by `/internal/manifest`

## Canonical Listing Values
- `name`: `Sentinel Alpha`
- `category`: `execution_fidelity_layer`
- `endpoint`: `/contracts/risk-score`
- `pricing_tiers`:
  - `basic`: `0.02`
  - `executive`: `0.05`
  - `premium`: `0.10`
  - `priority`: `0.15`
- `payment`: `x402`
- `network`: `eip155:8453`
- `outputs`: `score`, `confidence`, `action`, `emergency_signal`, `attestation`
- `supported_chains`: `base`
- `modes`: `scan`, `webhook`, `dry_run`
- `identity`: `did:sentinel-alpha:local`
- `engine`: `Mycelium Engine`
- `agent_system`: `Sentinel Cells`

## Safety Notes
- No secrets are included in the listing.
- No runtime payment or scoring behavior is changed by this pack.
- `/contracts/risk-score` request/response schema remains unchanged.
