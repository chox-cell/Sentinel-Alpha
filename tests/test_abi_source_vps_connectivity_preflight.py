import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_VPS_CONNECTIVITY_PREFLIGHT.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
RESULT_SCHEMA = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_preflight_doc_exists_and_records_v10_8a_posture():
    assert PREFLIGHT.exists()
    text = PREFLIGHT.read_text(encoding="utf-8")
    lower = text.lower()

    assert "VPS Sourcify Connectivity Preflight v1" in text
    assert "v10.8a" in lower
    assert "all five rows returned network_error" in lower
    assert "no usable metadata was received" in lower
    assert "provider remains disabled" in lower
    assert "vps preflight not run yet" in lower
    assert "max 1 sourcify endpoint check" in lower
    assert "no raw provider response committed" in lower
    assert '"green light rerun sourcify trial from vps"' in lower


def test_preflight_doc_lists_allowed_statuses():
    text = PREFLIGHT.read_text(encoding="utf-8").lower()
    for status in (
        "not_run",
        "reachable",
        "timeout",
        "network_error",
        "dns_error",
        "tls_error",
        "http_error",
        "blocked",
    ):
        assert status in text


def test_linked_docs_reference_vps_preflight_and_rerun_phrase():
    runbook = RUNBOOK.read_text(encoding="utf-8").lower()
    approval = APPROVAL.read_text(encoding="utf-8").lower()
    schema = RESULT_SCHEMA.read_text(encoding="utf-8").lower()
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()

    assert "abi_source_provider_vps_connectivity_preflight.md" in runbook
    assert "green light rerun sourcify trial from vps" in approval
    assert "preflight status is not trial evidence" in schema
    assert "vps sourcify connectivity preflight" in ledger
    assert "planned / not run" in ledger


def test_preflight_docs_forbid_unsafe_positive_phrases():
    combined = (
        PREFLIGHT.read_text(encoding="utf-8")
        + RUNBOOK.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
        + RESULT_SCHEMA.read_text(encoding="utf-8")
        + CLAIMS_LEDGER.read_text(encoding="utf-8")
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


def test_env_unchanged_during_preflight_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PREFLIGHT.read_text(encoding="utf-8")
    _ = RUNBOOK.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = RESULT_SCHEMA.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
