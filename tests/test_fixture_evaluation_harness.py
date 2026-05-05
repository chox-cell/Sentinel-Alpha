import hashlib
from pathlib import Path

from services.scanner_engine.evaluation_harness import (
    evaluate_fixture_dataset,
    load_base_fixture_dataset,
    summarize_evaluation_results,
)


def _by_type(results: list[dict], fixture_type: str) -> dict:
    for row in results:
        if row.get("fixture_type") == fixture_type:
            return row
    raise AssertionError(f"missing fixture type: {fixture_type}")


def test_fixture_dataset_loads_and_has_expected_count():
    fixtures = load_base_fixture_dataset()
    assert len(fixtures) == 8


def test_all_fixtures_evaluated_expected_vs_observed_present():
    fixtures = load_base_fixture_dataset()
    results = evaluate_fixture_dataset(fixtures)
    assert len(results) == 8
    for row in results:
        assert "expected_signals" in row
        assert "observed_signals" in row
        assert "matched_signals" in row
        assert "missing_expected_signals" in row
        assert row["evaluation_status"] in {"pass", "review"}


def test_key_fixture_signal_matches():
    fixtures = load_base_fixture_dataset()
    results = evaluate_fixture_dataset(fixtures)

    erc20 = _by_type(results, "erc20_like")
    assert "erc20_candidate" in erc20["matched_signals"]

    erc721 = _by_type(results, "erc721_like")
    assert "erc721_candidate" in erc721["matched_signals"]

    erc1155 = _by_type(results, "erc1155_like")
    assert "erc1155_candidate" in erc1155["matched_signals"]

    proxy_like = _by_type(results, "proxy_like")
    assert ("proxy_candidate" in proxy_like["matched_signals"]) or (
        "proxy_pattern_possible" in proxy_like["matched_signals"]
    )

    opcode_like = _by_type(results, "bytecode_opcode")
    for key in ["delegatecall_present", "selfdestruct_present", "external_call_present"]:
        if key in opcode_like["expected_signals"]:
            assert key in opcode_like["matched_signals"]


def test_summary_includes_total_and_no_overclaim_language():
    fixtures = load_base_fixture_dataset()
    results = evaluate_fixture_dataset(fixtures)
    summary = summarize_evaluation_results(results)
    assert summary["total_fixtures"] == 8
    text = str(summary).lower()
    assert "proves honeypot detection" not in text
    assert "malicious certainty" not in text
    assert "live simulation available" not in text


def test_env_unchanged_during_harness_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    fixtures = load_base_fixture_dataset()
    results = evaluate_fixture_dataset(fixtures)
    _ = summarize_evaluation_results(results)
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
