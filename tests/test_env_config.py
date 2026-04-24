import pytest

from shared.config.env import get_env_bool, get_quicknode_env_status, get_required_env


def test_get_env_bool_parses_values(monkeypatch):
    monkeypatch.setenv("FLAG", "true")
    assert get_env_bool("FLAG") is True
    monkeypatch.setenv("FLAG", "0")
    assert get_env_bool("FLAG") is False
    monkeypatch.delenv("FLAG", raising=False)
    assert get_env_bool("FLAG", default=True) is True


def test_get_required_env_raises_for_missing(monkeypatch):
    monkeypatch.delenv("MUST_HAVE", raising=False)
    with pytest.raises(ValueError):
        get_required_env("MUST_HAVE")


def test_get_quicknode_env_status_no_secret_exposed(monkeypatch):
    monkeypatch.setenv("QUICKNODE_WEBHOOK_URL", "https://example.com/webhook")
    monkeypatch.setenv("QUICKNODE_WEBHOOK_SECRET", "super-secret")
    monkeypatch.setenv("QUICKNODE_DRY_RUN", "true")

    status = get_quicknode_env_status()
    assert status["webhook_url_configured"] is True
    assert status["webhook_secret_configured"] is True
    assert status["dry_run"] is True
    assert status["signature_mode"] == "enabled"
    assert "QUICKNODE_WEBHOOK_SECRET" not in status
