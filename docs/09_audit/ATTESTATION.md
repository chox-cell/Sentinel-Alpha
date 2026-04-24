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

## Current Engine Version
mycelium-wrsi-0.2

## Rule
Every /contracts/risk-score response must include attestation.
