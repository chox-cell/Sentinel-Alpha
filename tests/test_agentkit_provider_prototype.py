import hashlib
from pathlib import Path


ROOT = Path("examples/agentkit-sentinel-provider")
DOC = Path("docs/16_launch/SENTINEL_AGENTKIT_PROVIDER_PROTOTYPE.md")


def test_prototype_files_exist():
    required = [
        ROOT / "package.json",
        ROOT / "tsconfig.json",
        ROOT / "README.md",
        ROOT / "src/index.ts",
        ROOT / "src/sentinelRiskCheckAction.ts",
        ROOT / "src/types.ts",
        DOC,
    ]
    for file in required:
        assert file.exists(), f"missing {file}"


def test_readme_required_disclaimers():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    lower = text.lower()
    assert "prototype only" in lower
    assert "not an official coinbase agentkit provider" in lower
    assert "not submitted upstream" in lower
    assert "does not execute transactions" in lower
    assert "does not sign wallet actions" in lower
    assert "does not guarantee protection" in lower
    assert "does not claim honeypot detection" in lower


def test_source_action_shape_and_mapping():
    text = (ROOT / "src/sentinelRiskCheckAction.ts").read_text(encoding="utf-8")
    lower = text.lower()
    assert "@beezshield/sentinel" in text
    assert "contract_address" in text
    assert "allow" in lower and "review" in lower and "block" in lower
    assert "notsecurityguarantee" in lower


def test_docs_issue_url_and_forbidden_absence():
    all_text = "\n".join(
        [
            DOC.read_text(encoding="utf-8"),
            (ROOT / "README.md").read_text(encoding="utf-8"),
            (ROOT / "src/sentinelRiskCheckAction.ts").read_text(encoding="utf-8"),
        ]
    )
    lower = all_text.lower()
    assert "https://github.com/coinbase/agentkit/issues/1168" in all_text
    forbidden = [
        "official provider is live",
        "integration is live",
        "claims it detects honeypots",
        "claims it prevents mev",
        "guaranteed protection is provided",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in lower


def test_env_unchanged_during_prototype_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = (ROOT / "README.md").read_text(encoding="utf-8")
    _ = (ROOT / "src/sentinelRiskCheckAction.ts").read_text(encoding="utf-8")
    _ = DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
