from pathlib import Path


def test_builder_handoff_doc_exists():
    assert Path("docs/16_launch/BUILDER_HANDOFF_PACK.md").exists()


def test_website_has_builder_handoff_elements():
    html = Path("apps/website/index.html").read_text(encoding="utf-8")
    assert "Copy cURL" in html
    assert "Add to your bot" in html
    assert "Pre-execution decision engine for agents." in html
    assert "AgentKit integration: upcoming integration" in html


def test_readme_has_builder_handoff_section():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "Builder Handoff" in readme


def test_no_secrets_or_fake_live_protocol_claims():
    files = [
        Path("docs/16_launch/BUILDER_HANDOFF_PACK.md"),
        Path("apps/website/index.html"),
        Path("README.md"),
    ]
    markers = [
        "BEGIN PRIVATE KEY",
        "PRIVATE_KEY=",
        "API_KEY=",
        "SECRET_KEY=",
        "AWS_SECRET_ACCESS_KEY",
        "xoxb-",
        "sk_live_",
    ]
    banned_claims = ["mcp live support", "a2a live support", "supports mcp", "supports a2a"]
    for path in files:
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for marker in markers:
            assert marker not in text
        for claim in banned_claims:
            assert claim not in lowered
