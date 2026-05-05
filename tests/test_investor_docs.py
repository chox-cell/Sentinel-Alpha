from pathlib import Path


DOCS = [
    Path("docs/18_investor/SENTINEL_ALPHA_INVESTOR_THESIS.md"),
    Path("docs/18_investor/TECHNICAL_ACQUISITION_PITCH.md"),
    Path("docs/18_investor/CLAIMS_LEDGER.md"),
]


def _merged() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in DOCS)


def test_investor_docs_exist():
    for p in DOCS:
        assert p.exists(), f"missing {p}"


def test_investor_docs_required_content():
    merged = _merged().lower()
    required = [
        "@beezshield/sentinel",
        "x402",
        "erc-8004",
        "agentkit-style example",
        "official provider coming next",
    ]
    for token in required:
        assert token in merged


def test_sandbox_is_roadmap_not_live():
    merged = _merged().lower()
    assert "sandbox simulation workers are on the roadmap" in merged
    assert "sandbox simulation is currently live" not in merged


def test_investor_docs_no_forbidden_claims():
    merged = _merged().lower()
    forbidden = [
        "guaranteed protection",
        "agentkit provider live",
        "official agentkit integration live",
        "automatic x402 settlement",
        "impossible to compete",
        "only guardian",
        "51%",
    ]
    for token in forbidden:
        assert token not in merged
