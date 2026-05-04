from pathlib import Path


DOCS = [
    Path("docs/17_growth/BUILDER_OUTREACH_PACK.md"),
    Path("docs/17_growth/AGENTKIT_TARGETS.md"),
    Path("docs/17_growth/GITHUB_ISSUE_TEMPLATE.md"),
    Path("docs/17_growth/LAUNCH_POSTS.md"),
]


def test_growth_docs_exist():
    for p in DOCS:
        assert p.exists(), f"missing {p}"


def test_growth_docs_required_content():
    merged = "\n".join(p.read_text(encoding="utf-8") for p in DOCS)
    required = [
        "@beezshield/sentinel",
        "npm install @beezshield/sentinel",
        "contract_address",
        "AgentKit-style example",
        "official provider coming next",
    ]
    for token in required:
        assert token in merged


def test_growth_docs_no_overclaims():
    merged = "\n".join(p.read_text(encoding="utf-8").lower() for p in DOCS)
    forbidden = [
        "agentkit provider live",
        "official agentkit integration live",
        "guaranteed protection",
        "automatic x402 settlement",
    ]
    for token in forbidden:
        assert token not in merged
