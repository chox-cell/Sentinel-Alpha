# DLQ + REPLAY v0.1

Goal:
- Add ingestion resilience by writing failed QuickNode candidate evaluations to DLQ and replaying later.

Implementation:
- `services/dlq/dead_letter.py`
- `workers/replay_dlq/run.py`
- `GET /internal/dlq/status`

DLQ requirements:
- append-only JSONL in `logs/dlq.jsonl`
- records include:
  - `trace_id`
  - `source`
  - `reason`
  - `candidate`
  - `error`
  - `created_at`

Replay requirements:
- read DLQ
- retry evaluation
- append replay summary to `logs/replay.jsonl`

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public response schema unchanged.
- Failed candidates must not break webhook processing.
