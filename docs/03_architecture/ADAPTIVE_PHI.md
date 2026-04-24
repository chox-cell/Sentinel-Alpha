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
- `get_learning_rate() -> float`

## Default State
- Every known signal multiplier starts at `1.0`.
- Default learning rate (`eta`) is `0.01`.

## Phi Learning Rate Calibration v0.1
- `PHI_LEARNING_RATE` controls adaptive increments.
- Invalid/missing values fallback to `0.01`.
- Live-safe conservative caps:
  - min multiplier `0.75`
  - max multiplier `1.25`

## Stub Rules
- `BLOCK` or `EXIT_NOW` with `score >= 85`:
  - increment triggered signal multipliers slightly using `eta`
  - cap at `1.25`
- `ALLOW` with `threat_class != normal`:
  - increment triggered signal multipliers more strongly using `eta`
  - cap at `1.25`
- `ALLOW` with `threat_class == normal`:
  - no change

## Integration Boundary
- Phi is NOT applied to live scoring yet.
- Worker computes and persists state only.
