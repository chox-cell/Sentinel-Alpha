import hashlib
from pathlib import Path


PLAN_DOC = Path("docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md")
STRATEGY_DOC = Path("docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md")
GATE_DOC = Path("docs/16_launch/SENTINEL_PROVIDER_DECISION_GATE.md")
CLAIMS_LEDGER = Path("docs/18_investor/CLAIMS_LEDGER.md")


def test_activation_plan_doc_exists_and_required_sections():
    assert PLAN_DOC.exists()
    text = PLAN_DOC.read_text(encoding="utf-8")
    lower = text.lower()

    assert "ABI/Source Provider Activation Plan v1" in text
    assert "Not active now." in text
    assert "No API key required by default." in text
    assert "No external provider call is made by baseline runtime." in text
    for provider in ["Basescan", "Etherscan", "Blockscout", "Sourcify"]:
        assert provider in text
    assert "explicit founder approval" in lower
    assert "timeout tests" in lower
    assert "rate-limit tests" in lower
    assert "invalid response tests" in lower
    assert "provider-down fallback tests" in lower
    assert "one-flag disable" in lower
    assert "\"live ABI coverage\"".lower() in lower
    assert "\"guaranteed source verification\"".lower() in lower


def test_strategy_gate_and_claims_references_exist():
    strategy = STRATEGY_DOC.read_text(encoding="utf-8").lower()
    gate = GATE_DOC.read_text(encoding="utf-8").lower()
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()

    assert "abi_source_provider_activation_plan.md" in strategy
    assert "no paid providers by default" in strategy
    assert "abi/source provider activation plan" in gate
    assert "abi/source live provider integration is active now" in ledger
    assert "not live by default" in ledger


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            PLAN_DOC.read_text(encoding="utf-8"),
            STRATEGY_DOC.read_text(encoding="utf-8"),
            GATE_DOC.read_text(encoding="utf-8"),
            CLAIMS_LEDGER.read_text(encoding="utf-8"),
        ]
    ).lower()
    forbidden = [
        "live abi coverage is available",
        "full verified-source coverage is available",
        "guaranteed protection is provided",
        "claims it detects honeypots",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in combined


def test_env_unchanged_during_activation_plan_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PLAN_DOC.read_text(encoding="utf-8")
    _ = STRATEGY_DOC.read_text(encoding="utf-8")
    _ = GATE_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
