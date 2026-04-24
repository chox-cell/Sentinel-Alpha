# Adaptive Phi Stub v0.1

## Purpose
Adaptive Phi provides a local learning stub that reads Outcome Memory and updates per-signal multipliers for future engine calibration cycles.

## Module
- `services/mycelium_engine/phi.py`

## State Storage
- `logs/phi_state.json`

## API
- `load_phi_state() -> dict`
- `save_phi_state(state: dict) -> None`
- `update_phi_from_outcomes(records: list) -> dict`

## Default State
- Every known signal multiplier starts at `1.0`.

## Stub Rules
- `BLOCK` or `EXIT_NOW` with `score >= 85`:
  - increment triggered signal multipliers slightly
  - cap at `1.5`
- `ALLOW` with `threat_class != normal`:
  - increment triggered signal multipliers more strongly
  - cap at `1.75`
- `ALLOW` with `threat_class == normal`:
  - no change

## Integration Boundary
- Phi is NOT applied to live scoring yet.
- Worker computes and persists state only.
