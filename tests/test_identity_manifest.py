import json
from pathlib import Path


def test_identity_manifest_exists_and_required_fields():
    path = Path("identity-manifest.json")
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["project"] == "Sentinel Alpha"
    assert data["engine"] == "Mycelium Engine"
    assert data["agent_system"] == "Sentinel Cells"
    assert data["current_identity"] == "did:sentinel-alpha:local"
    assert data["target_identity"] == "erc8004"
    assert data["status"] == "erc8004_registered"
    assert data["agent_id"] == "45967"
    assert data["registry"] == "8004scan"
    assert data["registry_url"] == "https://8004scan.io/agents/base/45967"
    assert data["network"] == "base"
    assert data["chain_id"] == 8453
    assert data["endpoint"] == "/contracts/risk-score"
    assert data["wallet"] == "0x3cf9C2E55485fF8DAFfb59c84a0fa7c03bDbAeaf"
    assert data["attestation_version"] == "attestation-0.1"
    assert data["release_target"] == "v1.8"


def test_marketplace_submission_identity_status_unchanged():
    submission = json.loads(Path("marketplace-submission.json").read_text(encoding="utf-8"))
    assert submission["identity_status"] == "erc8004_registered"
