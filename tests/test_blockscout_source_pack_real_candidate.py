import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/16_launch/BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md"
PLAN = REPO_ROOT / "docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"


def test_b01_real_urls_and_fields():
    text = PACK.read_text(encoding="utf-8")
    low = text.lower()

    assert "https://base.blockscout.com/api-docs" in text
    assert "Base Mainnet API docs | Blockscout" in text
    assert "https://base.blockscout.com" in text
    assert "/api/v2/smart-contracts/{address}" in text
    assert "b01" in low
    assert "replacement_required" in low and "false" in low
    assert "selected_for_validation" in low
    assert "validation_status" in low
    assert "not_run" in low


def test_b02_b03_placeholders():
    text = PACK.read_text(encoding="utf-8")
    assert "REQUIRED_SOURCE_URL" in text
    assert "replacement_required" in text.lower()
    assert "b02" in text.lower()
    assert "b03" in text.lower()


def test_selection_status_gate():
    text = PACK.read_text(encoding="utf-8").lower()
    assert "selected_candidate_id" in text
    assert "null" in text
    assert "endpoint_validation_blocked" in text
    assert "true" in text
    assert "no candidate selected for validation yet" in text


def test_validation_plan_b01_not_selected_gate():
    pl = PLAN.read_text(encoding="utf-8").lower()
    assert "b01" in pl
    assert "source-backed" in pl
    assert "not selected" in pl
    assert "green light vps blockscout endpoint validation only" in pl


def test_approval_v11_9_blockscout_b01():
    ap = APPROVAL.read_text(encoding="utf-8")
    assert "blockscout_source_candidate_b01:" in ap
    assert "source_backed / not_selected / not_validated" in ap
    assert "selected_blockscout_candidate: null" in ap


def test_claims_source_backed_candidate_row():
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "blockscout base source-backed endpoint candidate" in cl
    assert "source-backed candidate prepared / not selected / not validated" in cl


def test_posture_docs_forbid_unsafe_positive_phrases():
    combined = (
        RUNBOOK.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
        + CLAIMS.read_text(encoding="utf-8")
    ).lower()
    forbidden = [
        "blockscout endpoint works",
        "blockscout integration live",
        "trial completed",
        "live abi coverage",
        "full verified-source coverage",
        "guaranteed source verification",
        "detects honeypots",
        "guaranteed protection",
        "prevents mev",
        "live simulation",
        "production provider active",
    ]
    for phrase in forbidden:
        assert phrase not in combined, phrase


def test_env_unchanged_during_real_candidate_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PACK.read_bytes()
    _ = PLAN.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
