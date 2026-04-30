import json
from pathlib import Path


def test_agent_discovery_files_exist():
    required = [
        Path("apps/website/llms.txt"),
        Path("apps/website/llms-full.txt"),
        Path("apps/website/.well-known/agent.json"),
        Path("apps/website/.well-known/x402.json"),
        Path("apps/website/robots.txt"),
        Path("apps/website/sitemap.xml"),
        Path("docs/16_launch/AGENT_DISCOVERY_STRATEGY.md"),
    ]
    for path in required:
        assert path.exists()


def test_agent_discovery_content_has_urls_and_pricing():
    llms = Path("apps/website/llms.txt").read_text(encoding="utf-8")
    llms_full = Path("apps/website/llms-full.txt").read_text(encoding="utf-8")
    agent_json = json.loads(Path("apps/website/.well-known/agent.json").read_text(encoding="utf-8"))
    x402_json = json.loads(Path("apps/website/.well-known/x402.json").read_text(encoding="utf-8"))

    assert "https://beezshield.com" in llms
    assert "https://api.beezshield.com/contracts/risk-score" in llms
    assert "https://8004scan.io/agents/base/45967" in llms
    assert "https://github.com/chox-cell/Sentinel-Alpha" in llms
    assert "basic: 0.02" in llms
    assert "executive: 0.05" in llms
    assert "premium: 0.10" in llms
    assert "priority: 0.15" in llms

    assert "bot pre-execution risk gate" in llms_full.lower()
    assert "defi agent safety" in llms_full.lower()
    assert "contract screening" in llms_full.lower()
    assert "execution policy decision" in llms_full.lower()

    assert agent_json["agent_id"] == "45967"
    assert agent_json["erc8004_url"] == "https://8004scan.io/agents/base/45967"
    assert agent_json["pricing_lanes"] == {
        "basic": "0.02",
        "executive": "0.05",
        "premium": "0.10",
        "priority": "0.15",
    }

    assert x402_json["network"] == "eip155:8453"
    assert x402_json["challenge_endpoint"] == "https://api.beezshield.com/internal/x402/challenge?lane=basic"
    assert x402_json["lanes_endpoint"] == "https://api.beezshield.com/internal/x402/lanes"


def test_agent_discovery_has_no_secrets_and_no_false_claims():
    files = [
        Path("apps/website/llms.txt"),
        Path("apps/website/llms-full.txt"),
        Path("apps/website/.well-known/agent.json"),
        Path("apps/website/.well-known/x402.json"),
        Path("docs/16_launch/AGENT_DISCOVERY_STRATEGY.md"),
    ]
    markers = [
        "BEGIN PRIVATE KEY",
        "PRIVATE_KEY=",
        "API_KEY=",
        "SECRET_KEY=",
        "AWS_SECRET_ACCESS_KEY",
        "xoxb-",
        "sk_live_",
    ]
    banned_claims = ["mcp live support", "a2a live support", "supports mcp", "supports a2a"]

    for path in files:
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for marker in markers:
            assert marker not in text
        for claim in banned_claims:
            assert claim not in lowered
