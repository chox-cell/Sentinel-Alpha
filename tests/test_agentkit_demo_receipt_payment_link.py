import hashlib
import json
from pathlib import Path


ROOT = Path("examples/agentkit-sentinel-provider")
DEMO = ROOT / "src/demo.ts"
ACTION = ROOT / "src/sentinelRiskCheckAction.ts"
SAMPLE = ROOT / "examples/sample-output.json"
README = ROOT / "README.md"
DOC_PROTOTYPE = Path("docs/16_launch/SENTINEL_AGENTKIT_PROVIDER_PROTOTYPE.md")
DOC_RECEIPT = Path("docs/16_launch/SENTINEL_DECISION_RECEIPT.md")
DOC_TRUST = Path("docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md")


def test_demo_exists_and_includes_receipt_payment_link_fields():
    assert DEMO.exists()
    demo_text = DEMO.read_text(encoding="utf-8")
    action_text = ACTION.read_text(encoding="utf-8")
    combined = (demo_text + "\n" + action_text).lower()
    assert "sentinel_decision_ref" in combined
    assert "action_ref" in combined
    assert "payment_decision_link_ref" in combined
    assert "automatic_settlement_claimed" in combined
    assert "payment_protocol" in combined
    assert "payment_status" in combined


def test_sample_output_has_minimum_verifiable_loop_shape():
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))
    assert data["notSecurityGuarantee"] is True
    assert data["automatic_settlement_claimed"] is False
    assert data["payment_protocol"] == "x402"
    assert data["payment_status"] == "unknown"
    assert "sentinel_decision_ref" in data
    assert "action_ref" in data
    assert "payment_decision_link_ref" in data
    assert data["sampleOnly"] is True


def test_readme_and_docs_cover_boundaries():
    readme = README.read_text(encoding="utf-8").lower()
    assert "minimum verifiable loop output" in readme
    assert "no real x402 settlement is performed by this demo" in readme
    assert "no wallet execution/signing" in readme
    assert "not a security guarantee" in readme
    assert "local example only" in readme

    docs = "\n".join(
        [
            DOC_PROTOTYPE.read_text(encoding="utf-8"),
            DOC_RECEIPT.read_text(encoding="utf-8"),
            DOC_TRUST.read_text(encoding="utf-8"),
        ]
    ).lower()
    assert "decision receipt" in docs
    assert "payment decision link" in docs


def test_forbidden_positive_phrases_absent_with_negation_allowed():
    combined = "\n".join(
        [
            DEMO.read_text(encoding="utf-8"),
            ACTION.read_text(encoding="utf-8"),
            SAMPLE.read_text(encoding="utf-8"),
            README.read_text(encoding="utf-8"),
            DOC_PROTOTYPE.read_text(encoding="utf-8"),
            DOC_RECEIPT.read_text(encoding="utf-8"),
            DOC_TRUST.read_text(encoding="utf-8"),
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

    # allow negated wording only
    phrase = "automatic x402 settlement"
    start = 0
    while True:
        idx = combined.find(phrase, start)
        if idx == -1:
            break
        window = combined[max(0, idx - 40) : idx + len(phrase) + 40]
        assert ("no automatic x402 settlement" in window) or ("no real x402 settlement" in window)
        start = idx + 1


def test_env_unchanged_during_agentkit_demo_receipt_payment_link_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DEMO.read_text(encoding="utf-8")
    _ = SAMPLE.read_text(encoding="utf-8")
    _ = README.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
