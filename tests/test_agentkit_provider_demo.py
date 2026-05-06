import hashlib
import json
from pathlib import Path


ROOT = Path("examples/agentkit-sentinel-provider")
DEMO = ROOT / "src/demo.ts"
README = ROOT / "README.md"
PKG = ROOT / "package.json"


def test_demo_file_exists_and_uses_action():
    assert DEMO.exists()
    text = DEMO.read_text(encoding="utf-8")
    assert "sentinelRiskCheckAction" in text
    assert "contract_address" in text
    lower = text.lower()
    forbidden = ["private_key", "seed phrase", "cdp", "ethers", "viem", "walletconnect"]
    for token in forbidden:
        assert token not in lower


def test_package_json_has_demo_script():
    data = json.loads(PKG.read_text(encoding="utf-8"))
    assert data.get("private") is True
    scripts = data.get("scripts", {})
    assert "demo" in scripts


def test_readme_mentions_demo_and_safety_disclaimers():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "run local demo" in lower
    assert "npm run demo" in text
    assert "not an official coinbase agentkit provider" in lower
    assert "not a security guarantee" in lower
    assert "no wallet action is executed" in lower
    assert "no transaction is signed" in lower


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            DEMO.read_text(encoding="utf-8"),
            README.read_text(encoding="utf-8"),
            PKG.read_text(encoding="utf-8"),
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


def test_env_unchanged_during_demo_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DEMO.read_text(encoding="utf-8")
    _ = README.read_text(encoding="utf-8")
    _ = PKG.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
