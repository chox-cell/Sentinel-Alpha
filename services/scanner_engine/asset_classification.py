from __future__ import annotations

from services.signals.validators import is_valid_evm_address, normalize_address

_ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

_CANDIDATE_TYPES = {
    "eoa",
    "generic_contract",
    "erc20_candidate",
    "erc721_candidate",
    "erc1155_candidate",
    "proxy_candidate",
    "router_candidate",
    "pool_candidate",
    "vault_candidate",
    "unknown",
}


def _as_bool(value: object) -> bool:
    return value is True or value == 1


def classify_asset_type(
    address: str,
    chain: str,
    chain_read_result: dict | None = None,
    abi_result: dict | None = None,
) -> dict:
    """
    Conservative v5.1 asset classification boundary.
    Uses available chain-read and optional ABI hints only; no deep claims.
    """
    normalized = normalize_address(address or "")
    chain_norm = (chain or "base").strip().lower() or "base"
    chain_read_result = chain_read_result or {}
    abi_result = abi_result or {}

    basis: list[str] = []
    notes: list[str] = []
    unsupported = False

    if normalized == _ZERO_ADDRESS:
        return {
            "asset_type": "unknown",
            "asset_confidence": 0.99,
            "classification_basis": ["zero_address"],
            "fallback_mode": False,
            "unsupported_asset_type": False,
            "signals": {"zero_address": True, "chain": chain_norm},
            "notes": ["zero address is treated as invalid/high-risk input"],
        }

    if not is_valid_evm_address(normalized):
        return {
            "asset_type": "unknown",
            "asset_confidence": 0.95,
            "classification_basis": ["invalid_address"],
            "fallback_mode": True,
            "unsupported_asset_type": True,
            "signals": {"invalid_address": True, "chain": chain_norm},
            "notes": ["address is not a valid EVM address"],
        }

    read_status = str(chain_read_result.get("chain_read_status") or "unknown")
    account_type = str(chain_read_result.get("account_type") or "unknown")
    code_available = bool(chain_read_result.get("contract_code_available"))
    fallback_mode = read_status != "ok"

    if read_status in {"not_configured", "unsupported_chain", "provider_error", "reads_disabled", "unavailable"}:
        basis.append(f"chain_read:{read_status}")
        notes.append("provider data unavailable or disabled; using conservative unknown classification")
        return {
            "asset_type": "unknown",
            "asset_confidence": 0.2,
            "classification_basis": basis,
            "fallback_mode": True,
            "unsupported_asset_type": False,
            "signals": {
                "chain_read_status": read_status,
                "account_type": account_type,
                "contract_code_available": code_available,
            },
            "notes": notes,
        }

    if read_status == "ok" and account_type == "eoa":
        return {
            "asset_type": "eoa",
            "asset_confidence": 0.95,
            "classification_basis": ["chain_read:ok", "account_type:eoa"],
            "fallback_mode": False,
            "unsupported_asset_type": False,
            "signals": {"account_type": "eoa", "contract_code_available": False},
            "notes": ["EOA classification from bytecode absence"],
        }

    # Contract path: default conservative to generic_contract unless strong hints exist.
    asset_type = "generic_contract"
    confidence = 0.55 if code_available else 0.35
    basis.extend(["chain_read:ok", "account_type:contract" if account_type == "contract" else "account_type:unknown"])

    kind = str(abi_result.get("kind") or "").strip().lower()
    if kind in _CANDIDATE_TYPES and kind.endswith("_candidate"):
        asset_type = kind
        confidence = 0.7
        basis.append("abi_hint:kind")
    else:
        if _as_bool(abi_result.get("is_proxy")):
            asset_type = "proxy_candidate"
            confidence = 0.68
            basis.append("abi_hint:is_proxy")
        elif _as_bool(abi_result.get("is_router")):
            asset_type = "router_candidate"
            confidence = 0.66
            basis.append("abi_hint:is_router")
        elif _as_bool(abi_result.get("is_pool")):
            asset_type = "pool_candidate"
            confidence = 0.66
            basis.append("abi_hint:is_pool")
        elif _as_bool(abi_result.get("is_vault")):
            asset_type = "vault_candidate"
            confidence = 0.66
            basis.append("abi_hint:is_vault")
        elif _as_bool(abi_result.get("supports_erc1155")):
            asset_type = "erc1155_candidate"
            confidence = 0.7
            basis.append("abi_hint:erc1155")
        elif _as_bool(abi_result.get("supports_erc721")):
            asset_type = "erc721_candidate"
            confidence = 0.7
            basis.append("abi_hint:erc721")
        elif _as_bool(abi_result.get("supports_erc20")):
            asset_type = "erc20_candidate"
            confidence = 0.7
            basis.append("abi_hint:erc20")
        else:
            notes.append("no ABI/source hints available; classified conservatively as generic_contract")

    if asset_type not in _CANDIDATE_TYPES:
        asset_type = "unknown"
        unsupported = True
        confidence = 0.2
        basis.append("unsupported_type")

    return {
        "asset_type": asset_type,
        "asset_confidence": round(confidence, 2),
        "classification_basis": basis,
        "fallback_mode": fallback_mode,
        "unsupported_asset_type": unsupported,
        "signals": {
            "chain_read_status": read_status,
            "account_type": account_type,
            "contract_code_available": code_available,
        },
        "notes": notes,
    }

