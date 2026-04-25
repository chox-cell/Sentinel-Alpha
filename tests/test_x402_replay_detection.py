from fastapi.testclient import TestClient

from apps.api.main import app
from services.x402 import replay_guard


def _request_body() -> dict:
    return {
        "contract_address": "0x1111111111111111111111111111111111111199",
        "chain": "base",
        "context": {"event_type": "new_deploy"},
    }


def test_replay_detection_blocks_second_use(monkeypatch, tmp_path):
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", tmp_path / "x402_payments.jsonl")
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "false")
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("PRICE_BASIC", "0.02")

    tx_header = "tx:0x" + ("c" * 64)
    client = TestClient(app)

    first = client.post(
        "/contracts/risk-score",
        json=_request_body(),
        headers={"X402-PAYMENT": tx_header},
    )
    assert first.status_code == 200
    assert first.json()["billing"]["status"] == "tx_format_valid_unverified"

    second = client.post(
        "/contracts/risk-score",
        json=_request_body(),
        headers={"X402-PAYMENT": tx_header},
    )
    assert second.status_code == 402
    assert second.json()["detail"] == {"error": "x402_replay_detected"}
