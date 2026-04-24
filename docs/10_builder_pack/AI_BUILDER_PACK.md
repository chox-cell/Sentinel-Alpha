# AI Builder Pack v1.8

## Project
Sentinel Alpha

## System Type
Execution Fidelity Layer for Bots and Agents

## Engine
Mycelium Engine

## Agents
Sentinel Cells:
- Scout Cell
- T-Cell
- B-Cell
- Signal Cell
- Synapse Cell

## Core Endpoint
POST /contracts/risk-score

## Current Code State
Real Signals v0 is active.

Current flow:
Request/Webhook
→ extract_signals
→ compute_score
→ compute_confidence
→ decide
→ classify_threat
→ build_attestation
→ return Executive JSON

## Files to respect
- services/signals/extractor.py
- services/mycelium_engine/engine.py
- services/risk_service/service.py
- services/attestation_layer/attestation.py
- apps/api/main.py
- apps/webhooks/quicknode.py

## Builder Mission
Improve Sentinel Alpha without changing identity.

## Allowed Next Builds
1. tests
2. bytecode scanner
3. QuickNode event normalizer
4. simulation stub
5. deployer profile stub
6. cache metrics
7. real docs update

## Forbidden
- rename
- dashboard
- architecture rewrite
- endpoint change
