import json
from pathlib import Path


def _sentinel_pkg():
    p = Path("packages/sentinel-sdk/package.json")
    assert p.is_file(), "packages/sentinel-sdk/package.json missing"
    return json.loads(p.read_text(encoding="utf-8"))


def test_sentinel_sdk_package_name_and_entry():
    data = _sentinel_pkg()
    assert data["name"] == "@beezshield/sentinel"
    scripts = data.get("scripts") or {}
    assert "vitest" in scripts.get("test", "").lower()
    exports = data.get("exports", {})
    assert "." in exports
    assert exports["."]["default"].endswith("dist/index.js")


def test_sentinel_sdk_readme_product_truth():
    text = Path("packages/sentinel-sdk/README.md").read_text(encoding="utf-8")
    assert "publish" in text.lower()
    assert "@beezshield/sentinel" in text
    assert "AgentKit" in text or "agentkit" in text.lower()
    assert "automatic" in text.lower() and "x402" in text.lower()
    assert "BASE_RPC" not in text
    assert "PRIVATE_KEY" not in text


def test_sentinel_sdk_sources_export_required_api():
    idx = Path("packages/sentinel-sdk/src/index.ts").read_text(encoding="utf-8")
    for needle in (
        "createSentinelClient",
        "scoreContract",
        "decideBeforeExecution",
        "isX402Challenge",
        "normalizeSentinelDecision",
        "SentinelClientConfig",
        "SentinelRiskResponse",
        "SentinelDecision",
        "X402Challenge",
    ):
        assert needle in idx
