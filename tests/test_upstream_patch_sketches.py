import hashlib
from pathlib import Path


FILES = [
    Path("docs/17_growth/upstream_patch_sketches/x402/README.md"),
    Path("docs/17_growth/upstream_patch_sketches/x402/sentinel-risk-decision-example.md"),
    Path("docs/17_growth/upstream_patch_sketches/agentkit/README.md"),
    Path("docs/17_growth/upstream_patch_sketches/agentkit/sentinel-risk-check-action.ts"),
    Path("docs/17_growth/upstream_patch_sketches/eliza/README.md"),
    Path("docs/17_growth/upstream_patch_sketches/eliza/sentinel-risk-check-action.ts"),
]


def test_all_patch_sketch_files_exist():
    for file in FILES:
        assert file.exists(), f"missing {file}"


def test_issue_urls_present():
    text = "\n".join(path.read_text(encoding="utf-8") for path in FILES if path.suffix in {".md", ".ts"})
    assert "https://github.com/x402-foundation/x402/issues/2198" in text
    assert "https://github.com/coinbase/agentkit/issues/1168" in text
    assert "https://github.com/elizaOS/eliza/issues/7396" in text


def test_typescript_sketches_have_required_tokens():
    agentkit = Path("docs/17_growth/upstream_patch_sketches/agentkit/sentinel-risk-check-action.ts").read_text(encoding="utf-8")
    eliza = Path("docs/17_growth/upstream_patch_sketches/eliza/sentinel-risk-check-action.ts").read_text(encoding="utf-8")
    for text in (agentkit, eliza):
        lower = text.lower()
        assert "@beezshield/sentinel" in text
        assert "contract_address" in text
        assert "allow" in lower and "review" in lower and "block" in lower
        assert "not submitted upstream" in lower
        assert "not a security guarantee" in lower


def test_forbidden_phrases_absent():
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in FILES)
    forbidden = [
        "claims it detects honeypots",
        "claims it prevents mev",
        "guaranteed protection is provided",
        "live simulation is enabled",
        "integration is live",
        "provider is live",
    ]
    for token in forbidden:
        assert token not in text


def test_env_unchanged_during_patch_sketch_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    for file in FILES:
        _ = file.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
