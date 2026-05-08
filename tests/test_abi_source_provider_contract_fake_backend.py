import hashlib
from pathlib import Path

from services.scanner_engine.abi_source_adapter import analyze_abi_source_status


PLAN_DOC = Path("docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md")
STRATEGY_DOC = Path("docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md")


def _run_fake_scenario(scenario: str) -> dict:
    return analyze_abi_source_status(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
        provider_context={
            "provider_name": "fake_backend",
            "fake_backend": True,
            "scenario": scenario,
        },
    )


def test_fake_backend_success_verified_source():
    out = _run_fake_scenario("success_verified_source")
    assert out["provider_name"] == "fake_backend"
    assert out["source_provider_status"] in {"available", "adapter_ready"}
    assert out["verified_source_status"] == "verified"
    assert out["abi_available"] is True
    assert len(out["abi_function_names"]) > 0
    assert out["fallback_mode"] is False


def test_fake_backend_success_abi_only():
    out = _run_fake_scenario("success_abi_only")
    assert out["abi_available"] is True
    assert out["verified_source_status"] in {"unknown", "unverified"}
    assert out["fallback_mode"] in {False, True}
    assert "verified-source coverage is complete" not in " ".join(out["notes"]).lower()


def test_fake_backend_timeout_rate_limited_invalid_provider_down_unsupported_chain():
    timeout = _run_fake_scenario("timeout")
    assert timeout["source_fetch_error_type"] == "timeout"
    assert timeout["fallback_mode"] is True
    assert timeout["abi_available"] in {"unknown", False}
    assert "low_confidence" in timeout["confidence_impact"]

    rate_limited = _run_fake_scenario("rate_limited")
    assert rate_limited["source_fetch_error_type"] == "rate_limited"
    assert rate_limited["fallback_mode"] is True
    assert "low_confidence" in rate_limited["confidence_impact"]

    invalid = _run_fake_scenario("invalid_response")
    assert invalid["source_fetch_error_type"] == "invalid_response"
    assert invalid["fallback_mode"] is True

    down = _run_fake_scenario("provider_down")
    assert down["source_fetch_error_type"] == "provider_down"
    assert down["fallback_mode"] is True

    unsupported = _run_fake_scenario("unsupported_chain")
    assert unsupported["source_fetch_error_type"] == "unsupported_chain"
    assert unsupported["fallback_mode"] is True


def test_no_requests_or_httpx_required_for_fake_backend_tests():
    out = _run_fake_scenario("success_verified_source")
    notes = " ".join(out["notes"]).lower()
    assert "no external provider call was performed" in notes
    assert "http" not in notes


def test_docs_mention_fake_backend_contract_tests_and_not_live():
    plan = PLAN_DOC.read_text(encoding="utf-8").lower()
    strategy = STRATEGY_DOC.read_text(encoding="utf-8").lower()
    assert "fake backend contract tests" in plan
    assert "does not enable live provider integration" in plan
    assert "no api keys required for fake backend contract tests" in plan
    assert "real provider activation must pass fake backend contract tests first" in strategy


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            PLAN_DOC.read_text(encoding="utf-8"),
            STRATEGY_DOC.read_text(encoding="utf-8"),
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


def test_env_unchanged_during_fake_backend_contract_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = _run_fake_scenario("success_verified_source")
    _ = PLAN_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
