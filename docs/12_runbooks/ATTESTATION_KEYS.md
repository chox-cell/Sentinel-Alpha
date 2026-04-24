# Attestation Keys Runbook v0.1

## Purpose
Enable local real-key attestation signing safely while preserving fallback stub mode.

## Environment
- `SENTINEL_ATTESTATION_PRIVATE_KEY` (optional)
- `SENTINEL_ATTESTATION_PUBLIC_KEY` (optional)

## Modes
- Stub mode (default):
  - no private key configured
  - signature format: `sha256:<hex>`
- Real-key mode:
  - private key configured
  - signature format: `hmac-sha256:<hex>`

## Verification endpoint
- `GET /internal/attestation/status`
- Returns:
  - `attestation_version`
  - `signing_mode`
  - `public_key_configured`
  - `private_key_configured`

No key values are returned.

## Constraints
- No changes to `/contracts/risk-score`
- No public response schema changes
