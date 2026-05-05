from pathlib import Path


DOC = Path("docs/18_investor/AGENT_COMMERCE_INTELLIGENCE_NOTES.md")


def test_agent_commerce_notes_exists():
    assert DOC.exists(), f"missing {DOC}"


def test_agent_commerce_notes_required_content():
    text = DOC.read_text(encoding="utf-8")
    required = [
        "Agent Commerce Trust Object",
        "pre-execution trust",
        "Google UCP",
        "AP2",
        "Peppol",
        "Salesforce",
        "B2B deal scout is a separate future product idea",
        "BeezShield builds guardians, not traders.",
        "BeezShield agents verify, score, explain, block, review, and attest before autonomous execution.",
        "Sentinel Alpha protects onchain contract/asset execution.",
        "Ema-Bee is a future commerce safety gate concept, not a B2B arbitrage/trading agent.",
        "contracts/assets first",
        "roadmap only",
    ]
    for token in required:
        assert token in text


def test_agent_commerce_notes_forbidden_phrases_absent():
    text = DOC.read_text(encoding="utf-8")
    forbidden = [
        "every company has /.well-known/ucp",
        "Citi/JPM fund any agent",
        "Peppol gives internal RFQs",
        "pivot product focus",
        "Ema-Bee is live",
        "agents trade autonomously for profit",
    ]
    for token in forbidden:
        assert token not in text
