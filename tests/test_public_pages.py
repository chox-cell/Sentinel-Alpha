from pathlib import Path


PAGES = [
    Path("apps/website/docs.html"),
    Path("apps/website/sdk.html"),
    Path("apps/website/agentkit.html"),
    Path("apps/website/x402.html"),
    Path("apps/website/trust.html"),
    Path("apps/website/pricing.html"),
    Path("apps/website/about.html"),
    Path("apps/website/changelog.html"),
]


def _merged() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in PAGES)


def test_public_pages_exist():
    for page in PAGES:
        assert page.exists(), f"missing page: {page}"


def test_public_pages_required_copy():
    merged = _merged().lower()
    required = [
        "@beezshield/sentinel",
        "npm install @beezshield/sentinel",
        "contract_address",
        "agentkit-style example",
        "official provider coming next",
    ]
    for token in required:
        assert token in merged


def test_public_pages_no_overclaims():
    merged = _merged().lower()
    forbidden = [
        "agentkit provider live",
        "official agentkit integration live",
        "guaranteed protection",
        "automatic x402 settlement",
        "mcp live",
        "a2a live",
    ]
    for token in forbidden:
        assert token not in merged


def test_index_nav_has_required_links():
    html = Path("apps/website/index.html").read_text(encoding="utf-8")
    for href in (
        "docs.html",
        "pricing.html",
        "trust.html",
        "about.html",
        "https://github.com/chox-cell/Sentinel-Alpha",
        "https://www.npmjs.com/package/@beezshield/sentinel",
    ):
        assert href in html
