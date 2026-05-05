from pathlib import Path


DOC = Path("docs/18_investor/BUSINESS_MODEL_AND_MARKET_REALITY_CHECK.md")
LEDGER = Path("docs/18_investor/CLAIMS_LEDGER.md")


def test_business_model_market_reality_required_phrases():
    text = DOC.read_text(encoding="utf-8")
    required = [
        "BeezShield builds guardians, not traders",
        "pre-execution trust",
        "$7.84B",
        "$52.62B",
        "18%",
        "x402 per risk decision",
        "AgentKit-style example",
        "official AgentKit provider",
        "simulation adapter boundary",
        "no live simulation provider",
        "no historical evaluation dataset",
    ]
    for phrase in required:
        assert phrase in text


def test_business_model_market_reality_forbidden_phrases():
    text = DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "honeypot detection live",
        "sentinel would have caught",
        "guaranteed protection",
        "full protection",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_claims_ledger_has_requested_entries():
    text = LEDGER.read_text(encoding="utf-8")
    required = [
        "$7.84B",
        "$52.62B",
        "18% highly confident managing agent identities/security",
        "Time-to-Trust 2026-2027",
        "outcome-based 10-20% saved value",
        "honeypot simulation live",
        "simulation adapter boundary is live",
        "official AgentKit provider",
    ]
    for phrase in required:
        assert phrase in text
