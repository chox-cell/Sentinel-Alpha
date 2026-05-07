import hashlib
import importlib.util
import json
from pathlib import Path


MODULE = Path("services/scanner_engine/payment_decision_link.py")
SERVICE = Path("services/risk_service/service.py")
SAMPLE = Path("examples/agentkit-sentinel-provider/examples/sample-output.json")
DOC_RECEIPT = Path("docs/16_launch/SENTINEL_DECISION_RECEIPT.md")
DOC_TRUST_LOOP = Path("docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md")
DOC_COMPOSABILITY = Path("docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md")
CLAIMS_LEDGER = Path("docs/18_investor/CLAIMS_LEDGER.md")


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sample_receipt():
    return {
        "receipt_version": "v1",
        "decision_id": "abc123",
        "sentinel_decision_ref": "a" * 64,
        "action_ref": "b" * 64,
        "chain": "base",
        "contract_address_hash": "c" * 64,
        "decision_action": "review",
        "created_at": "2026-05-07T15:00:00Z",
    }


def test_module_exists_and_default_status():
    assert MODULE.exists()
    mod = _load(MODULE, "payment_decision_link_module")
    status = mod.get_payment_decision_link_status()
    assert status["link_enabled"] is False
    assert status["link_mode"] in {"disabled", "not_configured"}
    assert status["x402_settlement_required"] is False
    assert status["wallet_required"] is False
    assert status["private_key_required"] is False
    assert status["external_integration_status"] == "not_integrated"


def test_build_link_and_preserve_decision_refs():
    mod = _load(MODULE, "payment_decision_link_build_module")
    link = mod.build_payment_decision_link(
        _sample_receipt(),
        payment_context={
            "payment_request_id": "req-1",
            "payment_hash": "p" * 64,
            "payment_protocol": "x402",
            "payment_status": "authorized",
            "payer_id": "payer-a",
            "facilitator_id": "fac-1",
        },
    )
    assert isinstance(link["payment_decision_link_ref"], str) and len(link["payment_decision_link_ref"]) == 64
    assert link["sentinel_decision_ref"] == "a" * 64
    assert link["action_ref"] == "b" * 64
    assert link["automatic_settlement_claimed"] is False
    assert link["external_integration_status"] == "not_integrated"
    assert link["persistence_status"] == "not_persisted"


def test_missing_payment_context_is_supported():
    mod = _load(MODULE, "payment_decision_link_missing_context_module")
    link = mod.build_payment_decision_link(_sample_receipt())
    assert link["payment_status"] == "unknown"
    assert link["payment_protocol"] == "unknown"
    assert link["payment_hash"] is None
    assert isinstance(link["payment_decision_link_ref"], str) and len(link["payment_decision_link_ref"]) == 64


def test_sanitizer_removes_forbidden_and_hashes_ids():
    mod = _load(MODULE, "payment_decision_link_sanitize_module")
    sanitized = mod.sanitize_payment_context(
        {
            "payment_request_id": "req-2",
            "payment_hash": "h" * 64,
            "payment_protocol": "x402",
            "payment_status": "required",
            "payer_id": "payer-secret",
            "facilitator_id": "facilitator-secret",
            "authorization": "x",
            "headers": {"auth": "x"},
            "cookies": "x",
            "api_key": "x",
            "private_key": "x",
            "seed_phrase": "x",
            "payment_signature": "x",
            "wallet_private_key": "x",
            "raw_payment_header": "x",
            "raw_x402_payload": "x",
            "bearer_token": "x",
        }
    )
    assert sanitized["payer_id_hash"] and len(sanitized["payer_id_hash"]) == 64
    assert sanitized["facilitator_id_hash"] and len(sanitized["facilitator_id_hash"]) == 64
    for bad_key in [
        "authorization",
        "headers",
        "cookies",
        "api_key",
        "private_key",
        "seed_phrase",
        "payment_signature",
        "wallet_private_key",
        "raw_payment_header",
        "raw_x402_payload",
        "bearer_token",
        "payer_id",
        "facilitator_id",
    ]:
        assert bad_key not in sanitized


def test_sample_docs_and_service_alignment():
    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    assert "payment_decision_link_ref" in sample
    assert sample["automatic_settlement_claimed"] is False

    service_text = SERVICE.read_text(encoding="utf-8")
    assert "\"payment_decision_link_status\"" in service_text

    text = DOC_RECEIPT.read_text(encoding="utf-8").lower()
    assert "no automatic x402 settlement claim" in text
    assert "not persisted by default" in text
    assert "no official x402 integration claim" in text
    assert "payment_decision_link_ref" in text
    assert "payment_request_id" in text
    assert "payment_hash" in text

    assert "payment_decision_link_ref" in DOC_TRUST_LOOP.read_text(encoding="utf-8")
    assert "payment_decision_link_ref" in DOC_COMPOSABILITY.read_text(encoding="utf-8")
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "payment_decision_link_ref boundary exists locally" in ledger
    assert "do not claim that payment-decision link metadata performs settlement execution" in ledger


def test_forbidden_phrases_absent_with_negation_exception():
    combined = "\n".join(
        [
            MODULE.read_text(encoding="utf-8"),
            SERVICE.read_text(encoding="utf-8"),
            SAMPLE.read_text(encoding="utf-8"),
            DOC_RECEIPT.read_text(encoding="utf-8"),
            DOC_TRUST_LOOP.read_text(encoding="utf-8"),
            DOC_COMPOSABILITY.read_text(encoding="utf-8"),
        ]
    ).lower()

    # Allowed only in explicit negation statements.
    for phrase in ["automatic x402 settlement"]:
        positions = []
        start = 0
        while True:
            idx = combined.find(phrase, start)
            if idx == -1:
                break
            positions.append(idx)
            start = idx + 1
        for idx in positions:
            window = combined[max(0, idx - 24) : idx + len(phrase) + 24]
            assert ("no automatic x402 settlement" in window) or ("does not perform automatic x402 settlement" in window)

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


def test_env_unchanged_during_payment_link_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = MODULE.read_text(encoding="utf-8")
    _ = DOC_RECEIPT.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
