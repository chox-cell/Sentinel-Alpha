import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
TRIAL_PLAN = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md"
RESULT_SCHEMA = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md"
SAMPLE_MD = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.sample.md"
ACTIVATION = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_approval_record_exists_and_hold_posture():
    assert APPROVAL.exists()
    text = APPROVAL.read_text(encoding="utf-8")
    lower = text.lower()

    assert "ABI/Source Provider Trial Approval Record v1" in text
    assert "approval_status: not_approved" in text
    assert "trial_run: false" in text
    assert "provider_active: false" in text
    assert "live_calls_performed: false" in text
    assert "api_keys_required: false" in text
    assert "paid_calls_allowed: false" in text
    assert '"green light live provider trial"' in text
    assert "provider disabled by default" in lower
    assert "what remains blocked" in lower

    assert "## 9) Public claim controls" in text or "public claim controls" in lower


def test_linked_docs_reference_approval_record():
    needle = "ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
    assert needle in RUNBOOK.read_text(encoding="utf-8")
    assert needle in TRIAL_PLAN.read_text(encoding="utf-8")
    assert needle in RESULT_SCHEMA.read_text(encoding="utf-8")
    assert needle in SAMPLE_MD.read_text(encoding="utf-8")
    assert needle in ACTIVATION.read_text(encoding="utf-8")


def test_claims_ledger_approval_row():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "abi/source provider trial approval record" in ledger
    assert "not approved / trial not run" in ledger


def test_forbidden_positive_phrases_absent():
    lower = APPROVAL.read_text(encoding="utf-8").lower()
    forbidden = [
        "trial approved",
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


def test_env_unchanged_during_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    paths = (
        APPROVAL,
        RUNBOOK,
        TRIAL_PLAN,
        RESULT_SCHEMA,
        SAMPLE_MD,
        ACTIVATION,
        CLAIMS_LEDGER,
    )
    for path in paths:
        _ = path.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
