# ADAPTIVE PHI STUB v0.1

Goal:
- Read Outcome Memory records and produce updated local signal multipliers for future scoring calibration.

Implementation:
- `services/mycelium_engine/phi.py`
- `workers/phi_updater/run.py`

Functions:
- `load_phi_state() -> dict`
- `save_phi_state(state: dict) -> None`
- `update_phi_from_outcomes(records: list) -> dict`
- `get_learning_rate() -> float`

State file:
- `logs/phi_state.json`

Rules:
- Default multiplier for each signal: `1.0`
- Default learning rate eta: `0.01`
- `PHI_LEARNING_RATE` env overrides eta; invalid values fallback to `0.01`
- `BLOCK` or `EXIT_NOW` with `score >= 85`: slight increase using eta (max `1.25`)
- `ALLOW` with non-normal threat class: stronger increase using eta (max `1.25`)
- `ALLOW` with `normal`: unchanged
- conservative floor: min `0.75`

Constraint:
- Do not apply Phi multipliers to live scoring yet.
- No public schema changes.
- Keep `/contracts/risk-score` unchanged.
