import json
import os

import requests

BASE_USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDC_DECIMALS = 6

ERC20_TRANSFER_TOPIC0 = (
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
)

_RPC_TIMEOUT_SEC = 8


def _is_true_env(name: str, default: str = "false") -> bool:
    return (os.getenv(name, default) or default).strip().lower() in {"1", "true", "yes", "on"}


def usdc_to_units(amount: float) -> int:
    return int(round(float(amount) * (10 ** USDC_DECIMALS)))


def _is_valid_tx_hash(tx_hash: str) -> bool:
    value = (tx_hash or "").strip()
    if not value.startswith("0x") or len(value) != 66:
        return False
    return all(ch in "0123456789abcdefABCDEF" for ch in value[2:])


def _is_valid_wallet(wallet: str) -> bool:
    value = (wallet or "").strip()
    if not value.startswith("0x") or len(value) != 42:
        return False
    return all(ch in "0123456789abcdefABCDEF" for ch in value[2:])


def _normalize_wallet_42(wallet: str) -> str:
    w = (wallet or "").strip().lower()
    if not w.startswith("0x"):
        w = "0x" + w
    if len(w) != 42:
        return ""
    return w


def _topic32_to_address(topic: str | None) -> str:
    if not topic or not isinstance(topic, str):
        return ""
    t = topic.strip().lower()
    if t.startswith("0x"):
        t = t[2:]
    if len(t) < 40:
        return ""
    addr_hex = t[-40:]
    if not all(c in "0123456789abcdef" for c in addr_hex):
        return ""
    return "0x" + addr_hex


def _parse_log_amount_hex(data: str | None) -> int | None:
    if not data or not isinstance(data, str):
        return None
    d = data.strip().lower()
    if not d.startswith("0x"):
        d = "0x" + d
    try:
        return int(d, 16)
    except ValueError:
        return None


def _receipt_status_ok(status) -> bool:
    if status is None:
        return False
    if isinstance(status, int):
        return status == 1
    s = str(status).strip().lower()
    return s in {"0x1", "0x01", "1"}


def _fetch_receipt(rpc_url: str, tx_hash: str) -> tuple[dict | None, str | None]:
    """Returns (receipt_dict, error_status). error_status set on RPC/parse failure."""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionReceipt",
        "params": [tx_hash],
        "id": 1,
    }
    try:
        resp = requests.post(
            rpc_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=_RPC_TIMEOUT_SEC,
        )
    except (requests.RequestException, OSError):
        return None, "rpc_error"

    if resp.status_code != 200:
        return None, "rpc_error"

    try:
        body = resp.json()
    except json.JSONDecodeError:
        return None, "rpc_error"

    if body.get("error"):
        return None, "rpc_error"

    return body.get("result"), None


def get_onchain_verification_status() -> dict:
    enabled = _is_true_env("X402_ONCHAIN_VERIFY")
    mock_enabled = _is_true_env("X402_MOCK_ONCHAIN_VERIFY")
    rpc_url = (os.getenv("BASE_RPC_URL") or "").strip()
    network = (os.getenv("X402_NETWORK", "base") or "base").strip().lower() or "base"
    return {
        "onchain_verify_enabled": enabled,
        "mock_onchain_verify_enabled": mock_enabled,
        "rpc_configured": bool(rpc_url),
        "network": network,
        "base_usdc_address": BASE_USDC_ADDRESS,
        "usdc_decimals": USDC_DECIMALS,
    }


def verify_usdc_transfer_tx(tx_hash: str, expected_amount: float, treasury_wallet: str) -> dict:
    enabled = _is_true_env("X402_ONCHAIN_VERIFY")
    if not enabled:
        return {"verified": False, "status": "onchain_verification_disabled"}

    if not _is_valid_tx_hash(tx_hash):
        return {"verified": False, "status": "invalid_tx_hash"}
    if not _is_valid_wallet(treasury_wallet):
        return {"verified": False, "status": "invalid_treasury_wallet"}
    if float(expected_amount) <= 0:
        return {"verified": False, "status": "invalid_expected_amount"}

    expected_units = usdc_to_units(float(expected_amount))
    if _is_true_env("X402_MOCK_ONCHAIN_VERIFY"):
        return {
            "verified": True,
            "status": "verified",
            "tx_hash": tx_hash,
            "mock": True,
            "amount_units": expected_units,
            "expected_units": expected_units,
            "treasury_wallet": treasury_wallet,
        }

    rpc_url = (os.getenv("BASE_RPC_URL") or "").strip()
    if not rpc_url:
        return {"verified": False, "status": "rpc_not_configured"}

    treasury_norm = _normalize_wallet_42(treasury_wallet)
    if not treasury_norm:
        return {"verified": False, "status": "invalid_treasury_wallet"}

    receipt, err = _fetch_receipt(rpc_url, tx_hash)
    if err:
        return {"verified": False, "status": err}
    if receipt is None:
        return {"verified": False, "status": "receipt_not_found"}

    if not _receipt_status_ok(receipt.get("status")):
        return {"verified": False, "status": "tx_failed"}

    usdc_addr = BASE_USDC_ADDRESS.lower()
    topic0_want = ERC20_TRANSFER_TOPIC0.lower()

    matching_to_treasury: list[int] = []

    for log in receipt.get("logs") or []:
        if not isinstance(log, dict):
            continue
        addr = (log.get("address") or "").strip().lower()
        if addr != usdc_addr:
            continue
        topics = log.get("topics") or []
        if len(topics) < 3:
            continue
        t0 = str(topics[0]).strip().lower()
        if t0 != topic0_want:
            continue
        to_addr = _topic32_to_address(str(topics[2]))
        if to_addr != treasury_norm:
            continue
        amt = _parse_log_amount_hex(log.get("data"))
        if amt is None:
            continue
        matching_to_treasury.append(amt)

    if not matching_to_treasury:
        return {"verified": False, "status": "no_matching_usdc_transfer"}

    best = max(matching_to_treasury)
    if best < expected_units:
        return {"verified": False, "status": "amount_too_low"}

    return {
        "verified": True,
        "status": "verified",
        "tx_hash": tx_hash,
        "amount_units": best,
        "expected_units": expected_units,
        "treasury_wallet": treasury_norm,
    }
