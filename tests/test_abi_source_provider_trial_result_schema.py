import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DOC = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"

RESULT_FIELDS = [
    "result_version",
    "trial_id",
    "chain",
    "contract_address_hash",
    "category",
    "provider_name",
    "provider_endpoint_hash",
    "lookup_status",
    "verified_source_status",
    "abi_available",
    "abi_function_count",
    "abi_function_names_sample",
    "source_fetch_error_type",
    "latency_ms",
    "timeout_ms",
    "fallback_mode",
    "confidence_impact",
    "response_sanitized",
    "raw_response_stored",
    "secret_material_observed",
    "created_at",
    "notes",
]

LOOKUP_STATUSES = [
    "not_run",
    "dry_run_not_executed",
    "success",
    "timeout",
    "rate_limited",
    "invalid_response",
    "provider_down",
    "unsupported_chain",
    "unsupported_provider",
    "error",
]


def test_result_schema_doc_exists_and_core_gates():
    assert SCHEMA_DOC.exists()
    text = SCHEMA_DOC.read_text(encoding="utf-8")
    lower = text.lower()

    assert "ABI/Source Provider Trial Result Schema v1" in text
    assert "schema only" in lower
    assert "trial not run" in lower
    assert "no provider trial executed" in lower
    assert "no live provider enabled" in lower
    assert "no network call performed" in lower
    assert "no api key required" in lower

    for name in RESULT_FIELDS:
        assert f"`{name}`" in text, f"missing field: {name}"

    for status in LOOKUP_STATUSES:
        assert f"`{status}`" in text, f"missing lookup_status: {status}"

    assert "## 6) Privacy rules" in text or "privacy rules" in lower

    for tid in ["T01", "T02", "T03", "T04", "T05"]:
        assert f'"{tid}"' in text
    assert lower.count('"lookup_status": "not_run"') == 5

    assert '"raw_response_stored": false' in text
    assert '"secret_material_observed": false' in text

    assert "no full abi coverage" in lower
    assert "does not promise verified source" in lower


def test_claims_ledger_schema_row():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "abi/source trial result schema" in ledger
    assert "schema prepared / trial not run" in ledger


def test_schema_forbidden_phrases_absent():
    text = SCHEMA_DOC.read_text(encoding="utf-8").lower()
    forbidden = [
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
        assert token not in text, f"unexpected phrase: {token}"


def test_env_unchanged_during_schema_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = SCHEMA_DOC.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
