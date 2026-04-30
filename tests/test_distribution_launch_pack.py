from pathlib import Path


def test_distribution_launch_docs_exist():
    assert Path("docs/16_launch/DISTRIBUTION_LAUNCH_PACK.md").exists()
    assert Path("docs/16_launch/OUTREACH_COPY.md").exists()
    assert Path("docs/16_launch/LAUNCH_CHECKLIST.md").exists()


def test_readme_includes_live_links():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "https://beezshield.com" in readme
    assert "https://8004scan.io/agents/base/45967" in readme
    assert "https://api.beezshield.com/contracts/risk-score" in readme


def test_no_secrets_in_launch_docs():
    files = [
        Path("docs/16_launch/DISTRIBUTION_LAUNCH_PACK.md"),
        Path("docs/16_launch/OUTREACH_COPY.md"),
        Path("docs/16_launch/LAUNCH_CHECKLIST.md"),
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
    for path in files:
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            assert marker not in text
