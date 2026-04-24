# Attestation Layer v1.8

## Purpose
Every decision must include proof of audit.

## Current File
services/attestation_layer/attestation.py

## Current Attestation Fields
- decision_fingerprint
- engine_version
- signed_at

## Current Engine Version
mycelium-wrsi-0.2

## Rule
Every /contracts/risk-score response must include attestation.
