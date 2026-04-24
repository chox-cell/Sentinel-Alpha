# IDENTITY & ATTESTATION v0.1

Goal:
- Enrich attestation with local agent identity metadata and deterministic signature stub while preserving public response shape.

Implementation:
- `services/identity/agent_identity.py`
- `services/attestation_layer/attestation.py`

Identity function:
- `get_agent_identity() -> dict`

Required identity fields:
- `agent_name`: `Sentinel Alpha`
- `engine_name`: `Mycelium Engine`
- `agent_system`: `Sentinel Cells`
- `primary_endpoint`: `/contracts/risk-score`
- `identity_version`: `identity-0.1`
- `did`: `did:sentinel-alpha:local`

Attestation requirements:
- Keep:
  - `decision_fingerprint`
  - `engine_version`
  - `signed_at`
- Add:
  - `agent_identity`
  - `attestation_version`: `attestation-0.1`
  - `signature`

Signature stub:
- `signature = sha256(decision_fingerprint + did + engine_version)`
- No real private key yet.
