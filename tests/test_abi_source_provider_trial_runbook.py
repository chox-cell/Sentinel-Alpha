import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
TRIAL_PLAN = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md"
TRIAL_DATASET = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md"
RESULT_SCHEMA = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md"
ACTIVATION = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md"
GATE = REPO_ROOT / "docs/16_launch/SENTINEL_PROVIDER_DECISION_GATE.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_runbook_exists_and_gate_content():
    assert RUNBOOK.exists()
    text = RUNBOOK.read_text(encoding="utf-8")
    lower = text.lower()

    assert "ABI/Source Provider Trial Runbook v1" in text
    assert "trial not run" in lower
    assert "provider not active" in lower
    assert "no live calls have been performed" in lower or "no live calls" in lower
    assert "## 4) Founder approval gate" in text or "founder approval gate" in lower
    assert "<= 5" in text
    assert "env_hash_before" in text and "env_hash_after" in text
    assert "before run" in lower and "after run" in lower
    assert "sentinel_abi_source_provider_enabled=false" in lower
    assert "provider disabled after run" in lower or "disable provider immediately" in lower
    assert "## 8) Abort conditions" in text or "abort conditions" in lower
    assert "## 9) rollback" in lower
    assert "sentinel_abi_source_dry_run_only=false" in lower
    assert "paid_calls_allowed" in lower and "false" in lower
    assert "## 11) Public claim controls" in text or "public claim controls" in lower


def test_linked_docs_reference_runbook():
    needle = "ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
    for path in (TRIAL_PLAN, TRIAL_DATASET, RESULT_SCHEMA, ACTIVATION, GATE):
        assert needle in path.read_text(encoding="utf-8"), path.name


def test_claims_ledger_runbook_row():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "abi/source provider trial runbook" in ledger
    assert "runbook prepared / trial not run" in ledger


def test_runbook_forbidden_positive_phrases_absent():
    lower = RUNBOOK.read_text(encoding="utf-8").lower()
    forbidden = [
        "trial completed",
        "live abi coverage",
        "full verified-source coverage",
        "guaranteed source verification",
        "detects honeypots",
        "guaranteed protection",
        "prevents mev",
        "live simulation",
    ]
    for token in forbidden:
        assert token not in lower, token


def test_env_unchanged_during_runbook_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = RUNBOOK.read_text(encoding="utf-8")
    for path in (TRIAL_PLAN, TRIAL_DATASET, RESULT_SCHEMA, ACTIVATION, GATE, CLAIMS_LEDGER):
        _ = path.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
