# Identity & Attestation v0.1

## Purpose
Bind each decision attestation to local Sentinel Alpha identity metadata and a deterministic signature stub for audit continuity.

## Modules
- `services/identity/agent_identity.py`
- `services/attestation_layer/attestation.py`

## Identity API
- `get_agent_identity() -> dict`

Identity fields:
- `agent_name`
- `engine_name`
- `agent_system`
- `primary_endpoint`
- `identity_version`
- `did`

## Attestation fields
Existing:
- `decision_fingerprint`
- `engine_version`
- `signed_at`

Added in v0.1:
- `agent_identity`
- `attestation_version` (`attestation-0.1`)
- `signature`

## Signature stub
- Deterministic local stub:
  - `sha256(decision_fingerprint + did + engine_version)`
- No private key signing yet.

## Constraint
- Top-level `/contracts/risk-score` response schema remains unchanged.
