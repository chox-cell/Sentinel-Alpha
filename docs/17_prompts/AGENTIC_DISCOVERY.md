# AGENTIC DISCOVERY MANIFEST HARDENING v0.1

Goal:
- Make Sentinel Alpha machine-discoverable via a strict JSON manifest and internal discovery endpoint.

Artifacts:
- `docs/01_manifest/manifest.json`
- `GET /internal/manifest`
- `docs/01_manifest/AGENTIC_DISCOVERY.md`

Manifest identity requirements:
- Sentinel Alpha
- Mycelium Engine
- Sentinel Cells
- `/contracts/risk-score`

Manifest contract includes:
- core endpoints
- payment mode/method
- versioning metadata
- supported chains
- decision outputs/actions
- operating modes
- pricing tiers
- constraints

Constraints:
- Do not modify `/contracts/risk-score`.
- Do not change public risk response schema.
