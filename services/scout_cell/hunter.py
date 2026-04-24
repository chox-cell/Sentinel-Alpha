from shared.utils.logger import log_event
from services.risk_service.service import evaluate_contract
from services.scout_cell.event_reducer import reduce_quicknode_event

def handle_new_contract(event: dict):
    candidates = reduce_quicknode_event(event)
    results = []

    for candidate in candidates:
        try:
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
                    "body": body,
                }
            )
        except Exception as e:
            results.append(
                {
                    "contract_address": candidate["contract_address"],
                    "chain": candidate["chain"],
                    "event_type": candidate["event_type"],
                    "transaction_hash": candidate["transaction_hash"],
                    "block_number": candidate["block_number"],
                    "status": "error",
                    "message": str(e),
                }
            )

    summary = {
        "status": "ok",
        "candidates": len(candidates),
        "results": results,
    }
    log_event(
        "quicknode_reduced",
        {
            "candidate_count": len(candidates),
            "block_number": (candidates[0]["block_number"] if candidates else None),
        },
    )
    return summary
