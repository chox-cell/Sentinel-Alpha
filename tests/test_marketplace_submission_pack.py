import json
from pathlib import Path


def test_marketplace_submission_json_required_fields():
    path = Path("marketplace-submission.json")
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["name"] == "Sentinel Alpha"
    assert data["tagline"] == "Execution Fidelity Layer for Bots and Agents"
    assert data["category"] == "execution_fidelity_layer"
    assert data["endpoint"] == "/contracts/risk-score"
    assert data["payment_method"] == "x402"
    assert data["network"] == "eip155:8453"
    assert data["treasury_wallet"] == "0x3cf9C2E55485fF8DAFfb59c84a0fa7c03bDbAeaf"
    assert data["pricing_tiers"] == {
        "basic": "0.02",
        "executive": "0.05",
        "premium": "0.10",
        "priority": "0.15",
    }
    assert data["supported_chains"] == ["base"]
    assert data["outputs"] == ["score", "confidence", "action", "emergency_signal", "attestation"]
    assert data["sdk"] == {
        "python": "sdk/python/README.md",
        "typescript": "sdk/typescript/README.md",
    }
    assert data["github"] == "https://github.com/chox-cell/Sentinel-Alpha"
    assert data["release_tag"] == "v1.5.0"
    assert data["public_base_url_required"] is True
    assert data["identity_status"] == "local_did_pending_erc8004"
    assert data["real_payment_verified"] is True


def test_marketplace_submission_docs_exist_and_include_required_claims():
    docs = [
        Path("docs/14_distribution/AGENTIC_MARKET_SUBMISSION.md"),
        Path("docs/14_distribution/BOT_BUILDER_PITCH.md"),
        Path("docs/14_distribution/LAUNCH_POST.md"),
    ]
    for doc in docs:
        assert doc.exists()
        text = doc.read_text(encoding="utf-8")
        assert "Real Base USDC payment verified" in text
        assert "Replay protection active" in text
        assert "Settlement ledger active" in text
        assert "ERC-8004 real identity pending" in text
        assert "No dashboard required" in text
