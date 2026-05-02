from pathlib import Path


def test_index_core_positioning_and_links():
    html = Path("apps/website/index.html").read_text(encoding="utf-8")
    assert "Pre-execution decision engine for agents" in html
    assert "https://8004scan.io/agents/base/45967" in html
    assert "https://api.beezshield.com/contracts/risk-score" in html
    assert "x402" in html.lower()
    assert "ERC-8004" in html


def test_main_js_has_swarm_functions():
    js = Path("apps/website/main.js").read_text(encoding="utf-8")
    assert "function spawnSwarm()" in js
    assert "function animateToTarget(" in js
    assert "function applyRiskState(" in js


def test_css_has_swarm_hive_trust_classes():
    css = Path("apps/website/styles.css").read_text(encoding="utf-8")
    assert ".swarm-layer" in css
    assert ".hive-visual" in css
    assert ".trust-links" in css
    assert ".swarm-state-stable" in css
    assert ".swarm-state-warning" in css
    assert ".swarm-state-critical" in css


def test_llms_txt_discovery_fields():
    llms = Path("apps/website/llms.txt").read_text(encoding="utf-8")
    assert "https://api.beezshield.com/contracts/risk-score" in llms
    assert "basic: 0.02" in llms
    assert "executive: 0.05" in llms
    assert "premium: 0.10" in llms
    assert "priority: 0.15" in llms
    assert "https://8004scan.io/agents/base/45967" in llms


def test_no_fake_claims_or_secrets():
    files = [
        Path("apps/website/index.html"),
        Path("apps/website/main.js"),
        Path("apps/website/styles.css"),
        Path("apps/website/llms.txt"),
        Path("apps/website/llms-full.txt"),
        Path("README.md"),
    ]
    banned = [
        "MCP live",
        "A2A live",
        "guaranteed protection",
        "attack victim",
        "pay to survive",
        "BEGIN PRIVATE KEY",
        "PRIVATE_KEY=",
        "API_KEY=",
        "SECRET_KEY=",
        "AWS_SECRET_ACCESS_KEY",
        "xoxb-",
        "sk_live_",
    ]
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in banned:
            assert phrase not in text
