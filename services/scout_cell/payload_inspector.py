def inspect_quicknode_payload(payload: dict) -> dict:
    payload = payload or {}

    data = None
    if isinstance(payload, dict):
        data = payload.get("data")
        if data is None:
            data = payload.get("event")

    possible_list_paths = []
    sample_paths_only = []

    def walk(node, path):
        if len(sample_paths_only) >= 40:
            return
        if isinstance(node, list):
            possible_list_paths.append(path or "$")
            sample_paths_only.append(path or "$")
            if node:
                walk(node[0], f"{path}[0]" if path else "$[0]")
            return
        if isinstance(node, dict):
            for key, value in node.items():
                next_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    sample_paths_only.append(next_path)
                    walk(value, next_path)

    walk(payload, "")

    receipts = payload.get("receipts") if isinstance(payload, dict) else None
    receipt_obj = payload.get("receipt") if isinstance(payload, dict) else None
    logs_top = payload.get("logs") if isinstance(payload, dict) else None

    receipt_count_guess = 0
    if isinstance(receipts, list):
        receipt_count_guess = len(receipts)
    elif isinstance(receipt_obj, dict):
        receipt_count_guess = 1

    log_count_guess = 0
    if isinstance(logs_top, list):
        log_count_guess += len(logs_top)
    if isinstance(receipt_obj, dict) and isinstance(receipt_obj.get("logs"), list):
        log_count_guess += len(receipt_obj["logs"])
    if isinstance(receipts, list):
        for item in receipts:
            if isinstance(item, dict) and isinstance(item.get("logs"), list):
                log_count_guess += len(item["logs"])

    top_level_keys = list(payload.keys()) if isinstance(payload, dict) else []
    data_keys = list(data.keys()) if isinstance(data, dict) else []

    return {
        "top_level_type": type(payload).__name__,
        "top_level_keys": top_level_keys[:50],
        "data_type": type(data).__name__ if data is not None else "none",
        "data_keys": data_keys[:50],
        "possible_list_paths": sorted(set(possible_list_paths))[:50],
        "receipt_count_guess": receipt_count_guess,
        "log_count_guess": log_count_guess,
        "sample_paths_only": sample_paths_only[:50],
    }
