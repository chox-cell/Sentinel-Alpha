import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN = REPO_ROOT / "docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md"
PIVOT = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"
TRIAL_PLAN = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md"


def test_blockscout_plan_doc_exists_and_has_required_content():
    assert PLAN.exists()
    text = PLAN.read_text(encoding="utf-8")
    low = text.lower()

    assert "blockscout endpoint validation plan v11.7" in low
    assert "sourcify" in low and "unresolved" in low
    assert "provider remains disabled" in low
    assert "full trial remains blocked" in low or "full five-target" in low
    assert "one target" in low
    assert "one endpoint" in low
    assert "no dataset-wide lookup" in low or "dataset-wide" in low
    assert "no api key" in low or "no api keys" in low
    assert "{blockscout_base_url}/api/v2/smart-contracts/{address}" in text
    assert "BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md" in text
    assert "blockscout endpoint validation" in low and "blocked" in low
    assert "b01" in low and "source-backed" in low
    assert "not selected" in low
    assert 'green light VPS Blockscout endpoint validation only' in text
    assert 'green light rerun Blockscout trial from VPS' in text
    assert "raw_response_stored: false" in text
    assert "secret_material_observed: false" in text
    assert "notsecurityguarantee: true" in low


def test_pivot_references_blockscout_plan():
    pv = PIVOT.read_text(encoding="utf-8")
    assert "BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md" in pv


def test_runbook_blockscout_validation_gate():
    rb = RUNBOOK.read_text(encoding="utf-8")
    assert "BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md" in rb
    assert "blockscout" in rb.lower()


def test_approval_and_claims_blockscout_plan_posture():
    ap = APPROVAL.read_text(encoding="utf-8")
    cl = CLAIMS.read_text(encoding="utf-8").lower()

    assert "blockscout_validation_plan_status:" in ap
    assert "prepared / not run" in ap
    assert "blockscout endpoint validation plan" in cl
    assert "plan prepared / not run / no provider activation" in cl


def test_trial_plan_references_blockscout_plan():
    assert "BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md" in TRIAL_PLAN.read_text(encoding="utf-8")


def test_posture_docs_forbid_unsafe_positive_phrases():
    # BLOCKSCOUT plan and PIVOT list forbidden shorthand explicitly in claim-control sections.
    combined = (
        RUNBOOK.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
        + CLAIMS.read_text(encoding="utf-8")
        + TRIAL_PLAN.read_text(encoding="utf-8")
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


def test_env_unchanged_during_blockscout_plan_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PLAN.read_bytes()
    _ = PIVOT.read_text(encoding="utf-8")
    _ = RUNBOOK.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
