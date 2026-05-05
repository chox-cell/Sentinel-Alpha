from pathlib import Path


ROADMAP = Path("docs/16_launch/SENTINEL_RISK_ENGINE_V5_ROADMAP.md")
CLAIMS = Path("docs/18_investor/CLAIMS_LEDGER.md")


def _between(text: str, start: str, end: str) -> str:
    s = text.find(start)
    if s == -1:
        return ""
    s += len(start)
    if not end:
        return text[s:]
    e = text.find(end, s)
    if e == -1:
        return text[s:]
    return text[s:e]


def test_v5_roadmap_docs_exist():
    assert ROADMAP.exists(), f"missing {ROADMAP}"
    assert CLAIMS.exists(), f"missing {CLAIMS}"


def test_v5_roadmap_required_sections_and_lines():
    text = ROADMAP.read_text(encoding="utf-8")
    required = [
        "v5.1 Asset Classification Engine",
        "v5.2.1 ERC-8004 Identity Signals",
        "v5.8 Intent Alignment Layer",
        "v5.9 Mempool / MEV Signal Layer",
        "Registered identity is not a safety guarantee.",
        "Unregistered identity is not proof of malice.",
    ]
    for token in required:
        assert token in text


def test_claims_ledger_new_source_and_roadmap_entries():
    text = CLAIMS.read_text(encoding="utf-8")
    assert "47.1% of active agents are monitored" in text
    assert "unknown identity creates 80% higher risk" in text
    assert "47.1% of active agents are monitored | needs source" in text
    assert "unknown identity creates 80% higher risk | needs source" in text
    assert "simulation is a strength signal, not a guarantee" in text
    assert "mempool sentiment is roadmap" in text


def test_forbidden_phrases_are_not_positive_claims():
    text = ROADMAP.read_text(encoding="utf-8")
    forbidden_block = _between(text, "## 8) Forbidden claims", "")
    assert "prevents MEV" in forbidden_block

    positive_area = text.replace(forbidden_block, "")
    forbidden_positive = [
        "catches most bytecode-level traps",
        "detects all honeypots",
        "guaranteed protection",
        "AgentKit provider live",
    ]
    for token in forbidden_positive:
        assert token not in positive_area
