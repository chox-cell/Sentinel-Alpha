# Real Identity / ERC-8004 Plan v0.1

## Purpose
Prepare Sentinel Alpha for real identity and ERC-8004-aligned attestation architecture without deploying contracts yet.

## Current mode
- Default identity mode is `local_stub`.
- Current DID default: `did:sentinel-alpha:local`.
- No private key material is stored in this phase.

## Planned identity modes
- `local_stub`
  - local deterministic identity metadata for development.
- `real_key`
  - off-chain real attestation public-key mode (future signing hardening).
- `erc8004`
  - on-chain identity anchor mode using configured ERC-8004 contract address.

## Environment controls
- `SENTINEL_IDENTITY_MODE`
- `SENTINEL_AGENT_DID`
- `SENTINEL_ERC8004_CONTRACT_ADDRESS`
- `SENTINEL_ATTESTATION_PUBLIC_KEY`

## Runtime visibility
- `GET /internal/identity/status`
  - returns current mode/status booleans only
  - does not expose secrets

## Constraints
- `/contracts/risk-score` unchanged
- Public response schema unchanged
- No real private key usage in v0.1
