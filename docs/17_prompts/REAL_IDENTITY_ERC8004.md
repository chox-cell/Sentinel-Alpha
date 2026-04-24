# REAL IDENTITY / ERC-8004 PLANNING v0.1

Goal:
- Prepare identity architecture for future real-key and ERC-8004 integration without changing live API schema.

Implementation:
- `services/identity/identity_config.py`
- `GET /internal/identity/status`

Function:
- `get_identity_status() -> dict`

Output fields:
- `identity_mode`
- `did`
- `agent_name`
- `engine_name`
- `attestation_version`
- `erc8004_enabled`
- `real_key_enabled`

Environment:
- `SENTINEL_IDENTITY_MODE` (default `local_stub`)
- `SENTINEL_AGENT_DID` (default `did:sentinel-alpha:local`)
- `SENTINEL_ERC8004_CONTRACT_ADDRESS` (optional)
- `SENTINEL_ATTESTATION_PUBLIC_KEY` (optional)

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public response schema unchanged.
- Do not introduce real private key material.
