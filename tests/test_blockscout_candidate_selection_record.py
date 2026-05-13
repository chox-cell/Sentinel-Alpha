import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/16_launch/BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md"
PLAN = REPO_ROOT / "docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"


def test_source_pack_selection_and_block_reason():
    text = PACK.read_text(encoding="utf-8")
    low = text.lower()

    assert "selected_candidate_id: b01" in low
    assert "endpoint_validation_blocked: true" in low
    assert "validation phrase not yet given" in low
    assert "selected for future validation only" in low
    assert "no network validation has run" in low


def test_b01_selected_for_validation_true():
    t = PACK.read_text(encoding="utf-8")
    assert "| `selected_for_validation` | true |" in t
    assert "| `validation_status` | not_run |" in t
    assert "selected_reason" in t.lower()
    assert "source-backed base blockscout api docs candidate" in t.lower()


def test_b02_b03_not_selected():
    t = PACK.read_text(encoding="utf-8").lower()
    assert "| `candidate_id` | b02 |" in t
    assert "| `selected_for_validation` | false |" in t
    assert "b03" in t


def test_validation_plan_b01_selected_and_phrases():
    pl = PLAN.read_text(encoding="utf-8")
    low = pl.lower()
    assert "b01" in low
    assert "selected" in low
    assert 'green light VPS Blockscout endpoint validation only' in pl
    assert 'green light rerun Blockscout trial from VPS' in pl


def test_approval_v12_selection():
    ap = APPROVAL.read_text(encoding="utf-8")
    assert "blockscout_selected_candidate: B01" in ap
    assert "validation_not_run" in ap
    assert "provider_remains_disabled: true" in ap


def test_claims_selection_row():
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "blockscout candidate selection record" in cl
    assert "b01 selected / validation not run / no provider activation" in cl


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


def test_env_unchanged_during_selection_record_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PACK.read_bytes()
    _ = PLAN.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
