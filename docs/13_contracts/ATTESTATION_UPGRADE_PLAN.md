# Attestation Upgrade Plan (Contract)

## Purpose

Describe how attestation will evolve alongside ERC-8004 identity so audit bindings remain consistent when real agent identity is enabled.

## Current state

- Attestation version: `attestation-0.1` (see `identity-manifest.json` and `get_identity_status()`).
- Signing modes and key configuration documented under attestation services; no schema key renames planned for risk-score success payloads.

## Planned alignment with ERC-8004

- Bind attestation metadata to resolved ERC-8004 agent identity when `SENTINEL_IDENTITY_MODE=erc8004` and contract address is configured.
- Preserve existing attestation field names in API responses unless a separate versioned migration is approved.

## Non-goals (this pack)

- No runtime change to `/contracts/risk-score` or public response schema in this planning phase.

## References

- Identity plan: `docs/13_contracts/ERC8004_IDENTITY_PLAN.md`
- Identity manifest: `identity-manifest.json`
