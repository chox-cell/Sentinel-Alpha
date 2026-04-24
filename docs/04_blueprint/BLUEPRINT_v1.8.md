# Sentinel Alpha Blueprint v1.8

## Identity
Sentinel Alpha is the Execution Fidelity Layer for Bots and Agents.

## Core Output
Score + Confidence + Action + Emergency Signal + Audit Attestation

## Current Code State
Real Signals v0 is active.

## Current Endpoint
POST /contracts/risk-score

## Current Webhook
POST /webhooks/quicknode

## Current Engine
Mycelium Engine:
- compute_score
- compute_confidence
- decide
- classify_threat

## Current Signal Extractor
services/signals/extractor.py

Signals:
- invalid_address
- unverified_address_shape
- new_deploy
- first_liquidity
- owner_privileges
- liquidity_unlocked
- oracle_dislocation
- simulation_revert
- bad_cluster
- shadow_link
- bad_bot_activity
- insufficient_data

## Current Moat Foundations
- Outcome Memory v0.1 active
- Outcome Verifier v0.1 active
- Adaptive Phi Stub v0.1 active
- Shadow Link v0.1 active
- Policy Calibration v0.1 active
- Cache Metrics v0.1 active
- Attestation active
- Redis cache active
- Webhook ingestion active

## Not Built Yet
- bytecode scan
- real deployer graph
- live liquidity scan
- real simulation
- real x402 settlement
- QuickNode signature verification

## Next Build Priority
1. tests
2. docs sync
3. bytecode scanner stub
4. QuickNode payload normalizer
5. deployer profile stub
