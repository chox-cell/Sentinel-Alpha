from __future__ import annotations

import re


def _normalize_hex(bytecode: str | None) -> tuple[str | None, str]:
    if bytecode is None:
        return None, "missing"
    if not isinstance(bytecode, str):
        return None, "invalid"
    raw = bytecode.strip().lower()
    if not raw:
        return None, "missing"
    if raw.startswith("0x"):
        raw = raw[2:]
    if not raw:
        return "", "empty"
    if len(raw) % 2 != 0:
        return None, "invalid"
    if not re.fullmatch(r"[0-9a-f]+", raw):
        return None, "invalid"
    return raw, "ok"


def analyze_bytecode_signals(address=None, chain=None, bytecode=None, chain_read_result=None):
    chain_read_result = chain_read_result or {}
    status = str(chain_read_result.get("chain_read_status") or "unknown")
    account_type = str(chain_read_result.get("account_type") or "unknown")
    code_available_flag = bool(chain_read_result.get("contract_code_available"))
    notes: list[str] = []

    if bytecode is None and isinstance(chain_read_result.get("bytecode"), str):
        bytecode = chain_read_result.get("bytecode")

    out = {
        "bytecode_analysis_status": "unknown",
        "bytecode_available": False,
        "bytecode_size": 0,
        "selector_candidates": [],
        "delegatecall_present": False,
        "selfdestruct_present": False,
        "external_call_present": False,
        "proxy_pattern_possible": "unknown",
        "suspicious_selector_candidates": [],
        "bytecode_confidence": 0.2,
        "confidence_impact": "none",
        "fallback_mode": True,
        "notes": notes,
    }

    if account_type == "eoa":
        out["bytecode_analysis_status"] = "unavailable"
        out["bytecode_confidence"] = 0.1
        notes.append("EOA-like target: contract bytecode analysis is unavailable.")
        return {
            **out,
            "signal_flags": {
                "bytecode_analysis_unavailable": 1,
                "delegatecall_present": 0,
                "selfdestruct_present": 0,
                "external_call_present": 0,
                "proxy_pattern_possible": 0,
                "suspicious_selector_candidate_present": 0,
            },
        }

    norm, norm_state = _normalize_hex(bytecode)
    if norm_state == "invalid":
        out["bytecode_analysis_status"] = "invalid"
        out["confidence_impact"] = "review_due_to_invalid_bytecode_payload"
        notes.append("Invalid bytecode hex payload; local analysis skipped.")
        return {
            **out,
            "signal_flags": {
                "bytecode_analysis_unavailable": 1,
                "delegatecall_present": 0,
                "selfdestruct_present": 0,
                "external_call_present": 0,
                "proxy_pattern_possible": 0,
                "suspicious_selector_candidate_present": 0,
            },
        }

    if norm_state in {"missing", "empty"}:
        out["bytecode_analysis_status"] = "unavailable"
        out["confidence_impact"] = "review_due_to_missing_bytecode"
        if code_available_flag:
            notes.append("Bytecode marked available by chain-read, but bytecode bytes are missing.")
        else:
            notes.append("Bytecode is unavailable; local bytecode analyzer has no bytes to parse.")
        return {
            **out,
            "signal_flags": {
                "bytecode_analysis_unavailable": 1,
                "delegatecall_present": 0,
                "selfdestruct_present": 0,
                "external_call_present": 0,
                "proxy_pattern_possible": 0,
                "suspicious_selector_candidate_present": 0,
            },
        }

    # Analyzed path
    bytecode_hex = norm or ""
    out["bytecode_analysis_status"] = "analyzed"
    out["fallback_mode"] = status != "ok"
    out["bytecode_available"] = True
    out["bytecode_size"] = len(bytecode_hex) // 2
    out["bytecode_confidence"] = 0.7 if status == "ok" else 0.55

    # EVM opcodes in hex stream.
    out["delegatecall_present"] = "f4" in bytecode_hex
    out["selfdestruct_present"] = "ff" in bytecode_hex
    out["external_call_present"] = "f1" in bytecode_hex or "fa" in bytecode_hex
    out["proxy_pattern_possible"] = True if out["delegatecall_present"] else "unknown"

    # Selector candidates from PUSH4 opcode (0x63XXXXXXXX).
    selectors = re.findall(r"63([0-9a-f]{8})", bytecode_hex)
    out["selector_candidates"] = [f"0x{s}" for s in selectors[:24]]

    suspicious = []
    for sel in out["selector_candidates"]:
        if sel in {"0x3659cfe6", "0xf851a440", "0x79ba5097"}:  # proxy/admin-ish candidates
            suspicious.append(sel)
    out["suspicious_selector_candidates"] = suspicious
    if suspicious:
        notes.append("Suspicious selector candidates found; candidates only, no definitive malicious verdict.")
    if out["delegatecall_present"]:
        notes.append("DELEGATECALL opcode found; proxy pattern possible, not definitive.")
    if out["selfdestruct_present"]:
        notes.append("SELFDESTRUCT opcode found; presence-only signal, no definitive malicious verdict.")

    return {
        **out,
        "signal_flags": {
            "bytecode_analysis_unavailable": 0,
            "delegatecall_present": 1 if out["delegatecall_present"] else 0,
            "selfdestruct_present": 1 if out["selfdestruct_present"] else 0,
            "external_call_present": 1 if out["external_call_present"] else 0,
            "proxy_pattern_possible": 1 if out["proxy_pattern_possible"] is True else 0,
            "suspicious_selector_candidate_present": 1 if len(out["suspicious_selector_candidates"]) > 0 else 0,
        },
    }

