import hashlib
from pathlib import Path

from services.scanner_engine.router_pool_heuristics import analyze_router_pool_risk


def test_router_abi_hints_produce_router_candidate():
    result = analyze_router_pool_risk(
        address="0x6666666666666666666666666666666666666666",
        chain="base",
        asset_result={"asset_type": "router_candidate", "fallback_mode": False},
        abi_result={
            "available": True,
            "is_router": True,
            "functions": ["swapExactTokensForTokens", "addLiquidity", "getAmountsOut"],
        },
        bytecode_result={"fallback_mode": False},
        source_proxy_admin_result={"abi_available": True},
    )
    assert result["router_pool_analysis_status"] == "analyzed"
    assert result["router_candidate"] is True


def test_pool_abi_hints_produce_pool_candidate():
    result = analyze_router_pool_risk(
        address="0x7777777777777777777777777777777777777777",
        chain="base",
        asset_result={"asset_type": "pool_candidate", "fallback_mode": False},
        abi_result={
            "available": True,
            "is_pool": True,
            "functions": ["getReserves", "token0", "token1", "sync", "swap"],
        },
        bytecode_result={"fallback_mode": False},
        source_proxy_admin_result={"abi_available": True},
    )
    assert result["router_pool_analysis_status"] == "analyzed"
    assert result["pool_candidate"] is True
    assert result["reserve_function_possible"] is True


def test_eoa_returns_not_applicable():
    result = analyze_router_pool_risk(
        address="0x0000000000000000000000000000000000000000",
        chain="base",
        asset_result={"asset_type": "eoa", "fallback_mode": False},
        abi_result={},
        bytecode_result={},
        source_proxy_admin_result={},
    )
    assert result["router_pool_analysis_status"] == "not_applicable"
    assert result["router_candidate"] is False
    assert result["pool_candidate"] is False


def test_missing_abi_or_source_returns_unknown_fallback():
    result = analyze_router_pool_risk(
        address="0x1234567890abcdef1234567890abcdef12345678",
        chain="base",
        asset_result={"asset_type": "generic_contract", "fallback_mode": True},
        abi_result={},
        bytecode_result={},
        source_proxy_admin_result={"abi_available": "unknown"},
    )
    assert result["router_pool_analysis_status"] == "unknown"
    assert result["router_candidate"] == "unknown"
    assert result["pool_candidate"] == "unknown"
    assert result["fallback_mode"] is True


def test_no_overclaim_language():
    result = analyze_router_pool_risk(
        address="0x9999999999999999999999999999999999999999",
        chain="base",
        asset_result={"asset_type": "generic_contract", "fallback_mode": False},
        abi_result={"available": True, "functions": ["swap"]},
        bytecode_result={},
        source_proxy_admin_result={"abi_available": True},
    )
    text = str(result).lower()
    assert "malicious certainty" not in text
    assert "proves honeypot detection" not in text
    assert "complete dex support" in text


def test_env_unchanged():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = analyze_router_pool_risk(
        address="0x6666666666666666666666666666666666666666",
        chain="base",
        asset_result={"asset_type": "router_candidate", "fallback_mode": False},
        abi_result={"available": True, "functions": ["swapExactTokensForTokens"]},
        bytecode_result={},
        source_proxy_admin_result={"abi_available": True},
    )
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
