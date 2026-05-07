import hashlib
import importlib.util
import json
from pathlib import Path


MODULE_PATH = Path("services/scanner_engine/decision_receipt.py")
SERVICE_PATH = Path("services/risk_service/service.py")
SAMPLE_OUTPUT = Path("examples/agentkit-sentinel-provider/examples/sample-output.json")
DOC_RECEIPT = Path("docs/16_launch/SENTINEL_DECISION_RECEIPT.md")
DOC_TRUST_LOOP = Path("docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md")
DOC_COMPOSABILITY = Path("docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_module_exists_and_builds_required_receipt_shape():
    assert MODULE_PATH.exists()
    module = _load_module(MODULE_PATH, "decision_receipt_module")
    builder = getattr(module, "build_decision_receipt", None)
    assert callable(builder)

    response = {
        "decision": {"action": "review", "confidence": 0.63},
        "risk_metrics": {"score": 56},
        "signals": {"proxy_detected": 1, "unknown_account_kind": 0},
        "meta": {"security_explanation": {"summary": "local-only"}},
        "attestation": {"signed_at": "2026-05-07T12:00:00Z"},
    }
    request_context = {
        "contract_address": "0x1111111111111111111111111111111111111111",
        "chain": "base",
        "requested_action": "swap",
        "intent": {"kind": "trade", "side": "buy"},
        "policy_version": "sentinel-policy-v0",
        "trace_id": "trace-local-1",
    }
    receipt = builder(response, request_context=request_context, config={"receipt_version": "v1"})

    assert receipt["receipt_version"] == "v1"
    assert isinstance(receipt["sentinel_decision_ref"], str) and len(receipt["sentinel_decision_ref"]) == 64
    assert isinstance(receipt["action_ref"], str) and len(receipt["action_ref"]) == 64
    assert isinstance(receipt["contract_address_hash"], str) and len(receipt["contract_address_hash"]) == 64
    assert "contract_address" not in receipt
    assert receipt["notSecurityGuarantee"] is True
    assert receipt["persistence_status"] == "not_persisted"
    assert receipt["external_integration_status"] == "not_integrated"


def test_service_wires_decision_receipt_metadata():
    text = SERVICE_PATH.read_text(encoding="utf-8")
    assert "\"decision_receipt\": build_decision_receipt(" in text
    assert "\"meta\": {" in text


def test_sample_output_and_docs_include_required_references_and_boundaries():
    sample = json.loads(SAMPLE_OUTPUT.read_text(encoding="utf-8"))
    assert "sentinel_decision_ref" in sample
    assert "action_ref" in sample

    receipt_doc = DOC_RECEIPT.read_text(encoding="utf-8").lower()
    assert "sentinel_decision_ref" in receipt_doc
    assert "action_ref" in receipt_doc
    assert "not persisted by default" in receipt_doc
    assert "not a security guarantee" in receipt_doc

    trust_loop_doc = DOC_TRUST_LOOP.read_text(encoding="utf-8").lower()
    composability_doc = DOC_COMPOSABILITY.read_text(encoding="utf-8").lower()
    assert "sentinel decision receipt" in trust_loop_doc
    assert "decision receipt boundary" in composability_doc


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            MODULE_PATH.read_text(encoding="utf-8"),
            SERVICE_PATH.read_text(encoding="utf-8"),
            SAMPLE_OUTPUT.read_text(encoding="utf-8"),
            DOC_RECEIPT.read_text(encoding="utf-8"),
            DOC_TRUST_LOOP.read_text(encoding="utf-8"),
            DOC_COMPOSABILITY.read_text(encoding="utf-8"),
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


def test_env_unchanged_during_decision_receipt_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = MODULE_PATH.read_text(encoding="utf-8")
    _ = DOC_RECEIPT.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
