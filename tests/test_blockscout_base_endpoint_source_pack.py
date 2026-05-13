import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/16_launch/BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md"
PLAN = REPO_ROOT / "docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md"
PIVOT = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_source_pack_doc_exists_and_has_required_content():
    assert PACK.exists()
    text = PACK.read_text(encoding="utf-8")
    low = text.lower()

    assert "blockscout base endpoint source pack v12.0" in low
    assert "no blockscout endpoint validation has run" in low
    assert "no blockscout base url" in low and "selected for runtime" in low
    assert "provider remains disabled" in low
    assert "blockscout_base_url" in low
    assert "source_url" in low
    assert "source_label" in low
    assert "observed_endpoint_or_docs_path" in low
    assert "8453" in text
    assert "selected_for_validation" in low
    assert "false" in low
    assert "validation_status" in low
    assert "not_run" in low
    assert "b01" in low
    assert "b02" in low
    assert "b03" in low
    assert "REQUIRED_SOURCE_URL" in text
    assert 'green light VPS Blockscout endpoint validation only' in text
    assert 'green light rerun Blockscout trial from VPS' in text


def test_validation_plan_references_source_pack_and_gate():
    pl = PLAN.read_text(encoding="utf-8").lower()
    assert "blockscout_base_endpoint_source_pack.md" in pl
    assert "blockscout endpoint validation" in pl and "blocked" in pl
    assert "b01" in pl and "selected" in pl


def test_pivot_references_source_pack():
    assert "BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md" in PIVOT.read_text(encoding="utf-8")


def test_runbook_requires_source_pack_before_blockscout_validation():
    rb = RUNBOOK.read_text(encoding="utf-8")
    assert "BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md" in rb


def test_approval_and_claims_source_pack_posture():
    ap = APPROVAL.read_text(encoding="utf-8")
    cl = CLAIMS.read_text(encoding="utf-8").lower()

    assert "blockscout_source_pack_status:" in ap
    assert "prepared / endpoint not selected" in ap
    assert "blockscout base endpoint source pack" in cl
    assert "source pack prepared / b01 selected for future validation / not run" in cl


def test_posture_docs_forbid_unsafe_positive_phrases():
    # Source pack, validation plan, and pivot list forbidden shorthand in claim-control sections.
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


def test_env_unchanged_during_source_pack_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PACK.read_bytes()
    _ = PLAN.read_text(encoding="utf-8")
    _ = PIVOT.read_text(encoding="utf-8")
    _ = RUNBOOK.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
