import hashlib
from pathlib import Path

from services.scanner_engine.abi_source_cache import (
    build_abi_source_cache_key,
    get_abi_source_cache_status,
    read_abi_source_cache,
    sanitize_abi_source_cache_payload,
    write_abi_source_cache,
)


STRATEGY_DOC = Path("docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md")
DB_PLAN_DOC = Path("docs/16_launch/SENTINEL_LOCAL_RISK_HISTORY_DB_PLAN.md")
MODULE_PATH = Path("services/scanner_engine/abi_source_cache.py")


def test_default_cache_disabled_and_urls_not_required():
    status = get_abi_source_cache_status()
    assert status["cache_enabled"] is False
    assert status["cache_mode"] in {"disabled", "not_configured"}
    assert status["redis_required"] is False
    assert status["database_required"] is False
    notes = " ".join(status["notes"]).lower()
    assert "redis_url is not required" in notes
    assert "database_url is not required" in notes


def test_cache_key_is_deterministic_and_safe():
    k1 = build_abi_source_cache_key("0xABC", "Base", "Sourcify")
    k2 = build_abi_source_cache_key("0xabc", "base", "sourcify")
    assert k1 == k2
    assert "api_key" not in k1
    assert "authorization" not in k1
    assert "payment_signature" not in k1


def test_in_memory_backend_write_and_read_only_when_explicit():
    backend = {}
    payload = {
        "verified_source_status": "verified",
        "abi_available": True,
        "abi_function_names": ["transfer"],
        "abi_selector_count": 1,
        "provider_name": "local_fixture",
        "ttl_seconds": 300,
        "source_fetch_error_type": None,
    }
    out_w = write_abi_source_cache("0x1111", "base", "local_fixture", payload, cache_backend=backend)
    assert out_w["write_attempted"] is True
    assert out_w["write_status"] == "ok"
    out_r = read_abi_source_cache("0x1111", "base", "local_fixture", cache_backend=backend)
    assert out_r["read_attempted"] is True
    assert out_r["cache_hit"] is True
    assert out_r["value"]["provider_name"] == "local_fixture"


def test_payload_sanitizer_excludes_secrets_headers_and_signatures():
    payload = {
        "verified_source_status": "verified",
        "abi_available": True,
        "abi_function_names": ["transfer"],
        "abi_selector_count": 1,
        "provider_name": "local_fixture",
        "fetched_at": "2026-05-05T00:00:00Z",
        "ttl_seconds": 300,
        "source_fetch_error_type": None,
        "api_key": "secret",
        "authorization": "Bearer token",
        "cookie": "abc",
        "payment_signature": "sig",
        "private_key": "pkey",
        "seed_phrase": "seed",
        "raw_headers": {"x": "y"},
    }
    clean = sanitize_abi_source_cache_payload(payload)
    dumped = str(clean).lower()
    for forbidden in ["api_key", "authorization", "cookie", "payment_signature", "private_key", "seed_phrase", "raw_headers"]:
        assert forbidden not in dumped


def test_no_paid_provider_or_filesystem_write_requirements():
    text = MODULE_PATH.read_text(encoding="utf-8").lower()
    assert "requests." not in text
    assert "write_text(" not in text
    assert "open(" not in text


def test_docs_mention_disabled_default_and_no_managed_redis():
    strategy = STRATEGY_DOC.read_text(encoding="utf-8").lower()
    db_plan = DB_PLAN_DOC.read_text(encoding="utf-8").lower()
    assert "disabled by default" in strategy
    assert "managed redis remains postponed" in strategy
    assert "database_url is not required by default" in strategy
    assert "managed redis is postponed by default" in db_plan


def test_env_unchanged_during_cache_boundary_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = get_abi_source_cache_status()
    _ = build_abi_source_cache_key("0x2222", "base", "none")
    _ = sanitize_abi_source_cache_payload({})
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
