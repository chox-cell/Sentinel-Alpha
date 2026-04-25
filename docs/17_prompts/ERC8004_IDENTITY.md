# ERC-8004 Identity (Prompt Pack)

## Goal

Guide implementation work for real ERC-8004 agent identity for Sentinel Alpha while keeping current local DID and stub paths stable.

## Constraints

- Do not rename Sentinel Alpha, Mycelium Engine, or Sentinel Cells.
- Do not change `/contracts/risk-score` or successful public response schema keys in this planning pack.

## Source of truth for planning

- Contract plans:
  - `docs/13_contracts/ERC8004_IDENTITY_PLAN.md`
  - `docs/13_contracts/ATTESTATION_UPGRADE_PLAN.md`
- Machine-readable planning snapshot: `identity-manifest.json`

## Manifest snapshot

- `current_identity`: `did:sentinel-alpha:local`
- `target_identity`: `erc8004`
- `status`: `planned`
- `release_target`: `v1.8`

## Implementation hints

- Extend `services/identity/` and env configuration only after contract review; gate on `SENTINEL_IDENTITY_MODE` and `SENTINEL_ERC8004_CONTRACT_ADDRESS`.
- Keep `GET /internal/identity/status` safe (no secrets in output).
