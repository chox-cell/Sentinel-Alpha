import json
from pathlib import Path


def test_clean_distribution_assets_exist():
    required = [
        Path("docs/16_launch/CLEAN_DISTRIBUTION_ENGINE.md"),
        Path("docs/16_launch/RISK_FEED_STRATEGY.md"),
        Path("docs/16_launch/CLEAN_OUTREACH_COPY.md"),
        Path("docs/16_launch/REVENUE_PLAYBOOK.md"),
        Path("data/demo-risk-feed.json"),
        Path("apps/website/risk-feed.html"),
    ]
    for path in required:
        assert path.exists()


def test_demo_risk_feed_shape_and_disclaimers():
    feed = json.loads(Path("data/demo-risk-feed.json").read_text(encoding="utf-8"))
    assert isinstance(feed, list)
    assert len(feed) == 5
    for record in feed:
        assert record["source"] == "demo"
        assert record["chain"] == "base"
        assert "disclaimer" in record
        assert record["disclaimer"] == "demo sample, not accusation"


def test_readme_mentions_clean_distribution_engine():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "Clean Distribution Engine" in readme
    assert "https://beezshield.com" in readme
    assert "https://api.beezshield.com/contracts/risk-score" in readme
    assert "https://8004scan.io/agents/base/45967" in readme


def test_no_prohibited_phrases_or_fake_protocol_claims():
    files = [
        Path("docs/16_launch/CLEAN_DISTRIBUTION_ENGINE.md"),
        Path("docs/16_launch/RISK_FEED_STRATEGY.md"),
        Path("docs/16_launch/CLEAN_OUTREACH_COPY.md"),
        Path("docs/16_launch/REVENUE_PLAYBOOK.md"),
        Path("README.md"),
    ]
    banned = [
        "simulate attack on bot",
        "victim",
        "harassment",
        "extortion",
        "pay to survive",
        "mcp live support",
        "a2a live support",
        "supports mcp",
        "supports a2a",
    ]
    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in banned:
            assert phrase not in text
