# Attestation Layer v1.8

## Purpose
Every decision must include proof of audit.

## Current File
services/attestation_layer/attestation.py

## Current Attestation Fields
- decision_fingerprint
- engine_version
- signed_at
- agent_identity
- attestation_version
- signing_mode
- signature

## Identity & Attestation v0.1
Identity metadata is embedded in each attestation:
- agent_name
- engine_name
- agent_system
- primary_endpoint
- identity_version
- did

Deterministic signature stub:
- `sha256(decision_fingerprint + did + engine_version)`
- No private key signing yet.

## Real Attestation Key Signing v0.1
- Signing mode is now explicit:
  - `stub` when no private key is configured
  - `real_key` when `SENTINEL_ATTESTATION_PRIVATE_KEY` is configured
- Real-key mode uses local HMAC-SHA256 signature:
  - `hmac-sha256:<hex>`
- Stub mode preserves deterministic sha256 behavior.
- Internal status endpoint:
  - `GET /internal/attestation/status`
  - returns mode and key presence booleans only (no key values).

## Current Engine Version
mycelium-wrsi-0.2

## Rule
Every /contracts/risk-score response must include attestation.
