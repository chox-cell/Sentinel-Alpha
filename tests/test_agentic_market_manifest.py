import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app


def test_agentic_market_manifest_required_values():
    manifest_path = Path("agentic-market.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["name"] == "Sentinel Alpha"
    assert manifest["category"] == "execution_fidelity_layer"
    assert manifest["endpoint"] == "/contracts/risk-score"
    assert manifest["pricing_tiers"] == {
        "basic": "0.02",
        "executive": "0.05",
        "premium": "0.10",
        "priority": "0.15",
    }
    assert manifest["payment"] == "x402"
    assert manifest["network"] == "eip155:8453"
    assert manifest["outputs"] == ["score", "confidence", "action", "emergency_signal", "attestation"]
    assert manifest["supported_chains"] == ["base"]
    assert manifest["modes"] == ["scan", "webhook", "dry_run"]
    assert manifest["identity"] == "did:sentinel-alpha:local"
    assert manifest["engine"] == "Mycelium Engine"
    assert manifest["agent_system"] == "Sentinel Cells"


def test_internal_manifest_values_align_with_agentic_market_manifest():
    agentic_manifest = json.loads(Path("agentic-market.json").read_text(encoding="utf-8"))

    client = TestClient(app)
    response = client.get("/internal/manifest")
    assert response.status_code == 200
    internal_manifest = response.json()

    assert internal_manifest["name"] == agentic_manifest["name"]
    assert internal_manifest["category"] == agentic_manifest["category"]
    assert internal_manifest["primary_endpoint"] == agentic_manifest["endpoint"]
    assert internal_manifest["payment_method"] == agentic_manifest["payment"]
    assert internal_manifest["network"] == agentic_manifest["network"]
    assert internal_manifest["outputs"] == agentic_manifest["outputs"]
    assert internal_manifest["supported_chains"] == agentic_manifest["supported_chains"]
    assert internal_manifest["modes"] == agentic_manifest["modes"]
    assert internal_manifest["identity"] == agentic_manifest["identity"]
    assert internal_manifest["engine"] == agentic_manifest["engine"]
    assert internal_manifest["agent_system"] == agentic_manifest["agent_system"]
    assert internal_manifest["pricing"] == agentic_manifest["pricing_tiers"]
