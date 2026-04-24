# Agentic Discovery Manifest Hardening v0.1

## Purpose
Provide a strict machine-readable discovery contract so bots and agentic clients can programmatically understand Sentinel Alpha capabilities and integration constraints.

## Manifest file
- `docs/01_manifest/manifest.json`

## Internal discovery endpoint
- `GET /internal/manifest`
- Returns the manifest JSON directly.

## Guaranteed manifest identity
- `name`: Sentinel Alpha
- `engine`: Mycelium Engine
- `agent_system`: Sentinel Cells
- `primary_endpoint`: `/contracts/risk-score`

## Runtime and policy constraints
- First 60 minutes security wedge
- Machine-native distribution posture
- No dashboard expansion
- No compliance suite scope

## Compatibility note
- Public risk response schema remains unchanged.
- `/contracts/risk-score` remains unchanged.
