import json
from pathlib import Path


def test_identity_manifest_erc8004_registered():
    identity_manifest = json.loads(Path("identity-manifest.json").read_text(encoding="utf-8"))
    assert identity_manifest["status"] == "erc8004_registered"
    assert identity_manifest["agent_id"] == "45967"


def test_market_json_files_include_8004scan_url():
    expected_url = "https://8004scan.io/agents/base/45967"

    marketplace_submission = json.loads(Path("marketplace-submission.json").read_text(encoding="utf-8"))
    agentic_market = json.loads(Path("agentic-market.json").read_text(encoding="utf-8"))
    identity_manifest = json.loads(Path("identity-manifest.json").read_text(encoding="utf-8"))

    assert marketplace_submission["erc8004_url"] == expected_url
    assert agentic_market["erc8004_url"] == expected_url
    assert identity_manifest["registry_url"] == expected_url


def test_readme_includes_registration_proof_and_no_fake_protocol_claims():
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "45967" in readme
    assert "https://8004scan.io/agents/base/45967" in readme

    lowered = readme.lower()
    assert "mcp support" not in lowered
    assert "a2a support" not in lowered
    assert "supports mcp" not in lowered
    assert "supports a2a" not in lowered
