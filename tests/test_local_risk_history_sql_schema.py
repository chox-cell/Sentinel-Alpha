import hashlib
from pathlib import Path


SCHEMA = Path("db/schema/local_risk_history_v1.sql")
PLAN_DOC = Path("docs/16_launch/SENTINEL_LOCAL_RISK_HISTORY_DB_PLAN.md")


def test_schema_file_exists_and_has_required_tables():
    assert SCHEMA.exists()
    text = SCHEMA.read_text(encoding="utf-8").lower()
    required_tables = [
        "scan_requests",
        "risk_results",
        "contract_observations",
        "asset_classifications",
        "security_signals",
        "attestations",
        "x402_payment_events",
        "integration_clients",
        "provider_observations",
    ]
    for table in required_tables:
        assert table in text


def test_schema_uses_safe_constructs_and_indexes():
    text = SCHEMA.read_text(encoding="utf-8").lower()
    assert "create table if not exists" in text
    assert "jsonb" in text
    assert "timestamptz" in text
    assert "create index if not exists" in text
    assert "drop database" not in text


def test_schema_has_required_security_comments():
    text = SCHEMA.read_text(encoding="utf-8").lower()
    assert "no private keys" in text
    assert "no seed phrases" in text
    assert "no raw secrets" in text
    assert "payment proof minimized" in text


def test_plan_doc_still_no_runtime_dependency_and_no_db_url_required():
    text = PLAN_DOC.read_text(encoding="utf-8").lower()
    assert "no runtime db dependency now" in text
    assert "database_url" in text
    assert "not required yet" in text


def test_env_unchanged_during_schema_checks():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = SCHEMA.read_text(encoding="utf-8")
    _ = PLAN_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
