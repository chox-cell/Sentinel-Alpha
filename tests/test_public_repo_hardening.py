from pathlib import Path


def test_readme_has_public_repo_hardening_requirements():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "https://api.beezshield.com/contracts/risk-score" in readme
    assert "BeezShield" in readme
    assert "Product/agent: `Sentinel Alpha`" in readme
    assert "Verified production payment proof" in readme
    assert "ERC-8004 planned / adapter stub" in readme
    assert "not yet registered" in readme
    assert "placeholders" in readme
    assert "python3 scripts/public_smoke_test.py" in readme
    assert "Never commit `.env`" in readme


def test_security_and_license_files_exist():
    assert Path("SECURITY.md").exists()
    assert Path("LICENSE").exists()


def test_no_known_secret_markers_in_public_docs():
    files = [
        Path("README.md"),
        Path("SECURITY.md"),
        Path("docs/15_release/PUBLIC_REPO_REVIEW.md"),
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
