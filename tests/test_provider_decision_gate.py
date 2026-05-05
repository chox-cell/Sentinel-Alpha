import hashlib
from pathlib import Path


DOC = Path("docs/16_launch/SENTINEL_PROVIDER_DECISION_GATE.md")


def test_provider_decision_gate_doc_exists_and_required_phrases():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8").lower()
    required = [
        "explicit founder approval",
        "estimated monthly cost",
        "fallback behavior tested",
        "no secrets in repo",
        "provider can be disabled with one flag",
        "default: no paid providers",
        "pre-revenue target remains <= $10/mo",
        "abi/source provider",
        "simulation provider",
        "mempool/mev provider",
        "historical risk database",
    ]
    for phrase in required:
        assert phrase in text


def test_provider_decision_gate_avoids_live_overclaims():
    text = DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "providers are live by default",
        "live simulation enabled by default",
        "claims it detects honeypots",
        "claims it prevents mev",
        "guaranteed protection is live",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_env_unchanged_during_provider_gate_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
