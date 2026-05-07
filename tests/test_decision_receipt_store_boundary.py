import hashlib
import importlib.util
from pathlib import Path


STORE_MODULE_PATH = Path("services/scanner_engine/decision_receipt_store.py")
SERVICE_PATH = Path("services/risk_service/service.py")
DOC_RECEIPT = Path("docs/16_launch/SENTINEL_DECISION_RECEIPT.md")
DOC_DB_PLAN = Path("docs/16_launch/SENTINEL_LOCAL_RISK_HISTORY_DB_PLAN.md")


def _load_module(path: Path, name: str):
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
        "requested_action": "swap",
        "intent_hash": "d" * 64,
        "decision_action": "review",
        "confidence": 0.61,
        "risk_score": 55,
        "signals_summary": {"total": 1, "active_count": 1, "active_signals": ["proxy_detected"]},
        "explanation_hash": "e" * 64,
        "policy_version": "sentinel-policy-v0",
        "created_at": "2026-05-07T12:45:00Z",
        "notSecurityGuarantee": True,
        "contract_address": "0x1111111111111111111111111111111111111111",
        "private_key": "forbidden",
        "seed_phrase": "forbidden",
        "authorization": "forbidden",
        "api_key": "forbidden",
        "headers": {"x-auth": "forbidden"},
        "cookies": "forbidden",
        "payment_signature": "forbidden",
        "wallet_private_key": "forbidden",
        "raw_prompt": "forbidden",
        "raw_intent_text": "forbidden",
    }


def test_module_exists_and_default_status_is_disabled():
    assert STORE_MODULE_PATH.exists()
    module = _load_module(STORE_MODULE_PATH, "decision_receipt_store_module")
    status = module.get_decision_receipt_store_status()
    assert status["store_enabled"] is False
    assert status["store_mode"] in {"disabled", "not_configured"}
    assert status["database_required"] is False
    assert status["redis_required"] is False
    assert status["filesystem_required"] is False
    assert status["write_attempted"] is False
    assert status["write_status"] == "not_run"
    assert status["persistence_status"] == "not_persisted"


def test_sanitizer_removes_raw_contract_and_secret_markers():
    module = _load_module(STORE_MODULE_PATH, "decision_receipt_store_sanitizer_module")
    sanitized = module.sanitize_decision_receipt_for_storage(_sample_receipt())

    assert sanitized["receipt_version"] == "v1"
    assert sanitized["notSecurityGuarantee"] is True
    assert "contract_address" not in sanitized
    for forbidden in [
        "private_key",
        "seed_phrase",
        "authorization",
        "api_key",
        "headers",
        "cookies",
        "payment_signature",
        "wallet_private_key",
        "raw_prompt",
        "raw_intent_text",
    ]:
        assert forbidden not in sanitized


def test_build_store_record_and_default_persist_no_write():
    module = _load_module(STORE_MODULE_PATH, "decision_receipt_store_record_module")
    record = module.build_decision_receipt_store_record(
        _sample_receipt(),
        request_meta={"request_id": "req-1", "client_id": "client-A", "source": "unit-test"},
    )
    assert record["record_version"] == "v1"
    assert record["record_type"] == "sentinel_decision_receipt"
    assert "contract_address" not in record["receipt"]
    assert record["receipt"]["notSecurityGuarantee"] is True
    assert "client_id_hash" in record["request_meta"]

    persist_result = module.persist_decision_receipt(record)
    assert persist_result["write_attempted"] is False
    assert persist_result["write_status"] == "not_run"
    assert persist_result["persistence_status"] == "not_persisted"
    assert persist_result["error_type"] is None


def test_persist_writes_only_with_explicit_in_memory_test_backend():
    module = _load_module(STORE_MODULE_PATH, "decision_receipt_store_persist_module")
    record = module.build_decision_receipt_store_record(_sample_receipt(), request_meta={"request_id": "req-2"})

    list_backend = []
    out_list = module.persist_decision_receipt(record, store_backend=list_backend)
    assert out_list["write_attempted"] is True
    assert out_list["write_status"] == "written_to_test_backend"
    assert out_list["persistence_status"] == "stored_in_test_backend"
    assert out_list["test_only"] is True
    assert len(list_backend) == 1

    dict_backend = {}
    out_dict = module.persist_decision_receipt(record, store_backend=dict_backend)
    assert out_dict["write_attempted"] is True
    assert out_dict["write_status"] == "written_to_test_backend"
    assert out_dict["persistence_status"] == "stored_in_test_backend"
    assert out_dict["test_only"] is True
    assert len(dict_backend) == 1


def test_service_and_docs_include_store_boundary_language():
    service_text = SERVICE_PATH.read_text(encoding="utf-8")
    assert "\"decision_receipt_store\": get_decision_receipt_store_status()" in service_text

    receipt_doc = DOC_RECEIPT.read_text(encoding="utf-8").lower()
    db_plan_doc = DOC_DB_PLAN.read_text(encoding="utf-8").lower()
    assert "not persisted by default" in receipt_doc
    assert "no raw contract addresses" in receipt_doc
    assert "no raw secrets" in receipt_doc
    assert "v9.1" in db_plan_doc
    assert "runtime db writes are still disabled" in db_plan_doc


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            STORE_MODULE_PATH.read_text(encoding="utf-8"),
            DOC_RECEIPT.read_text(encoding="utf-8"),
            DOC_DB_PLAN.read_text(encoding="utf-8"),
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


def test_env_unchanged_during_store_boundary_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = STORE_MODULE_PATH.read_text(encoding="utf-8")
    _ = DOC_RECEIPT.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
