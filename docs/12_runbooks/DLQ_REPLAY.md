# DLQ + Replay Runbook v0.1

## Purpose
Provide resilient webhook ingestion by storing failed candidate evaluations in a dead-letter queue and replaying them later.

## Storage
- DLQ file: `logs/dlq.jsonl`
- Replay summaries: `logs/replay.jsonl`

## DLQ API
- `services/dlq/dead_letter.py`
  - `write_dlq(record: dict) -> dict`
  - `read_dlq(limit: int = 50) -> list[dict]`

Required DLQ fields:
- `trace_id`
- `source`
- `reason`
- `candidate`
- `error`
- `created_at`

## Replay worker
- `workers/replay_dlq/run.py`
- Reads recent DLQ records, retries evaluation, appends replay summaries.

## Internal status endpoint
- `GET /internal/dlq/status`
- Returns count estimate and DLQ path only (no secrets).

## Safety
- Failed candidates do not stop webhook processing for remaining candidates.
- No raw full webhook payloads stored in DLQ.
