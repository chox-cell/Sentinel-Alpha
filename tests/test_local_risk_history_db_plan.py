from pathlib import Path


DOC = Path("docs/16_launch/SENTINEL_LOCAL_RISK_HISTORY_DB_PLAN.md")


def test_local_risk_history_db_plan_required_content():
    text = DOC.read_text(encoding="utf-8")
    required = [
        "local Postgres",
        "no managed DB",
        "scan_requests",
        "risk_results",
        "contract_observations",
        "asset_classifications",
        "security_signals",
        "attestations",
        "x402_payment_events",
        "no private keys",
        "no seed phrases",
        "no runtime DB dependency now",
        "DATABASE_URL",
        "not required yet",
    ]
    for token in required:
        assert token in text


def test_supabase_is_postponed_not_default():
    text = DOC.read_text(encoding="utf-8").lower()
    assert "supabase" in text
    assert ("not default" in text) or ("postponed" in text)


def test_no_supabase_service_role_required_runtime_key_claim():
    text = DOC.read_text(encoding="utf-8")
    assert "SUPABASE_SERVICE_ROLE_KEY" not in text
