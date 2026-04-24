from shared.utils.logger import log_event
from services.risk_service.service import evaluate_contract
from services.scout_cell.quicknode_normalizer import normalize_quicknode_payload

def handle_new_contract(event: dict):
    normalized = normalize_quicknode_payload(event)
    contract = normalized["contract_address"]
    chain = normalized["chain"]

    log_event("quicknode_incoming", event)

    if not contract:
        result = {"status": "ignored", "reason": "missing contract_address"}
        log_event("quicknode_ignored", result)
        return result

    try:
        context = normalized["context"]

        body = evaluate_contract(contract, chain, context)

        result = {
            "status_code": 200,
            "body": body,
        }

        log_event("quicknode_analyzed", result)
        return result

    except Exception as e:
        result = {"status": "error", "message": str(e)}
        log_event("quicknode_error", result)
        return result
