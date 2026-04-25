# ERC-8004 Identity Plan (Contract)

## Purpose

Plan the upgrade from local stub identity (`did:sentinel-alpha:local`) to real ERC-8004 agent identity on Base without changing current runtime behavior of `/contracts/risk-score` or public response schema.

## Current state

- `SENTINEL_IDENTITY_MODE` defaults to `local_stub`.
- `SENTINEL_AGENT_DID` defaults to `did:sentinel-alpha:local`.
- `SENTINEL_ERC8004_CONTRACT_ADDRESS` optional; real ERC-8004 path gated when contract is set and mode is `erc8004`.

## Adapter stub v1.9 (runtime-safe, no chain calls)

- Module: `services/identity/erc8004_adapter.py`
- Env (defaults off): `ERC8004_ENABLED=false`, `ERC8004_REGISTRY_ADDRESS=`, `ERC8004_AGENT_ID=`
- `get_erc8004_status()` returns booleans and a planning status only (`planned` | `configured_not_registered` | `registered_unverified`); it does not verify on-chain identity and makes no external calls.
- `build_agent_identity_payload()` returns the same stable agent fields as the local identity stub plus an `erc8004_adapter` block for future wiring; it never embeds registry URLs or raw secrets.
- Internal: `GET /internal/identity/erc8004/status`

## Target state

- On-chain ERC-8004 registration or binding aligned with Sentinel Alpha agent semantics.
- `get_identity_status()` reflects `erc8004_enabled` when contract and mode are configured.
- Attestation and risk responses continue to use the same top-level schema keys.

## Non-goals (this pack)

- No rename of Sentinel Alpha, Mycelium Engine, or Sentinel Cells.
- No change to successful `/contracts/risk-score` response schema keys.

## References

- Root artifact: `identity-manifest.json`
- Prompt: `docs/17_prompts/ERC8004_IDENTITY.md`
- Attestation alignment: `docs/13_contracts/ATTESTATION_UPGRADE_PLAN.md`
