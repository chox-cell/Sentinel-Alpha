import hashlib
from pathlib import Path

from services.scanner_engine.simulation_provider_adapter import (
    build_simulation_request,
    get_simulation_provider_status,
    run_simulation_provider,
    sanitize_simulation_request,
)


DATA_STRATEGY = Path("docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md")
V5_ROADMAP = Path("docs/16_launch/SENTINEL_RISK_ENGINE_V5_ROADMAP.md")


def test_default_provider_disabled_and_no_keys_required():
    status = get_simulation_provider_status()
    assert status["provider_enabled"] is False
    assert status["provider_mode"] in {"disabled", "not_configured"}
    assert status["provider_required"] is False
    assert status["private_key_required"] is False
    notes = " ".join(status["notes"]).lower()
    assert "no provider key is required" in notes


def test_tenderly_access_key_not_required_and_no_execution_by_default():
    out = run_simulation_provider(build_simulation_request(address="0x1", chain="base", action="buy"))
    assert out["live_simulation_available"] is False
    assert out["simulation_status"] == "not_run"
    assert out["execution_attempted"] is False
    assert out["write_attempted"] is False
    assert out["honeypot_risk"] == "unknown"


def test_request_sanitizer_strips_sensitive_fields():
    req = {
        "chain": "base",
        "address": "0x111",
        "action": "call",
        "private_key": "x",
        "seed_phrase": "x",
        "authorization": "x",
        "api_key": "x",
        "headers": {"authorization": "x"},
        "cookies": "x",
        "payment_signature": "x",
        "wallet_private_key": "x",
    }
    clean = sanitize_simulation_request(req)
    dumped = str(clean).lower()
    for forbidden in [
        "private_key",
        "seed_phrase",
        "authorization",
        "api_key",
        "headers",
        "cookies",
        "payment_signature",
        "wallet_private_key",
    ]:
        assert forbidden not in dumped


def test_explicit_test_backend_returns_deterministic_result_only():
    backend = {
        "result": {
            "simulation_provider_status": "test_backend",
            "simulation_status": "simulated_test_only",
            "buy_simulation_status": "passed",
            "sell_simulation_status": "failed",
            "call_simulation_status": "passed",
            "provider_name": "test_backend",
            "error_type": None,
        }
    }
    out = run_simulation_provider(
        build_simulation_request(address="0x111", chain="base", action="buy"),
        provider_backend=backend,
    )
    assert out["simulation_status"] == "simulated_test_only"
    assert out["provider_name"] == "test_backend"
    assert out["live_simulation_available"] is False
    assert out["honeypot_risk"] == "unknown"


def test_docs_reflect_disabled_non_live_posture():
    ds = DATA_STRATEGY.read_text(encoding="utf-8").lower()
    rm = V5_ROADMAP.read_text(encoding="utf-8").lower()
    assert "no paid simulation provider" in ds
    assert "no claim of live paid provider integration unless enabled" in ds
    assert "simulation adapter boundary" in rm
    assert "no paid provider until demand" in rm


def test_env_unchanged_during_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = get_simulation_provider_status()
    _ = build_simulation_request(address="0x222", chain="base", action="sell")
    _ = run_simulation_provider({})
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
