from services.x402.payment_config import get_payment_status


def test_cdp_alias_pair_sets_api_key_configured(monkeypatch):
    monkeypatch.delenv("CDP_API_KEY_NAME", raising=False)
    monkeypatch.delenv("CDP_API_KEY_PRIVATE_KEY", raising=False)
    monkeypatch.setenv("CDP_API_KEY_ID", "alias-id")
    monkeypatch.setenv("CDP_API_KEY_SECRET", "alias-secret")

    status = get_payment_status()
    assert status["cdp_api_key_configured"] is True
