from pathlib import Path


DOC = Path("docs/00_project/SENTINEL_ALPHA_ROADMAP_TRACKER.md")


def test_roadmap_tracker_exists():
    assert DOC.exists(), f"missing {DOC}"


def test_roadmap_tracker_required_content():
    text = DOC.read_text(encoding="utf-8").lower()
    required = [
        "@beezshield/sentinel",
        "/contracts/risk-score",
        "v6.1 local bytecode signal analyzer",
        "v6.2 abi / source provider adapter",
        "v6.3 local postgres risk history schema",
        "v7.0 outreach batch 1",
        "<= $10/month",
        "no paid quicknode by default",
        "no guaranteed protection",
        "no detects all honeypots",
        "no mev prevention",
    ]
    for token in required:
        assert token in text
