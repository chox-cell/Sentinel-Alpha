import hashlib
from pathlib import Path


LANDING = Path("docs/17_growth/AGENTKIT_SENTINEL_MINI_LANDING.md")
README = Path("examples/agentkit-sentinel-provider/README.md")


def test_mini_landing_exists_and_required_content():
    assert LANDING.exists()
    text = LANDING.read_text(encoding="utf-8")
    lower = text.lower()
    assert "Sentinel Alpha for AgentKit — Prototype" in text
    assert "allow/review/block" in lower
    assert "@beezshield/sentinel" in text
    assert "npm run demo" in text
    assert "sample-output.json" in text
    assert "https://github.com/coinbase/agentkit/issues/1168" in text
    assert "not an official Coinbase AgentKit provider" in text
    assert "no wallet execution" in lower
    assert "no transaction signing" in lower
    assert "not a security guarantee" in lower


def test_readme_references_mini_landing_doc():
    text = README.read_text(encoding="utf-8")
    assert "AGENTKIT_SENTINEL_MINI_LANDING.md" in text


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            LANDING.read_text(encoding="utf-8").lower(),
            README.read_text(encoding="utf-8").lower(),
        ]
    )
    forbidden = [
        "official provider is live",
        "integration is live",
        "claims it detects honeypots",
        "claims it prevents mev",
        "guaranteed protection is provided",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in combined


def test_env_unchanged_during_mini_landing_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = LANDING.read_text(encoding="utf-8")
    _ = README.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
