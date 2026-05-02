import os
from bs4 import BeautifulSoup

def test_beezshield_prime_website():
    html_path = "apps/website/index.html"
    assert os.path.exists(html_path), "index.html not found"

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    text_content = soup.get_text()

    # Required copy
    assert "Machine Trust Infrastructure for Autonomous Agents" in text_content
    assert "Pre-execution decision engine for agents" in text_content
    assert "Your agent should not execute blind" in text_content
    assert "api.beezshield.com" in html_content
    assert "8004scan.io/agents/base/45967" in html_content
    assert "x402" in text_content
    assert "ERC-8004" in text_content
    assert "Copy cURL" in text_content
    assert "Add to your bot" in text_content

    # SDK Preview section
    assert "Build with Sentinel Alpha" in text_content
    assert "@beezshield/sentinel" in text_content
    assert "createSentinelClient()" in text_content
    assert "scoreContract()" in text_content
    assert "decideBeforeExecution()" in text_content
    assert "Developer Preview Soon" in text_content
    assert "coming next" in text_content.lower()

    # Prohibited claims
    assert "MCP live" not in text_content.lower()
    assert "A2A live" not in text_content.lower()
    assert "attack victim" not in text_content.lower()
    assert "pay to survive" not in text_content.lower()
    assert "guaranteed protection" not in text_content.lower()

    # Docs file
    assert os.path.exists("docs/16_launch/BEEZSHIELD_PRIME_WEBSITE.md"), "Docs file not found"
