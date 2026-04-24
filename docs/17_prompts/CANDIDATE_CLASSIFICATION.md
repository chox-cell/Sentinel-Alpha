# CANDIDATE CLASSIFICATION v0.1

Goal:
- Classify reduced QuickNode candidates before evaluation to prioritize high-value security signals and skip low-value compute.

Implementation:
- `services/scout_cell/candidate_classifier.py`
- function: `classify_candidate(candidate: dict) -> dict`

Classifier output:
- `candidate_type`
- `priority_score` (0-100)
- `should_evaluate`
- `reason`

Rules:
- `first_liquidity` => priority 100, evaluate
- `new_token_candidate` => priority 90, evaluate
- Transfer topic => `token_transfer`, priority 40, skip unless `context.force_evaluate=true`
- Approval topic => `approval`, priority 20, skip
- Unknown => priority 10, skip

Hunter integration:
- classify each candidate
- evaluate only when `should_evaluate=true`
- summary includes `candidates`, `evaluated`, `skipped`, `results`

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public response schema unchanged.
