# QUICKNODE PAYLOAD INSPECTOR v0.1

Goal:
- Safely inspect large unknown QuickNode payload structures when reducer output is empty.

Implementation:
- `services/scout_cell/payload_inspector.py`
- function: `inspect_quicknode_payload(payload: dict) -> dict`

Inspector output fields:
- `top_level_type`
- `top_level_keys`
- `data_type`
- `data_keys`
- `possible_list_paths`
- `receipt_count_guess`
- `log_count_guess`
- `sample_paths_only`

Runtime trigger:
- In webhook flow, if `candidate_count == 0` and payload size > 100000 bytes:
  - log `quicknode_payload_inspected`
  - include inspection summary only
  - do not log raw payload

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public response schema unchanged.
