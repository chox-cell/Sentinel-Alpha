"""
JSON-RPC chain read boundary (Ethereum-compatible).

Backend uses JSON-RPC—not the Viem JS library. A matching TypeScript/SDK path can
reuse the same semantics later. Responses must never include provider URLs or
raw env-derived secrets.
"""

from __future__ import annotations

import os
from typing import Any

import requests

from services.signals.validators import is_valid_evm_address, normalize_address

_CHAIN_READ_TIMEOUT_SEC = 8.0

# Only chains backed by BASE_RPC_URL in this codebase (extend when adding RPC URLs per chain).
_SUPPORTED_CHAINS = frozenset({"base"})


def _truthy_env(name: str, default: str = "false") -> bool:
    return (os.getenv(name, default) or default).strip().lower() in {"1", "true", "yes", "on"}


def get_chain_readiness(chain: str) -> dict[str, Any]:
    """
    Readiness for JSON-RPC reads on ``chain``.
    Status is one of: available | not_configured | unsupported_chain
    adapter_mode is configured when an RPC endpoint is wired for supported chains.
    """
    normalized = (chain or "base").strip().lower() or "base"
    if normalized not in _SUPPORTED_CHAINS:
        return {
            "status": "unsupported_chain",
            "adapter_mode": "fallback",
            "chain": normalized,
        }

    rpc_set = bool((os.getenv("BASE_RPC_URL") or "").strip())
    if not rpc_set:
        return {
            "status": "not_configured",
            "adapter_mode": "fallback",
            "chain": normalized,
        }

    # Payment/risk pipelines may expose BASE_RPC_URL without enabling bytecode reads yet.
    if not _truthy_env("SENTINEL_CHAIN_READ_ENABLED", "false"):
        return {
            "status": "reads_disabled",
            "adapter_mode": "fallback",
            "chain": normalized,
        }

    return {
        "status": "available",
        "adapter_mode": "configured",
        "chain": normalized,
    }


def _code_is_nonempty(code_hex: str | None) -> bool:
    if not code_hex or not isinstance(code_hex, str):
        return False
    stripped = code_hex.strip().lower()
    if stripped in {"0x", "0x0"}:
        return False
    if stripped.startswith("0x"):
        body = stripped[2:]
        return any(ch != "0" for ch in body)
    return True


def get_contract_code(address: str, chain: str) -> dict[str, Any]:
    """
    Fetch bytecode via eth_getCode. Returns status + optional code hex.
    Never includes the RPC URL or other secret material.
    """
    addr = normalize_address(address or "")
    readiness = get_chain_readiness(chain)

    if readiness["status"] == "not_configured":
        return {"status": "not_configured", "code": None}
    if readiness["status"] == "reads_disabled":
        return {"status": "reads_disabled", "code": None}
    if readiness["status"] == "unsupported_chain":
        return {"status": "unsupported_chain", "code": None}
    if not is_valid_evm_address(addr):
        return {"status": "invalid_address", "code": None}

    rpc_url = (os.getenv("BASE_RPC_URL") or "").strip()
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getCode",
        "params": [addr, "latest"],
    }

    try:
        resp = requests.post(
            rpc_url,
            json=payload,
            timeout=_CHAIN_READ_TIMEOUT_SEC,
            headers={"Content-Type": "application/json"},
        )
    except requests.RequestException:
        return {"status": "provider_error", "code": None}

    if resp.status_code != 200:
        return {"status": "provider_error", "code": None}

    try:
        body = resp.json()
    except ValueError:
        return {"status": "provider_error", "code": None}

    err = body.get("error") if isinstance(body, dict) else None
    if err:
        return {"status": "provider_error", "code": None}

    result = body.get("result") if isinstance(body, dict) else None
    if not isinstance(result, str):
        return {"status": "provider_error", "code": None}

    return {"status": "ok", "code": result}


def classify_account_type(address: str, chain: str) -> dict[str, Any]:
    """
    Infer account kind from bytecode length. Requires a successful eth_getCode.
    contract | eoa | unknown
    """
    fetch = get_contract_code(address, chain)
    status = fetch.get("status")
    if status != "ok":
        return {
            "account_type": "unknown",
            "code_fetch_status": status,
            "code": fetch.get("code"),
        }

    code = fetch.get("code")
    if _code_is_nonempty(code):
        account_type = "contract"
    else:
        account_type = "eoa"

    return {
        "account_type": account_type,
        "code_fetch_status": status,
        "code": code,
    }
