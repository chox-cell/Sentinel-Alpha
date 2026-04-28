import json
from pathlib import Path


def test_mit_license_exists_and_not_placeholder():
    text = Path("LICENSE").read_text(encoding="utf-8")
    assert "MIT License" in text
    assert "Copyright (c) 2026 Amine Khodja" in text
    assert "LICENSE PLACEHOLDER" not in text
    assert "placeholder license file" not in text.lower()


def test_marketplace_submission_final_fields():
    data = json.loads(Path("marketplace-submission.json").read_text(encoding="utf-8"))
    assert data["name"] == "Sentinel Alpha"
    assert data["tagline"] == "Execution Fidelity Layer for Bots and Agents"
    assert data["category"] == "execution_fidelity_layer"
    assert data["public_base_url"] == "https://api.beezshield.com"
    assert data["endpoint"] == "/contracts/risk-score"
    assert data["payment_method"] == "x402"
    assert data["network"] == "eip155:8453"
    assert data["pricing_tiers"] == {
        "basic": "0.02",
        "executive": "0.05",
        "premium": "0.10",
        "priority": "0.15",
    }
    assert data["treasury_wallet"] == "0x3cf9C2E55485fF8DAFfb59c84a0fa7c03bDbAeaf"
    assert data["github"] == "https://github.com/chox-cell/Sentinel-Alpha"
    assert data["release_tag"] == "v1.5.0"
    assert data["identity_status"] == "erc8004_registered"
    assert data["erc8004_agent_id"] == "45967"
    assert data["erc8004_url"] == "https://8004scan.io/agents/base/45967"
    assert data["real_payment_verified"] is True
    assert data["supported_chains"] == ["base"]
    assert data["outputs"] == ["score", "confidence", "action", "emergency_signal", "attestation"]
    assert data["sdk"] == {
        "python": "sdk/python/README.md",
        "typescript": "sdk/typescript/README.md",
    }


def test_readme_marketplace_discovery_and_no_fake_claims():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "Marketplace / Discovery" in readme
    assert "Agentic Market submission-ready" in readme
    assert "ERC-8004 registered" in readme
    assert "https://8004scan.io/agents/base/45967" in readme
    assert "https://api.beezshield.com/contracts/risk-score" in readme
    assert "x402 enabled" in readme
    assert "basic 0.02" in readme
    assert "executive 0.05" in readme
    assert "premium 0.10" in readme
    assert "priority 0.15" in readme

    lowered = readme.lower()
    assert "mcp support" not in lowered
    assert "a2a support" not in lowered
    assert "supports mcp" not in lowered
    assert "supports a2a" not in lowered
