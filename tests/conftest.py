import sys
import types

import pytest


@pytest.fixture(autouse=True)
def _sentinel_stable_demo_payment_env(monkeypatch):
    """
    `apps/api/main.py` loads `.env` at import time; local checkouts may set
    PAYMENT_MODE=real and break demo-header POST expectations in API tests.

    Tests that assert real-payment behavior override this via their own monkeypatch.
    """
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("PAYMENT_DEMO_SIGNATURE", "demo")


class _DummyRedisClient:
    def __init__(self):
        self._store = {}

    def get(self, key):
        return self._store.get(key)

    def setex(self, key, ttl, value):
        self._store[key] = value


if "redis" not in sys.modules:
    sys.modules["redis"] = types.SimpleNamespace(Redis=lambda *args, **kwargs: _DummyRedisClient())
