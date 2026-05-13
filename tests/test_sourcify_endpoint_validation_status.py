import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STATUS = REPO_ROOT / "docs/16_launch/SOURCIFY_ENDPOINT_VALIDATION_STATUS.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_status_doc_exists_and_covers_evidence():
    assert STATUS.exists()
    text = STATUS.read_text(encoding="utf-8")
    low = text.lower()

    assert "sourcify endpoint validation status v11.5" in low
    assert "network_error" in low or "network error" in low
    assert "5" in text
    assert "reachable" in low and "true" in text
    assert "404" in text
    assert "tls_error" in low or "tls error" in low
    assert "usable_metadata_received" in low and "false" in low
    assert "verified_source_status" in low and "unknown" in low
    assert "abi_available" in low and "unknown" in low
    assert "full 5-target trial remains blocked" in text.lower()
    assert 'green light retry VPS Sourcify endpoint validation only' in text
    assert 'green light rerun Sourcify trial from VPS' in text


def test_runbook_full_trial_blocked_until_usable_metadata():
    rb = RUNBOOK.read_text(encoding="utf-8").lower()
    assert "full trial remains blocked" in rb
    assert "usable metadata" in rb


def test_approval_and_claims_v11_5_posture():
    ap = APPROVAL.read_text(encoding="utf-8")
    cl = CLAIMS.read_text(encoding="utf-8").lower()

    assert "endpoint_validation_status: unresolved" in ap
    assert "full_trial_blocked: true" in ap
    assert "sourcify endpoint validation status" in cl
    assert "unresolved / no usable metadata / full trial blocked" in cl


def test_consolidated_docs_forbid_unsafe_positive_phrases():
    # STATUS.md §7 names forbidden shorthand explicitly; scan posture-bearing files only.
    combined = (
        RUNBOOK.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
        + CLAIMS.read_text(encoding="utf-8")
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


def test_env_unchanged_during_status_consolidation_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = STATUS.read_bytes()
    _ = RUNBOOK.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
