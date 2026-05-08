import hashlib
from pathlib import Path

from services.scanner_engine.abi_source_adapter import analyze_abi_source_status
from services.scanner_engine.abi_source_provider_config import (
    get_abi_source_provider_config,
    get_abi_source_provider_runtime_status,
)


PLAN_DOC = Path("docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md")
STRATEGY_DOC = Path("docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md")
CLAIMS_LEDGER = Path("docs/18_investor/CLAIMS_LEDGER.md")


def test_config_module_exists_and_default_is_disabled():
    cfg = get_abi_source_provider_config()
    assert cfg["provider_enabled"] is False
    assert cfg["provider_mode"] == "disabled"
    assert cfg["network_calls_enabled"] is False
    assert cfg["api_key_required"] is False
    assert all(p in cfg["supported_providers"] for p in ["basescan", "etherscan", "blockscout", "sourcify"])


def test_enabled_without_provider_is_not_configured():
    cfg = get_abi_source_provider_config(
        env={"SENTINEL_ABI_SOURCE_PROVIDER_ENABLED": "true"},
    )
    assert cfg["provider_enabled"] is True
    assert cfg["provider_mode"] == "not_configured"


def test_unsupported_provider_returns_unsupported_provider():
    cfg = get_abi_source_provider_config(
        env={
            "SENTINEL_ABI_SOURCE_PROVIDER_ENABLED": "true",
            "SENTINEL_ABI_SOURCE_PROVIDER_NAME": "unknown-provider",
        },
    )
    assert cfg["provider_mode"] == "unsupported_provider"


def test_supported_provider_enabled_returns_adapter_ready_without_network():
    cfg = get_abi_source_provider_config(
        env={
            "SENTINEL_ABI_SOURCE_PROVIDER_ENABLED": "true",
            "SENTINEL_ABI_SOURCE_PROVIDER_NAME": "basescan",
        },
    )
    status = get_abi_source_provider_runtime_status(cfg)
    assert status["provider_mode"] == "adapter_ready"
    assert status["network_calls_enabled"] is False
    assert status["external_integration_status"] == "not_integrated"


def test_status_does_not_expose_api_keys():
    cfg = get_abi_source_provider_config(
        env={
            "SENTINEL_ABI_SOURCE_PROVIDER_ENABLED": "true",
            "SENTINEL_ABI_SOURCE_PROVIDER_NAME": "etherscan",
            "ETHERSCAN_API_KEY": "secret-do-not-leak",
        },
    )
    dumped = str(cfg).lower()
    assert "secret-do-not-leak" not in dumped
    assert "etherscan_api_key" not in dumped


def test_adapter_default_and_skeleton_statuses():
    disabled_out = analyze_abi_source_status(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
    )
    assert disabled_out["source_provider_status"] in {"disabled", "not_configured"}
    assert disabled_out["fallback_mode"] is True

    not_configured_out = analyze_abi_source_status(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
        config={"SENTINEL_ABI_SOURCE_PROVIDER_ENABLED": True},
    )
    assert not_configured_out["source_provider_status"] == "not_configured"
    assert not_configured_out["fallback_mode"] is True

    unsupported_out = analyze_abi_source_status(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
        config={
            "SENTINEL_ABI_SOURCE_PROVIDER_ENABLED": True,
            "SENTINEL_ABI_SOURCE_PROVIDER_NAME": "bad-provider",
        },
    )
    assert unsupported_out["source_provider_status"] == "unsupported_provider"
    assert unsupported_out["source_fetch_error_type"] == "unsupported_provider"
    assert unsupported_out["fallback_mode"] is True

    adapter_ready_out = analyze_abi_source_status(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
        config={
            "SENTINEL_ABI_SOURCE_PROVIDER_ENABLED": True,
            "SENTINEL_ABI_SOURCE_PROVIDER_NAME": "basescan",
        },
    )
    assert adapter_ready_out["source_provider_status"] == "adapter_ready"
    assert adapter_ready_out["source_fetch_error_type"] == "not_activated"
    assert adapter_ready_out["fallback_mode"] is True


def test_docs_and_claims_mention_wiring_skeleton_and_disabled_live_calls():
    plan = PLAN_DOC.read_text(encoding="utf-8").lower()
    strategy = STRATEGY_DOC.read_text(encoding="utf-8").lower()
    claims = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "disabled wiring skeleton" in plan
    assert "live provider calls remain disabled" in plan
    assert "wiring skeleton posture (v9.8)" in strategy
    assert "live provider calls remain disabled" in strategy
    assert "abi/source provider wiring skeleton exists" in claims
    assert "skeleton only" in claims


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            PLAN_DOC.read_text(encoding="utf-8"),
            STRATEGY_DOC.read_text(encoding="utf-8"),
            CLAIMS_LEDGER.read_text(encoding="utf-8"),
        ]
    ).lower()
    forbidden = [
        "live abi coverage is available",
        "full verified-source coverage is available",
        "guaranteed source verification is provided",
        "claims it detects honeypots",
        "guaranteed protection is provided",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in combined


def test_env_unchanged_during_wiring_skeleton_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = get_abi_source_provider_config()
    _ = analyze_abi_source_status(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
    )
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
