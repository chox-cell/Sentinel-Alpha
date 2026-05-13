import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = REPO_ROOT / "reports/provider_trials/sourcify_vps_preflight.v11.2.json"
REPORT_MD = REPO_ROOT / "reports/provider_trials/sourcify_vps_preflight.v11.2.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_vps_preflight_json_exists_and_matches_recorded_posture():
    assert REPORT_JSON.exists()
    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))

    assert data["report_type"] == "sourcify_vps_connectivity_preflight"
    assert data["version"] == "v11.2"
    assert data["preflight_run"] is True
    assert data["trial_rerun"] is False
    assert data["trial_rerun_approved"] is False
    assert data["provider_active"] is False
    assert data["runtime_provider_enabled"] is False
    assert data["dataset_wide_lookup"] is False
    assert data["requests_attempted"] == 1
    assert data["provider_name"] == "sourcify"
    assert data["api_keys_required"] is False
    assert data["paid_calls_allowed"] is False
    assert data["raw_response_stored"] is False
    assert data["raw_body_stored"] is False
    assert data["secret_material_observed"] is False
    assert data["notSecurityGuarantee"] is True
    assert data["reachable"] is True
    assert data["http_status"] == 404
    assert data["error_type"] == "http_error"
    assert data["usable_metadata_received"] is False
    assert data["preflight_result"] == "reachable_http_404"
    assert data["endpoint_label"] == "sourcify_health"
    assert data["endpoint_hash"] == "0a952078645f1ffa5f743ea1ea170b2e60ff74f6d1ab07221276c5e8fa14f9d2"
    assert data["env_hash_before"] == data["env_hash_after"]


def test_vps_preflight_markdown_connectivity_only():
    md = REPORT_MD.read_text(encoding="utf-8").lower()

    assert "vps preflight completed" in md
    assert "connectivity evidence only" in md
    assert "no usable abi/source metadata was received" in md
    assert "no dataset-wide lookup" in md
    assert "no trial rerun" in md
    assert "provider remains disabled" in md
    assert "no raw body was stored" in md


def test_approval_and_claims_reflect_v11_2_preflight():
    approval = APPROVAL.read_text(encoding="utf-8").lower()
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()

    assert "v11.2_preflight_run: true" in approval
    assert "trial_rerun: false" in approval
    assert "vps sourcify connectivity preflight result" in ledger
    assert "completed / reachable_http_404 / no trial rerun" in ledger


def test_vps_preflight_artifacts_forbid_unsafe_positive_phrases():
    combined = (
        REPORT_JSON.read_text(encoding="utf-8")
        + REPORT_MD.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
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


def test_env_unchanged_during_vps_preflight_result_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = REPORT_JSON.read_bytes()
    _ = REPORT_MD.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
