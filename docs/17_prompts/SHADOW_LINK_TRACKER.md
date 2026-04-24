# SHADOW LINK TRACKER v0.1

Purpose:
- Add deterministic deployer/profile intelligence into Real Signals v0 without changing the public API schema.

Components:
- `services/profiler/deployer_profile.py`
- `services/shadow_link_tracker/tracker.py`

Functions:
- `build_deployer_profile(contract_address, chain, context=None) -> dict`
- `compute_shadow_link_score(profile: dict) -> float`

Stub rules:
- If `context.bad_cluster=true` -> `cluster_risk=high`
- If `context.known_rug_deployer=true` -> `shadow_link_score >= 0.8`
- If `shadow_link_score >= 0.75` -> signal `shadow_link=1`
- If `cluster_risk=high` -> signal `bad_cluster=1`

Signal mapping constraints:
- Map only to existing signals:
  - `bad_cluster`
  - `shadow_link`
  - `owner_privileges`

Public schema:
- No new top-level response fields.
- `/contracts/risk-score` remains unchanged.
