from services.signals.validators import is_valid_evm_address, normalize_address


MAX_REDUCED_CANDIDATES = 50


def reduce_quicknode_event(payload: dict) -> list[dict]:
    payload = payload or {}
    payload = _unwrap_payload(payload)
    block_number = _extract_block_number(payload)
    tx_hash = _extract_tx_hash(payload)
    logs = _extract_logs(payload)

    candidates: list[dict] = []
    seen: set[tuple] = set()

    # Include top-level contract/address candidate when present.
    top_address = normalize_address(
        payload.get("contract_address")
        or payload.get("address")
        or payload.get("contract")
    )
    if _is_useful_address(top_address):
        event_type = _infer_event_type(payload, None)
        key = (top_address, tx_hash, block_number, event_type)
        seen.add(key)
        candidates.append(
            _build_candidate(
                contract_address=top_address,
                event_type=event_type,
                transaction_hash=tx_hash,
                block_number=block_number,
                log_count=len(logs),
                context=_candidate_context(payload, event_type, tx_hash, block_number, len(logs)),
            )
        )

    for log in logs:
        address = normalize_address(
            log.get("address")
            or log.get("contract_address")
            or log.get("contract")
        )
        if not _is_useful_address(address):
            continue

        log_tx_hash = log.get("transactionHash") or log.get("transaction_hash") or tx_hash
        log_block = log.get("blockNumber") or log.get("block_number") or block_number
        event_type = _infer_event_type(payload, log)
        key = (address, log_tx_hash, log_block, event_type)
        if key in seen:
            continue
        seen.add(key)

        candidates.append(
            _build_candidate(
                contract_address=address,
                event_type=event_type,
                transaction_hash=log_tx_hash,
                block_number=log_block,
                log_count=len(logs),
                context=_candidate_context(payload, event_type, log_tx_hash, log_block, len(logs)),
            )
        )
        if len(candidates) >= MAX_REDUCED_CANDIDATES:
            break

    return candidates[:MAX_REDUCED_CANDIDATES]


def _build_candidate(
    *,
    contract_address: str,
    event_type: str,
    transaction_hash: str | None,
    block_number: str | int | None,
    log_count: int,
    context: dict,
) -> dict:
    return {
        "contract_address": contract_address,
        "chain": "base",
        "event_type": event_type,
        "transaction_hash": transaction_hash,
        "block_number": block_number,
        "log_count": log_count,
        "context": context,
    }


def _extract_logs(payload: dict) -> list[dict]:
    logs = []
    if isinstance(payload.get("logs"), list):
        logs.extend([x for x in payload["logs"] if isinstance(x, dict)])

    receipt = payload.get("receipt")
    if isinstance(receipt, dict) and isinstance(receipt.get("logs"), list):
        logs.extend([x for x in receipt["logs"] if isinstance(x, dict)])

    receipts = payload.get("receipts")
    if isinstance(receipts, list):
        for receipt_item in receipts:
            if isinstance(receipt_item, dict) and isinstance(receipt_item.get("logs"), list):
                logs.extend([x for x in receipt_item["logs"] if isinstance(x, dict)])
    return logs


def _extract_tx_hash(payload: dict) -> str | None:
    return (
        payload.get("transaction_hash")
        or payload.get("transactionHash")
        or payload.get("tx_hash")
        or payload.get("hash")
    )


def _extract_block_number(payload: dict) -> str | int | None:
    return payload.get("block_number") or payload.get("blockNumber")


def _is_useful_address(address: str) -> bool:
    return bool(address) and is_valid_evm_address(address)


def _infer_event_type(payload: dict, log: dict | None) -> str:
    text_parts = []
    for source in [payload, log or {}]:
        for key in ("event_type", "event", "name", "topic", "topics"):
            value = source.get(key)
            if isinstance(value, list):
                text_parts.extend(str(v).lower() for v in value)
            elif value is not None:
                text_parts.append(str(value).lower())

    full = " ".join(text_parts)
    if "liquidity" in full:
        return "first_liquidity"
    if "token" in full:
        return "new_token_candidate"
    return "contract_event"


def _candidate_context(
    payload: dict,
    event_type: str,
    tx_hash: str | None,
    block_number: str | int | None,
    log_count: int,
) -> dict:
    context = {
        "event_type": event_type,
        "transaction_hash": tx_hash,
        "block_number": block_number,
        "log_count": log_count,
        "source": "quicknode",
    }
    for key in [
        "owner_privileges",
        "liquidity_unlocked",
        "oracle_dislocation",
        "simulation_revert",
        "bad_cluster",
        "shadow_link",
        "bad_bot_activity",
    ]:
        if key in payload:
            context[key] = payload.get(key)
    return context


def _unwrap_payload(payload: dict) -> dict:
    current = payload
    for _ in range(3):
        if not isinstance(current, dict):
            return payload
        nested = current.get("data") or current.get("event")
        if isinstance(nested, dict):
            current = nested
            continue
        return current
    return current if isinstance(current, dict) else payload
