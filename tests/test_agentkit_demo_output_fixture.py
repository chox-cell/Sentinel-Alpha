import hashlib
import json
from pathlib import Path


ROOT = Path("examples/agentkit-sentinel-provider")
SAMPLE = ROOT / "examples/sample-output.json"
README = ROOT / "README.md"


def test_sample_output_exists_and_parses():
    assert SAMPLE.exists()
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))
    assert data["sampleOnly"] is True
    assert data["notSecurityGuarantee"] is True
    assert data["action"] in {"allow", "review", "block"}
    assert data["contract_address"] == "0x1111111111111111111111111111111111111111"


def test_readme_mentions_sample_output_and_disclaimers():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "sample output fixture" in lower
    assert "illustrative only" in lower
    assert "not live scan proof" in lower
    assert "not a security guarantee" in lower


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            SAMPLE.read_text(encoding="utf-8"),
            README.read_text(encoding="utf-8"),
        ]
    ).lower()
    forbidden = [
        "official provider is live",
        "integration is live",
        "detects honeypots",
        "prevents mev",
        "guaranteed protection",
        "live simulation",
    ]
    for token in forbidden:
        assert token not in combined


def test_env_unchanged_during_output_fixture_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = SAMPLE.read_text(encoding="utf-8")
    _ = README.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
