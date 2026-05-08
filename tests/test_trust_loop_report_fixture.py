import hashlib
import json
from pathlib import Path


JSON_FIXTURE = Path("reports/trust_loop/minimum_verifiable_loop.sample.json")
MD_FIXTURE = Path("reports/trust_loop/minimum_verifiable_loop.sample.md")
OUTREACH_TRACKER = Path("docs/17_growth/OUTREACH_TRACKER.md")
TRUST_LOOP_DOC = Path("docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md")
COMPOSABILITY_DOC = Path("docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md")
RECEIPT_DOC = Path("docs/16_launch/SENTINEL_DECISION_RECEIPT.md")


def test_json_fixture_exists_and_has_required_shape():
    assert JSON_FIXTURE.exists()
    data = json.loads(JSON_FIXTURE.read_text(encoding="utf-8"))
    assert data["report_type"] == "minimum_verifiable_trust_loop"
    assert data["sampleOnly"] is True
    assert data["documentationOnly"] is True
    assert data["notSecurityGuarantee"] is True
    assert data["partnership_claimed"] is False
    assert data["integration_claimed"] is False
    assert data["official_endorsement_claimed"] is False

    flow = data["flow"]
    for key in ["tool_preflight", "sentinel_precheck", "payment_authorization", "execution", "post_action_trail"]:
        assert key in flow

    assert "sentinel_decision_ref" in flow["sentinel_precheck"]
    assert "action_ref" in flow["sentinel_precheck"]
    assert "payment_decision_link_ref" in flow["payment_authorization"]
    assert ("trace_id" in flow["tool_preflight"]) or ("receipt_id" in flow["tool_preflight"])
    assert flow["post_action_trail"]["anchors"]["arbitrum"]["chain_id"] == 42161
    assert flow["post_action_trail"]["anchors"]["base"]["chain_id"] == 8453
    assert flow["payment_authorization"]["automatic_settlement_claimed"] is False
    assert flow["execution"]["wallet_execution"] is False
    assert flow["execution"]["transaction_signed"] is False


def test_markdown_fixture_exists_and_includes_required_statements():
    assert MD_FIXTURE.exists()
    text = MD_FIXTURE.read_text(encoding="utf-8").lower()
    assert "sample only" in text
    assert "no live calls" in text
    assert "no wallet execution/signing" in text
    assert "no db writes" in text
    assert "no official integration/partnership claim" in text
    assert "agent_trust_loop_reference.md" in text
    assert "action_ref" in text
    assert "sentinel_decision_ref" in text
    assert "payment_decision_link_ref" in text
    assert "payment_hash" in text
    assert "trace_id" in text and "receipt_id" in text


def test_outreach_tracker_records_verification_offer():
    text = OUTREACH_TRACKER.read_text(encoding="utf-8").lower()
    assert "review_feedback_and_verification_offer" in text
    assert "reviewer: giskard09" in text
    assert "verification_offer: willing to verify mycelium-side fields against the live verify endpoint shape once fixture exists" in text
    assert "documentation-only community collaboration signal" in text


def test_forbidden_positive_phrases_absent_with_negation_allowed():
    combined = "\n".join(
        [
            JSON_FIXTURE.read_text(encoding="utf-8"),
            MD_FIXTURE.read_text(encoding="utf-8"),
            TRUST_LOOP_DOC.read_text(encoding="utf-8"),
            COMPOSABILITY_DOC.read_text(encoding="utf-8"),
            RECEIPT_DOC.read_text(encoding="utf-8"),
            OUTREACH_TRACKER.read_text(encoding="utf-8"),
        ]
    ).lower()

    forbidden = [
        "integration is live and active",
        "partnership live",
        "guaranteed protection is provided",
        "claims it detects honeypots",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in combined

    phrase = "automatic x402 settlement"
    start = 0
    while True:
        idx = combined.find(phrase, start)
        if idx == -1:
            break
        window = combined[max(0, idx - 40) : idx + len(phrase) + 40]
        assert ("no automatic x402 settlement" in window) or ("does not perform automatic x402 settlement" in window)
        start = idx + 1


def test_env_unchanged_during_trust_loop_fixture_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = JSON_FIXTURE.read_text(encoding="utf-8")
    _ = MD_FIXTURE.read_text(encoding="utf-8")
    _ = OUTREACH_TRACKER.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
