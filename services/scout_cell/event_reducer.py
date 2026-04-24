from services.signals.validators import is_valid_evm_address, normalize_address


MAX_REDUCED_CANDIDATES = 50
TRANSFER_TOPIC0_PREFIX = "0xddf252ad"


def reduce_quicknode_event(payload: dict) -> list[dict]:
    raw_payload = payload or {}
    payload = _unwrap_payload(raw_payload)
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
        _append_candidate(
            candidates,
            seen,
            _build_candidate(
                contract_address=top_address,
                event_type=event_type,
                transaction_hash=tx_hash,
                block_number=block_number,
                log_count=len(logs),
                context=_candidate_context(payload, event_type, tx_hash, block_number, len(logs)),
            ),
        )

    # Existing logs extraction path.
    for idx, log in enumerate(logs):
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
        _append_candidate(
            candidates,
            seen,
            _build_candidate(
                contract_address=address,
                event_type=event_type,
                transaction_hash=log_tx_hash,
                block_number=log_block,
                log_count=len(logs),
                context=_candidate_context(
                    payload,
                    event_type,
                    log_tx_hash,
                    log_block,
                    len(logs),
                    log=log,
                    log_index=idx,
                ),
            ),
        )

    # QuickNode matchingReceipts v0.2 path.
    matching_receipts = payload.get("matchingReceipts")
    if isinstance(matching_receipts, list):
        for receipt_index, receipt in enumerate(matching_receipts):
            if not isinstance(receipt, dict):
                continue

            receipt_logs = receipt.get("logs")
            receipt_tx_hash = receipt.get("transactionHash") or receipt.get("transaction_hash")
            receipt_block = receipt.get("blockNumber") or receipt.get("block_number")
            receipt_from = receipt.get("from")
            receipt_to = receipt.get("to")

            # Candidate from contractAddress when present.
            contract_address = normalize_address(receipt.get("contractAddress"))
            if _is_useful_address(contract_address):
                _append_candidate(
                    candidates,
                    seen,
                    _build_candidate(
                        contract_address=contract_address,
                        event_type="new_token_candidate",
                        transaction_hash=receipt_tx_hash,
                        block_number=receipt_block,
                        log_count=len(receipt_logs) if isinstance(receipt_logs, list) else 0,
                        context={
                            "event_type": "new_token_candidate",
                            "source": "quicknode",
                            "receipt_index": receipt_index,
                            "log_index": None,
                            "transaction_hash": receipt_tx_hash,
                            "block_number": receipt_block,
                            "topic0": None,
                            "receipt_from": receipt_from,
                            "receipt_to": receipt_to,
                        },
                    ),
                )

            if not isinstance(receipt_logs, list):
                continue

            for log_index, log in enumerate(receipt_logs):
                if not isinstance(log, dict):
                    continue

                address = normalize_address(log.get("address"))
                if not _is_useful_address(address):
                    continue

                log_tx_hash = log.get("transactionHash") or log.get("transaction_hash") or receipt_tx_hash
                log_block = log.get("blockNumber") or log.get("block_number") or receipt_block
                topic0 = _extract_topic0(log)
                event_type = _event_type_from_topic(topic0)

                _append_candidate(
                    candidates,
                    seen,
                    _build_candidate(
                        contract_address=address,
                        event_type=event_type,
                        transaction_hash=log_tx_hash,
                        block_number=log_block,
                        log_count=len(receipt_logs),
                        context={
                            "event_type": event_type,
                            "source": "quicknode",
                            "receipt_index": receipt_index,
                            "log_index": log_index,
                            "transaction_hash": log_tx_hash,
                            "block_number": log_block,
                            "topic0": topic0,
                            "receipt_from": receipt_from,
                            "receipt_to": receipt_to,
                        },
                    ),
                )

    sorted_candidates = sorted(candidates, key=_priority_sort_key)
    return sorted_candidates[:MAX_REDUCED_CANDIDATES]


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


def _append_candidate(candidates: list[dict], seen: set[tuple], candidate: dict) -> None:
    key = (
        candidate["contract_address"],
        candidate["transaction_hash"],
        candidate["block_number"],
        candidate["event_type"],
    )
    if key in seen:
        return
    seen.add(key)
    candidates.append(candidate)


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
    topic0 = _extract_topic0(log or {})
    if topic0:
        return _event_type_from_topic(topic0)

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
    log: dict | None = None,
    receipt_index: int | None = None,
    log_index: int | None = None,
) -> dict:
    topic0 = _extract_topic0(log or {})
    context = {
        "event_type": event_type,
        "transaction_hash": tx_hash,
        "block_number": block_number,
        "log_count": log_count,
        "source": "quicknode",
        "receipt_index": receipt_index,
        "log_index": log_index,
        "topic0": topic0,
        "receipt_from": None,
        "receipt_to": None,
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


def _extract_topic0(log: dict) -> str | None:
    topics = log.get("topics")
    if isinstance(topics, list) and topics:
        first = topics[0]
        if first is not None:
            return str(first).lower()
    topic = log.get("topic0")
    if topic is not None:
        return str(topic).lower()
    return None


def _event_type_from_topic(topic0: str | None) -> str:
    t = (topic0 or "").lower()
    if t.startswith(TRANSFER_TOPIC0_PREFIX):
        return "contract_event"
    if "token" in t:
        return "new_token_candidate"
    liquidity_keywords = ["mint", "increaseliquidity", "liquidity", "pool"]
    if any(keyword in t for keyword in liquidity_keywords):
        return "first_liquidity"
    return "contract_event"


def _priority_sort_key(candidate: dict) -> tuple:
    event_type = candidate.get("event_type")
    if event_type == "first_liquidity":
        priority = 0
    elif event_type == "new_token_candidate":
        priority = 1
    else:
        priority = 3
    # high log_count ranks before low log_count for same priority bucket.
    return (priority, -int(candidate.get("log_count", 0) or 0), candidate.get("contract_address", ""))
