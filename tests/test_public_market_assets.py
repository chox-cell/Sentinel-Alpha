import json
from pathlib import Path


def test_public_market_json_assets_point_to_live_base_url():
    agentic = json.loads(Path("agentic-market.json").read_text(encoding="utf-8"))
    submission = json.loads(Path("marketplace-submission.json").read_text(encoding="utf-8"))
    identity = json.loads(Path("identity-manifest.json").read_text(encoding="utf-8"))

    assert agentic["public_base_url"] == "https://api.beezshield.com"
    assert submission["public_base_url"] == "https://api.beezshield.com"
    assert identity["public_base_url"] == "https://api.beezshield.com"
    assert identity["domain"] == "beezshield.com"


def test_identity_marked_erc8004_registered():
    submission = json.loads(Path("marketplace-submission.json").read_text(encoding="utf-8"))
    identity = json.loads(Path("identity-manifest.json").read_text(encoding="utf-8"))

    assert submission["identity_status"] == "erc8004_registered"
    assert identity["status"] == "erc8004_registered"


def test_public_market_docs_reference_live_endpoint():
    readme = Path("README.md").read_text(encoding="utf-8")
    submission_doc = Path("docs/14_distribution/AGENTIC_MARKET_SUBMISSION.md").read_text(encoding="utf-8")
    pitch_doc = Path("docs/14_distribution/BOT_BUILDER_PITCH.md").read_text(encoding="utf-8")

    assert "https://api.beezshield.com/contracts/risk-score" in readme
    assert "https://api.beezshield.com" in submission_doc
    assert "https://api.beezshield.com/contracts/risk-score" in pitch_doc
