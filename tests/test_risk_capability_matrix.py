from pathlib import Path


DOC = Path("docs/16_launch/SENTINEL_RISK_CAPABILITY_MATRIX.md")


def test_risk_capability_matrix_exists():
    assert DOC.exists(), f"missing {DOC}"


def test_risk_capability_matrix_required_content():
    text = DOC.read_text(encoding="utf-8")
    required = [
        "does not deeply analyze all contract types",
        "does not guarantee honeypot detection",
        "pre-execution risk decision layer",
        "@beezshield/sentinel",
        "AgentKit-style example",
        "verified source check",
        "proxy detection",
        "owner/admin permissions",
        "ERC20 tax/transfer behavior",
        "honeypot buy/sell simulation",
        "NFT contracts",
        "Zora creator coins",
    ]
    for token in required:
        assert token in text


def test_risk_capability_matrix_no_forbidden_claims():
    merged = DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "catches most bytecode-level traps",
        "guaranteed protection",
        "detects all honeypots",
        "covers all contract types",
    ]
    for token in forbidden:
        assert token not in merged
