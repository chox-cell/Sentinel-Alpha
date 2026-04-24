# QUICKNODE PAYLOAD NORMALIZER v0.1

Purpose:
- Normalize QuickNode webhook payloads into one internal shape for Scout Cell.

Accepted payload shapes:
- `{"contract_address": "...", "chain": "base"}`
- `{"address": "...", "chain": "base"}`
- `{"event_type": "...", "contract_address": "..."}`
- Nested wrappers: `{"data": {...}}` or `{"event": {...}}`

Normalizer output:
```python
{
  "contract_address": string | None,
  "chain": string,
  "event_type": string,
  "context": dict
}
```

Normalization defaults:
- `chain`: `"base"` when missing
- `event_type`: `"new_deploy"` when missing
- `context`: normalized payload map (includes `event_type`)

Implementation:
- `services/scout_cell/quicknode_normalizer.py`
- `normalize_quicknode_payload(payload: dict) -> dict`

Integration:
- `services/scout_cell/hunter.py` calls normalizer first, then calls `evaluate_contract` directly.
- Public API schema is unchanged.
