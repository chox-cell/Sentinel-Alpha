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

INDEX = Path("apps/website/index.html")
REGISTRY_X402 = Path("apps/website/registry/x402scan.html")


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
    html = INDEX.read_text(encoding="utf-8")
    for href in (
        "docs.html",
        "pricing.html",
        "trust.html",
        "about.html",
        "https://github.com/chox-cell/Sentinel-Alpha",
        "https://www.npmjs.com/package/@beezshield/sentinel",
    ):
        assert href in html


def test_index_x402scan_brand_surface():
    html = INDEX.read_text(encoding="utf-8")
    low = html.lower()
    assert "brand/beezshield-logo.svg?v=clean-logo-2" in html
    assert "beezshield-wordmark.svg" not in html
    assert "hero-wordmark" not in html
    assert "Registered on x402scan" in html
    assert "payable x402 resource" in low
    assert "directory listing only" in low
    assert "does not imply partnership" in low
    assert "POST https://api.beezshield.com/contracts/risk-score" in html
    assert "0.02 USDC" in html
    assert "BeezShield" in html
    assert "Machine Trust Infrastructure" in html
    assert "favicon.svg" in html
    assert "Browser demo paused" in html


def test_logo_no_text():
    logo = Path("apps/website/brand/beezshield-logo.svg").read_text(encoding="utf-8")
    favicon = Path("apps/website/favicon.svg").read_text(encoding="utf-8")
    
    for svg in [logo, favicon]:
        assert "<text" not in svg
        assert "BeezShield" not in svg


def test_registry_x402scan_page():
    assert REGISTRY_X402.exists()
    reg = REGISTRY_X402.read_text(encoding="utf-8").lower()
    assert "registered" in reg
    assert "/contracts/risk-score" in reg
    assert "what this proves" in reg
    assert "what this does not prove" in reg
    assert "agentic.market" in reg
    assert "pay.sh" in reg
    assert "ampersend" in reg
