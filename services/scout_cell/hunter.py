import uuid
import json

from shared.utils.logger import log_event
from shared.config.limits import get_ingestion_limits
from services.scout_cell.candidate_classifier import classify_candidate
from services.dlq.dead_letter import write_dlq
from services.risk_service.service import evaluate_contract
from services.scout_cell.event_reducer import reduce_quicknode_event

def handle_new_contract(event: dict):
    limits = get_ingestion_limits()
    payload_size_bytes = _estimate_payload_bytes(event)
    max_eval = limits["max_evaluations_per_webhook"]
    max_candidates = limits["max_candidates_per_webhook"]
    warn_threshold = limits["max_payload_bytes_warn"]
    hard_threshold = limits["max_payload_bytes_hard"]

    if payload_size_bytes > hard_threshold:
        log_event(
            "cost_warning",
            {
                "payload_size_bytes": payload_size_bytes,
                "threshold_type": "hard",
                "max_payload_bytes_hard": hard_threshold,
            },
        )
        return {
            "status": "ignored",
            "reason": "payload_too_large",
            "candidates": 0,
            "evaluated": 0,
            "skipped": 0,
            "results": [],
        }

    if payload_size_bytes > warn_threshold:
        log_event(
            "cost_warning",
            {
                "payload_size_bytes": payload_size_bytes,
                "threshold_type": "warn",
                "max_payload_bytes_warn": warn_threshold,
            },
        )

    candidates = reduce_quicknode_event(event)[:max_candidates]
    results = []
    evaluated_count = 0
    skipped_count = 0

    for candidate in candidates:
        classification = classify_candidate(candidate)
        if classification["should_evaluate"] and evaluated_count >= max_eval:
            classification = {
                **classification,
                "should_evaluate": False,
                "reason": "evaluation_cap_reached",
            }

        if not classification["should_evaluate"]:
            skipped_count += 1
            results.append(
                {
                    "contract_address": candidate["contract_address"],
                    "chain": candidate["chain"],
                    "event_type": candidate["event_type"],
                    "transaction_hash": candidate["transaction_hash"],
                    "block_number": candidate["block_number"],
                    "status": "skipped",
                    "classification": classification,
                }
            )
            continue

        try:
            evaluated_count += 1
            body = evaluate_contract(
                contract_address=candidate["contract_address"],
                chain=candidate["chain"],
                context=candidate["context"],
            )
            results.append(
                {
                    "contract_address": candidate["contract_address"],
                    "chain": candidate["chain"],
                    "event_type": candidate["event_type"],
                    "transaction_hash": candidate["transaction_hash"],
                    "block_number": candidate["block_number"],
                    "status_code": 200,
                    "classification": classification,
                    "body": body,
                }
            )
        except Exception as e:
            trace_id = str(uuid.uuid4())
            dlq_record = write_dlq(
                {
                    "trace_id": trace_id,
                    "source": "quicknode",
                    "reason": "candidate_evaluation_failed",
                    "candidate": candidate,
                    "error": str(e),
                }
            )
            results.append(
                {
                    "trace_id": trace_id,
                    "contract_address": candidate["contract_address"],
                    "chain": candidate["chain"],
                    "event_type": candidate["event_type"],
                    "transaction_hash": candidate["transaction_hash"],
                    "block_number": candidate["block_number"],
                    "status": "error",
                    "message": str(e),
                    "classification": classification,
                    "dlq_created_at": dlq_record["created_at"],
                }
            )

    summary = {
        "status": "ok",
        "candidates": len(candidates),
        "evaluated": evaluated_count,
        "skipped": skipped_count,
        "results": results,
    }
    log_event(
        "quicknode_reduced",
        {
            "candidate_count": len(candidates),
            "evaluated_count": evaluated_count,
            "skipped_count": skipped_count,
            "block_number": (candidates[0]["block_number"] if candidates else None),
        },
    )
    return summary


def _estimate_payload_bytes(payload: dict) -> int:
    try:
        return len(json.dumps(payload or {}, ensure_ascii=False).encode("utf-8"))
    except Exception:
        return len(str(payload).encode("utf-8"))
