from pathlib import Path


DOC = Path("docs/18_investor/AGENT_COMMERCE_INTELLIGENCE_NOTES.md")


def test_agent_commerce_notes_exists():
    assert DOC.exists(), f"missing {DOC}"


def test_agent_commerce_notes_required_content():
    text = DOC.read_text(encoding="utf-8")
    required = [
        "Useful vision retained",
        "Unsafe claim corrections",
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
        "agentic commerce increases need for pre-execution trust gates",
        "autonomous agents need policy layers before contracts/assets/payments/tools",
        "Trust Objects are future commerce safety roadmap",
        "UCP/AP2 are roadmap commerce context only",
        "future middleware/intent-boundary context; not live prevention claim",
        "simulation/heuristic roadmap; no detection guarantee",
        "guardian layer for autonomous execution",
        "usage-based risk decision pricing",
        "roadmap context, not runtime integration",
        "ERC-8004 identity live; broader reputation/validation roadmap",
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
        "prompt-injection prevention is live",
        "honeypot detection is live",
        "live simulation is enabled",
        "UCP/AP2 integration is live",
        "Trust Object Model is live",
        "BeezShield taxes every autonomous economic action",
    ]
    for token in forbidden:
        assert token not in text


def test_central_bank_of_trust_not_public_safe_and_guardian_wording_present():
    text = DOC.read_text(encoding="utf-8")
    assert "Central Bank of Trust" in text
    assert "guardian layer for autonomous execution" in text


def test_env_unchanged_during_agent_commerce_notes_tests():
    from pathlib import Path
    import hashlib

    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
