import uuid

from shared.utils.logger import log_event
from services.scout_cell.candidate_classifier import classify_candidate
from services.dlq.dead_letter import write_dlq
from services.risk_service.service import evaluate_contract
from services.scout_cell.event_reducer import reduce_quicknode_event

def handle_new_contract(event: dict):
    candidates = reduce_quicknode_event(event)
    results = []
    evaluated_count = 0
    skipped_count = 0

    for candidate in candidates:
        classification = classify_candidate(candidate)
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
