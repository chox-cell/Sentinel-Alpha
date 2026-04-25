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
- Outcome States v0.1 active
- Adaptive Phi Stub v0.1 active
- Phi Learning Rate Calibration v0.1 active
- Shadow Link v0.1 active
- Policy Calibration v0.1 active
- Cache Metrics v0.1 active
- QuickNode Signature Verification v0.1 active
- Latency Shield v0.1 active
- Identity & Attestation v0.1 active
- Real QuickNode Webhook Dry Run v0.1 active
- Agentic / Discovery Manifest Hardening v0.1 active
- Real QuickNode Live Setup v0.1 active
- Real QuickNode Live Connection v0.1 active
- QuickNode Event Reducer v0.1 active
- QuickNode Event Reducer matchingReceipts v0.2 active
- Payload Inspector v0.1 active
- DLQ + Replay v0.1 active
- Candidate Classification v0.1 active
- Cost / Volume Control v0.1 active
- Real Identity / ERC-8004 Planning v0.1 active
- Real Attestation Key Signing v0.1 active
- x402 Payments Planning + Env Lock v0.1 active
- x402 Real Payment Middleware v0.1 active
- x402 Real Payment Challenge v0.2 active
- x402 Real Payment Verification v0.4 active
- x402 Replay Protection v0.5 active
- x402 Settlement Logging v0.6 active
- x402 On-chain USDC Verification Adapter v0.7 active
- Base USDC Receipt Verification v0.9 active
- Mock Onchain Verification v0.9.1 active
- Agentic Market Listing Pack v1.0 active
- SDK Quickstart Pack v1.1 active
- Public Launch Docs Pack v1.2 active
- Pre-launch Hardening Pack v1.3 active
- Launch Env Finalizer v1.4 active
- Release Candidate Freeze v1.5 active
- Production Guard Pack v1.6 active
- Controlled Real Payment Test Plan v0.8 active
- Attestation active
- Redis cache active
- Webhook ingestion active

## Not Built Yet
- bytecode scan
- real deployer graph
- live liquidity scan
- real simulation
- real x402 settlement

## Next Build Priority
1. tests
2. docs sync
3. bytecode scanner stub
4. QuickNode payload normalizer
5. deployer profile stub
