import json
from pathlib import Path


def test_manifest_file_has_required_hardened_fields():
    manifest_path = Path("docs/01_manifest/manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["name"] == "Sentinel Alpha"
    assert manifest["category"] == "execution_fidelity_layer"
    assert manifest["engine"] == "Mycelium Engine"
    assert manifest["agent_system"] == "Sentinel Cells"
    assert manifest["primary_endpoint"] == "/contracts/risk-score"
    assert manifest["webhook_endpoint"] == "/webhooks/quicknode"
    assert manifest["health_endpoint"] == "/health"
    assert manifest["quicknode_health_endpoint"] == "/webhooks/quicknode/health"
    assert manifest["payment_method"] == "x402"
    assert manifest["network"] == "eip155:8453"
    assert manifest["payment_mode"] == "demo"
    assert manifest["identity"] == "did:sentinel-alpha:local"
    assert manifest["api_version"] == "2026.8.0"
    assert manifest["engine_version"] == "mycelium-wrsi-0.2"
    assert manifest["identity_version"] == "identity-0.1"
    assert manifest["attestation_version"] == "attestation-0.1"
    assert manifest["supported_chains"] == ["base"]
    assert manifest["outputs"] == ["score", "confidence", "action", "emergency_signal", "attestation"]
    assert manifest["actions"] == ["BLOCK", "REDUCE", "ALLOW", "REVIEW", "EXIT_NOW"]
    assert manifest["modes"] == ["scan", "webhook", "dry_run"]
    assert manifest["pricing"] == {"basic": "0.02", "executive": "0.05", "premium": "0.10", "priority": "0.15"}
    assert manifest["constraints"] == {
        "first_60_minutes_security": True,
        "no_dashboard": True,
        "no_compliance_suite": True,
        "machine_native": True,
    }
