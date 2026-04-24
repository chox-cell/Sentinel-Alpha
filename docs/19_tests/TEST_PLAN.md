# Sentinel Alpha Test Plan v1.8

## Required Tests

### 1. Health
GET /health returns ok true.

### 2. Invalid Address
Short EVM-like address should return:
- invalid_address = 1
- action = BLOCK
- score = 100

### 3. Liquidity Rug
Context:
- first_liquidity
- liquidity_unlocked
- bad_cluster

Expected:
- action = EXIT_NOW
- threat_class = liquidity_rug

### 4. Oracle Dislocation
Context:
- new_deploy
- oracle_dislocation
- simulation_revert

Expected:
- action = EXIT_NOW
- threat_class = oracle_dislocation

### 5. Normal New Deploy
Valid address + only new_deploy.

Expected:
- action = ALLOW
- low score
- confidence around 0.6

### 6. Webhook
POST /webhooks/quicknode should return status ok.

## Do Not Test Yet
- real x402
- real QuickNode stream
- live simulation
