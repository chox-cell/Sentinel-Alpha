import importlib
import json
import os

from fastapi.testclient import TestClient

import apps.api.main as main_module


def test_internal_env_source_uses_runtime_env_values(monkeypatch):
    saved = {
        "PAYMENT_MODE": os.environ.get("PAYMENT_MODE"),
        "X402_ENABLED": os.environ.get("X402_ENABLED"),
        "APP_ENV": os.environ.get("APP_ENV"),
    }
    try:
        os.environ["PAYMENT_MODE"] = "real"
        os.environ["X402_ENABLED"] = "true"
        os.environ["APP_ENV"] = "testverify"

        client = TestClient(main_module.app)
        es = client.get("/internal/env/source").json()
        xs = client.get("/internal/x402/status").json()

        assert es == {
            "env_source": ".env",
            "override": True,
            "app_env": "testverify",
            "payment_mode": "real",
            "x402_enabled": True,
        }
        assert xs["payment_mode"] == es["payment_mode"]
        raw = json.dumps({"env_source": es, "x402": xs})
        assert "secret" not in raw.lower()
    finally:
        for key, val in saved.items():
            if val is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = val
        importlib.reload(main_module)
