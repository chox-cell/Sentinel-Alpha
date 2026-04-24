# QUICKNODE EVENT REDUCER v0.1

Goal:
- Reduce large QuickNode receipts/log payloads into compact canonical event candidates before risk evaluation.

Implementation:
- `services/scout_cell/event_reducer.py`
- `reduce_quicknode_event(payload: dict) -> list[dict]`

Reducer output per candidate:
- `contract_address`
- `chain` (`base`)
- `event_type` (`contract_event` | `first_liquidity` | `new_token_candidate`)
- `transaction_hash`
- `block_number`
- `log_count`
- `context`

Rules:
- Ignore payloads with no useful contract address.
- Cap candidates at 50 per webhook.
- Use reducer first in Scout Cell hunter and evaluate each candidate.
- Return summary: `status`, `candidates`, `results`.
- Keep logs safe: log payload size + candidate count + block number only.

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public risk response schema unchanged.
