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
    Path("apps/website/demo.html"),
    Path("apps/website/manifesto.html"),
]

INDEX = Path("apps/website/index.html")
REGISTRY_X402 = Path("apps/website/registry/x402scan.html")
PILOT_TRUST_RECEIPT = Path("apps/website/pilot/trust-receipt.html")
PILOT_TREASURY = "0x3cf9C2E55485fF8DAFfb59c84a0fa7c03bDbAeaf"


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
    assert "Developer quickstart" in html
    assert "payable x402 resource" in low
    assert "directory listing only" in low
    assert "does not imply partnership" in low
    assert "security guarantee" in low
    assert "POST https://api.beezshield.com/contracts/risk-score" in html
    assert "0.02 USDC" in html
    assert "BeezShield" in html
    assert "Machine Trust Infrastructure" in html
    assert "favicon.svg" in html
    assert "agentic.market: validator passed (not listed)" in low


def test_no_wordmark_references_in_any_active_file():
    # All html/css pages under apps/website
    active_files = [INDEX, REGISTRY_X402, PILOT_TRUST_RECEIPT, Path("apps/website/styles.css")] + PAGES
    for path in active_files:
        if path.exists():
            content = path.read_text(encoding="utf-8").lower()
            assert "beezshield-wordmark.svg" not in content
            assert "hero-wordmark" not in content
            assert "brand-wordmark" not in content


def test_logo_count_patterns():
    import re
    index_html = INDEX.read_text(encoding="utf-8")
    # Assert exactly one logo in header
    nav_match = re.search(r'<nav class="top-nav">.*?</nav>', index_html, re.DOTALL)
    assert nav_match is not None
    nav_logos = re.findall(r'beezshield-logo\.svg', nav_match.group(0))
    assert len(nav_logos) == 1
    
    # Assert exactly one logo in footer
    footer_match = re.search(r'<footer class="site-footer">.*?</footer>', index_html, re.DOTALL)
    assert footer_match is not None
    footer_logos = re.findall(r'beezshield-logo\.svg', footer_match.group(0))
    assert len(footer_logos) == 1
    
    # Assert at most one icon in proof sections (not header/footer)
    total_logos = re.findall(r'beezshield-logo\.svg', index_html)
    assert len(total_logos) == 2

    # Assert exactly one logo in header, one in footer, and 2 total for all subpages
    for page in PAGES:
        html = page.read_text(encoding="utf-8")
        p_nav_match = re.search(r'<nav class="top-nav">.*?</nav>', html, re.DOTALL)
        assert p_nav_match is not None, f"Missing nav header in {page}"
        p_nav_logos = re.findall(r'beezshield-logo\.svg', p_nav_match.group(0))
        assert len(p_nav_logos) == 1, f"Should have exactly 1 logo in nav of {page}"

        p_footer_match = re.search(r'<footer class="site-footer">.*?</footer>', html, re.DOTALL)
        assert p_footer_match is not None, f"Missing footer in {page}"
        p_footer_logos = re.findall(r'beezshield-logo\.svg', p_footer_match.group(0))
        assert len(p_footer_logos) == 1, f"Should have exactly 1 logo in footer of {page}"

        p_total_logos = re.findall(r'beezshield-logo\.svg', html)
        assert len(p_total_logos) == 2, f"Should have exactly 2 logos total in {page}"
    
    # Registry page header logo rule
    registry_html = REGISTRY_X402.read_text(encoding="utf-8")
    reg_nav_match = re.search(r'<nav class="top-nav">.*?</nav>', registry_html, re.DOTALL)
    assert reg_nav_match is not None
    reg_nav_logos = re.findall(r'beezshield-logo\.svg', reg_nav_match.group(0))
    assert len(reg_nav_logos) == 1
    
    reg_footer_match = re.search(r'<footer class="site-footer">.*?</footer>', registry_html, re.DOTALL)
    assert reg_footer_match is not None
    reg_footer_logos = re.findall(r'beezshield-logo\.svg', reg_footer_match.group(0))
    assert len(reg_footer_logos) == 1

    reg_total_logos = re.findall(r'beezshield-logo\.svg', registry_html)
    assert len(reg_total_logos) == 2

    # Pilot page logo counts
    assert PILOT_TRUST_RECEIPT.exists()
    pilot_html = PILOT_TRUST_RECEIPT.read_text(encoding="utf-8")
    pilot_nav_match = re.search(r'<nav class="top-nav">.*?</nav>', pilot_html, re.DOTALL)
    assert pilot_nav_match is not None
    pilot_nav_logos = re.findall(r'beezshield-logo\.svg', pilot_nav_match.group(0))
    assert len(pilot_nav_logos) == 1

    pilot_footer_match = re.search(r'<footer class="site-footer">.*?</footer>', pilot_html, re.DOTALL)
    assert pilot_footer_match is not None
    pilot_footer_logos = re.findall(r'beezshield-logo\.svg', pilot_footer_match.group(0))
    assert len(pilot_footer_logos) == 1

    pilot_total_logos = re.findall(r'beezshield-logo\.svg', pilot_html)
    assert len(pilot_total_logos) == 2


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


def test_pilot_trust_receipt_page():
    assert PILOT_TRUST_RECEIPT.exists()
    html = PILOT_TRUST_RECEIPT.read_text(encoding="utf-8")
    low = html.lower()
    
    # Required pricing and description copy
    assert "$25" in html
    assert "$50" in html
    assert "$250" in html
    assert "agentkit" in low
    assert "sentinel" in low
    assert "redacted" in low
    assert "json" in low
    assert "receipt" in low
    
    # Required safety disclaimers
    assert "security guarantee" in low
    assert "execution quality guarantee" in low
    assert "endorsement" in low
    assert "partnership" in low
    
    # Single logo checks (logo file name check)
    assert "beezshield-wordmark.svg" not in html

    # Review-ready packet components
    assert "review-ready packet" in low
    assert "$50 trust receipt pilot" in low
    assert "json" in low and "markdown" in low
    assert "manual" in low
    assert "redacted proposed action" in low
    assert "sentinel decision" in low
    assert "post-action result ref" in low
    assert "not-checked boundary" in low

    # Checkout v0 form & copy buttons
    assert "pay for pilot" in low
    assert "payment tx hash" in low or "payment_tx_hash" in low
    assert "proposed action summary" in low or "proposed_action_summary" in low
    assert "chain" in low
    assert "result ref" in low or "result_ref_optional" in low
    assert "copy checkout json" in low
    assert "copy payment address" in low
    assert PILOT_TREASURY.lower() in low
    assert "not escrow" in low or "no escrow" in low
    assert "manual verification" in low



def test_robots_txt():
    robots_path = Path("apps/website/robots.txt")
    assert robots_path.exists()
    content = robots_path.read_text(encoding="utf-8")
    assert "User-agent: *" in content
    assert "Allow: /" in content
    assert "Sitemap: https://beezshield.com/sitemap.xml" in content


def test_sitemap_xml():
    sitemap_path = Path("apps/website/sitemap.xml")
    assert sitemap_path.exists()
    content = sitemap_path.read_text(encoding="utf-8")
    required_urls = [
        "https://beezshield.com/",
        "https://beezshield.com/index.html",
        "https://beezshield.com/about.html",
        "https://beezshield.com/docs.html",
        "https://beezshield.com/pricing.html",
        "https://beezshield.com/trust.html",
        "https://beezshield.com/sdk.html",
        "https://beezshield.com/agentkit.html",
        "https://beezshield.com/x402.html",
        "https://beezshield.com/registry/x402scan.html",
        "https://beezshield.com/pilot/trust-receipt.html",
    ]
    for url in required_urls:
        assert f"<loc>{url}</loc>" in content


def test_security_txt():
    sec_path = Path("apps/website/.well-known/security.txt")
    assert sec_path.exists()
    content = sec_path.read_text(encoding="utf-8")
    assert "Contact: https://github.com/chox-cell/Sentinel-Alpha/issues" in content
    assert "Disclosure: https://beezshield.com/trust.html" in content
    # Ensure no fake/unverified emails or claims
    assert "@beezshield.com" not in content
    assert "@gmail.com" not in content
    assert "partnership" not in content.lower()
    assert "guarantee" not in content.lower()


def test_homepage_organization_json_ld():
    homepage_path = Path("apps/website/index.html")
    assert homepage_path.exists()
    content = homepage_path.read_text(encoding="utf-8")
    
    import json
    import re
    # Extract JSON-LD script blocks
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    org_found = False
    for block in blocks:
        try:
            data = json.loads(block.strip())
            if data.get("@type") == "Organization":
                assert data.get("name") == "BeezShield"
                assert data.get("url") == "https://beezshield.com"
                assert data.get("description") == "Machine Trust Infrastructure for autonomous agent actions."
                assert "https://github.com/chox-cell/Sentinel-Alpha" in data.get("sameAs", [])
                assert "https://www.npmjs.com/package/@beezshield/sentinel" in data.get("sameAs", [])
                org_found = True
        except json.JSONDecodeError:
            continue
    assert org_found, "Organization JSON-LD block not found on homepage"


def test_trust_page_forbidden_phrases():
    trust_path = Path("apps/website/trust.html")
    assert trust_path.exists()
    content = trust_path.read_text(encoding="utf-8")
    
    # Strip footer to avoid matching the exact required footer copy
    import re
    body_content = re.sub(r'<footer class="site-footer">.*?</footer>', '', content, flags=re.DOTALL).lower()
    
    forbidden = [
        "official partnership",
        "endorsed by",
        "guaranteed protection",
        "security guarantee",
        "certified integration",
    ]
    for phrase in forbidden:
        assert phrase not in body_content, f"Found forbidden phrase '{phrase}' in trust.html main body"


def test_footer_claim_note():
    expected_copy = "BeezShield provides pre-execution risk decision support and Trust Receipt tooling for autonomous agent workflows. Directory and validator signals are discoverability evidence only, not security guarantees, endorsements, or official partnerships."
    all_pages = PAGES + [INDEX, REGISTRY_X402, PILOT_TRUST_RECEIPT]
    
    for page in all_pages:
        html = page.read_text(encoding="utf-8")
        assert expected_copy in html, f"Missing expected footer copy in {page}"
        
        # Verify Coinbase/Base/Agentic.Market are not mentioned in the footer section
        import re
        footer_match = re.search(r'<footer class="site-footer">.*?</footer>', html, re.DOTALL)
        assert footer_match is not None, f"Missing footer in {page}"
        footer_content = footer_match.group(0).lower()
        
        for forbidden_term in ["coinbase", "base", "agentic.market"]:
            assert forbidden_term not in footer_content, f"Forbidden term '{forbidden_term}' found in footer of {page}"


