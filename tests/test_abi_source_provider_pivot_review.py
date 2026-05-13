import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PIVOT = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"
TRIAL_PLAN = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md"
STRATEGY = REPO_ROOT / "docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md"
CORRECTION = REPO_ROOT / "docs/16_launch/SOURCIFY_ENDPOINT_CORRECTION_PLAN.md"


def test_pivot_review_doc_exists_and_covers_evidence():
    assert PIVOT.exists()
    text = PIVOT.read_text(encoding="utf-8")
    low = text.lower()

    assert "abi/source provider pivot review v11.6" in low
    assert "network_error" in low or "network error" in low
    assert "v10.8a" in low
    assert "reachable" in low and "true" in text
    assert "404" in text
    assert "tls_error" in low or "tls error" in low
    assert "v11.4" in low
    assert "no usable metadata" in low
    assert "full trial remains blocked" in low or "full 5-target trial remains blocked" in low
    assert "provider remains disabled" in low
    assert "option a" in low
    assert "option b" in low
    assert "option c" in low
    assert 'green light retry VPS Sourcify endpoint validation only' in text
    assert 'green light VPS Blockscout endpoint validation only' in text
    assert "do not run" in low and "full sourcify" in low and "five-target" in low


def test_runbook_references_pivot_review():
    rb = RUNBOOK.read_text(encoding="utf-8")
    assert "ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md" in rb
    assert "pivot review" in rb.lower()


def test_approval_and_claims_pivot_posture():
    ap = APPROVAL.read_text(encoding="utf-8")
    cl = CLAIMS.read_text(encoding="utf-8").lower()

    assert "provider_pivot_status:" in ap
    assert "review_prepared" in ap
    assert "abi/source provider pivot review" in cl
    assert "review prepared / no new provider activation" in cl


def test_trial_plan_and_strategy_reference_pivot():
    tp = TRIAL_PLAN.read_text(encoding="utf-8")
    st = STRATEGY.read_text(encoding="utf-8")
    assert "ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md" in tp
    assert "ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md" in st


def test_posture_docs_forbid_unsafe_positive_phrases():
    # PIVOT and STATUS name forbidden shorthand in their claim-control sections.
    # SENTINEL_DATA_PROVIDER_STRATEGY.md contains negations like "no live simulation claim" — exclude from substring scan.
    combined = (
        RUNBOOK.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
        + CLAIMS.read_text(encoding="utf-8")
        + TRIAL_PLAN.read_text(encoding="utf-8")
        + CORRECTION.read_text(encoding="utf-8")
    ).lower()
    forbidden = [
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


def test_env_unchanged_during_pivot_review_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PIVOT.read_bytes()
    _ = RUNBOOK.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
