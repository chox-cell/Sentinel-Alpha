# BUILD REAL SIGNALS MODE

Sentinel Alpha currently runs Real Signals v0.

Do not replace with mock_signals.

Current signal extractor:
- services/signals/extractor.py
- services/signals/validators.py

Current engine:
- services/mycelium_engine/engine.py

Current risk service:
- services/risk_service/service.py

Current output schema:
- api_version
- decision
- risk_metrics
- signals
- attestation
- latency
- meta
- billing

AI Builder must improve signals incrementally:
1. bytecode scan
2. deployer profile
3. liquidity state
4. simulation
5. oracle integrity

Do not rename:
- Sentinel Alpha
- Mycelium Engine
- Sentinel Cells
- /contracts/risk-score
