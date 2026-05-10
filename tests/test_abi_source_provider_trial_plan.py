import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TRIAL_PLAN_DOC = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_trial_plan_doc_exists_and_core_gates():
    assert TRIAL_PLAN_DOC.exists()
    text = TRIAL_PLAN_DOC.read_text(encoding="utf-8")

    assert "Controlled Free ABI/Source Provider Trial Plan v1" in text
    assert "not active now" in text.lower()
    assert "provider wiring skeleton exists" in text.lower()
    assert "no provider enabled by default" in text.lower()
    assert "no api keys required now" in text.lower()

    assert "**Sourcify**" in text or "1. **Sourcify**" in text
    assert "Blockscout" in text
    assert "Basescan" in text
    assert "Etherscan" in text

    assert "5 known" in text.lower()
    assert "base" in text.lower()
    assert "read-only lookup only" in text.lower()
    assert "no paid calls" in text.lower()
    assert "fallback to `unknown`" in text or "fallback to unknown" in text.lower()

    assert "explicit founder approval" in text.lower()
    assert "rollback owner" in text.lower()

    assert "no full abi coverage" in text.lower()
    assert "does not promise verified source" in text.lower()


def test_claims_ledger_trial_status_row():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "controlled abi/source provider trial" in ledger
    assert "planned only / not active" in ledger
    assert "not enabled by default" in ledger


def test_trial_plan_forbidden_phrases_absent():
    text = TRIAL_PLAN_DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "live abi coverage",
        "full verified-source coverage",
        "guaranteed source verification",
        "detects honeypots",
        "guaranteed protection",
        "prevents mev",
        "live simulation",
    ]
    for token in forbidden:
        assert token not in text, f"unexpected phrase: {token}"


def test_env_unchanged_during_trial_plan_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = TRIAL_PLAN_DOC.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
