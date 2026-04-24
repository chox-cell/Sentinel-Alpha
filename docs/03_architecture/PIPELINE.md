# Sentinel Alpha Pipeline v1.8

## Public API Path
Client/Bot
→ /contracts/risk-score
→ payment gate
→ evaluate_contract
→ extract_signals
→ Mycelium Engine
→ Attestation Layer
→ Executive JSON

## QuickNode Webhook Path
QuickNode
→ /webhooks/quicknode
→ Scout Cell
→ QuickNode Payload Normalizer v0.1
→ evaluate_contract
→ extract_signals
→ Mycelium Engine
→ Attestation Layer
→ Executive JSON

## Current Design Rule
Webhook must NOT call local API through HTTP.
It must call evaluate_contract directly to avoid self-call deadlock.

## Current Status
- API works
- Webhook works
- Real Signals v0 works
- Attestation works
