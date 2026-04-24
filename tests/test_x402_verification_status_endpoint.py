from fastapi.testclient import TestClient

from apps.api.main import app


def test_x402_verification_status_endpoint(monkeypatch):
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "false")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xtreasury")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)

    client = TestClient(app)
    response = client.get("/internal/x402/verification/status")
    assert response.status_code == 200
    body = response.json()
    assert body == {
        "onchain_verify_enabled": False,
        "accepted_payment_format": "tx:0x<64_hex_chars>",
        "network": "base",
        "treasury_configured": True,
    }
