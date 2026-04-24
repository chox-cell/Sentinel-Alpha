# Sentinel Alpha Profiler v0.1

## Purpose
Deployer profiling provides a deterministic stub layer for early behavioral risk inference.

## Module
- `services/profiler/deployer_profile.py`

## Output
`build_deployer_profile(...)` returns a profile map consumed by Signal Cell internals:
- `cluster_risk`
- `owner_privileges`
- `known_rug_deployer`

## Integration
- Called from `services/signals/extractor.py`
- Combined with Shadow Link Tracker to set existing signals only:
  - `bad_cluster`
  - `shadow_link`
  - `owner_privileges`

## Design Constraint
- No public API schema changes.
- No change to `/contracts/risk-score`.
