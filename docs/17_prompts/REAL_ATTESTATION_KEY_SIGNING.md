# REAL ATTESTATION KEY SIGNING v0.1

Goal:
- Add local real-key attestation signing while preserving stub fallback and public schema compatibility.

Implementation:
- `services/attestation_layer/key_signing.py`
- `services/attestation_layer/attestation.py`
- `GET /internal/attestation/status`

Functions:
- `get_attestation_private_key() -> str | None`
- `get_attestation_public_key() -> str | None`
- `sign_attestation_message(message: str) -> str`
- `get_signing_mode() -> "stub" | "real_key"`

Rules:
- If private key missing:
  - signing mode `stub`
  - deterministic sha256 signature behavior
- If private key present:
  - signing mode `real_key`
  - local HMAC-SHA256 signature
  - signature format: `hmac-sha256:<hex>`

Security:
- Never expose private/public key values in responses.
- Status endpoints expose booleans only.
