# QUICKNODE EVENT REDUCER v0.2

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
- Support top-level `matchingReceipts` and nested `matchingReceipts[i].logs`.
- For each receipt:
  - use `contractAddress` as `new_token_candidate` when present.
  - use each `log.address` as event candidate.
  - transaction hash: log first, receipt fallback.
  - block number: log first, receipt fallback.
- Topic mapping:
  - Transfer topic0 (`0xddf252ad...`) => `contract_event`
  - Mint / IncreaseLiquidity / Pool-liquidity-like topics => `first_liquidity`
- Candidate context includes:
  - `source`, `receipt_index`, `log_index`, `transaction_hash`, `block_number`, `topic0`, `receipt_from`, `receipt_to`
- Use reducer first in Scout Cell hunter and evaluate each candidate.
- Return summary: `status`, `candidates`, `results`.
- Keep logs safe: log payload size + candidate count + block number only.

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public risk response schema unchanged.
