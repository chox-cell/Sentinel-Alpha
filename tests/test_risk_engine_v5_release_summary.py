from pathlib import Path


DOC = Path("docs/16_launch/SENTINEL_RISK_ENGINE_V5_RELEASE_SUMMARY.md")


def test_v5_release_summary_exists():
    assert DOC.exists(), f"missing {DOC}"


def test_v5_release_summary_required_content():
    text = DOC.read_text(encoding="utf-8").lower()
    required = [
        "boundary-only",
        "simulation is not live by default",
        "mempool/mev monitoring is not live by default",
        "@beezshield/sentinel",
        "fallback-aware pre-execution risk decision layer",
    ]
    for token in required:
        assert token in text


def test_v5_release_summary_forbidden_claims_absent():
    text = DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "guaranteed protection",
        "detects all honeypots",
        "prevents mev",
        "catches most bytecode",
        "full intent verification",
    ]
    for token in forbidden:
        assert token not in text
