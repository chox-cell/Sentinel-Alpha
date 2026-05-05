from pathlib import Path


DOC = Path("docs/16_launch/BACKEND_DATA_PERSISTENCE_AUDIT.md")


def test_backend_data_persistence_audit_exists():
    assert DOC.exists(), f"missing {DOC}"


def test_backend_data_persistence_audit_required_mentions():
    text = DOC.read_text(encoding="utf-8").lower()
    required = [
        "/contracts/risk-score",
        "x402",
        "scanner engine",
        "scan requests",
        "risk results",
        "attestations",
        "payments",
        "redis",
        "postgres",
        "supabase",
        "cache",
        "stateless",
        "no secrets",
    ]
    for token in required:
        assert token in text
