import sys
import types


class _DummyRedisClient:
    def __init__(self):
        self._store = {}

    def get(self, key):
        return self._store.get(key)

    def setex(self, key, ttl, value):
        self._store[key] = value


if "redis" not in sys.modules:
    sys.modules["redis"] = types.SimpleNamespace(Redis=lambda *args, **kwargs: _DummyRedisClient())
