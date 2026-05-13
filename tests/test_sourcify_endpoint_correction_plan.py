import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN = REPO_ROOT / "docs/16_launch/SOURCIFY_ENDPOINT_CORRECTION_PLAN.md"
PREFLIGHT = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_VPS_CONNECTIVITY_PREFLIGHT.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
DATASET = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md"
SCHEMA = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_endpoint_correction_plan_exists_and_records_evidence():
    assert PLAN.exists()
    text = PLAN.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Sourcify Endpoint Correction Plan v1" in text
    assert "v10.8a" in lower
    assert "network_error" in lower
    assert "v11.2" in lower
    assert "reachable: true" in lower or "reachable true" in lower
    assert "http 404" in lower or "http_status: 404" in lower or "`http_status: 404`" in text.lower()
    assert "no usable metadata" in lower
    assert "provider remains disabled" in lower
    assert "trial rerun has not happened" in lower
    assert "full_match/8453" in lower
    assert "partial_match/8453" in lower
    assert "one target only first" in lower
    assert "no raw response body committed" in lower
    assert "endpoint validation is not trial evidence" in SCHEMA.read_text(encoding="utf-8").lower()
    assert '"green light rerun sourcify trial from vps"' in lower


def test_linked_docs_reference_endpoint_correction_plan():
    preflight = PREFLIGHT.read_text(encoding="utf-8").lower()
    runbook = RUNBOOK.read_text(encoding="utf-8").lower()
    approval = APPROVAL.read_text(encoding="utf-8").lower()
    dataset = DATASET.read_text(encoding="utf-8").lower()
    claims = CLAIMS.read_text(encoding="utf-8").lower()

    assert "sourcify_endpoint_correction_plan.md" in preflight
    assert "sourcify_endpoint_correction_plan.md" in runbook
    assert "rerun blocked pending endpoint validation" in approval
    assert "sourcify_endpoint_correction_plan.md" in dataset
    assert "sourcify endpoint correction plan" in claims
    assert "planned / no new network calls / no usable metadata yet" in claims


def test_endpoint_correction_docs_forbid_unsafe_positive_phrases():
    combined = (
        PLAN.read_text(encoding="utf-8")
        + PREFLIGHT.read_text(encoding="utf-8")
        + RUNBOOK.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
        + DATASET.read_text(encoding="utf-8")
        + SCHEMA.read_text(encoding="utf-8")
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


def test_env_unchanged_during_endpoint_correction_plan_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PLAN.read_text(encoding="utf-8")
    _ = PREFLIGHT.read_text(encoding="utf-8")
    _ = RUNBOOK.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = DATASET.read_text(encoding="utf-8")
    _ = SCHEMA.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
