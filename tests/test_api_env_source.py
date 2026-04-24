import importlib
import json
import os
from pathlib import Path

from fastapi.testclient import TestClient

import apps.api.main as main_module


def _write_repo_env(repo_root: Path, content: str):
    env_path = repo_root / ".env"
    existed = env_path.exists()
    previous = env_path.read_text(encoding="utf-8") if existed else None
    env_path.write_text(content, encoding="utf-8")
    return env_path, existed, previous


def _restore_repo_env(env_path: Path, existed: bool, previous: str | None):
    if existed:
        env_path.write_text(previous or "", encoding="utf-8")
    elif env_path.exists():
        env_path.unlink()


def test_internal_env_source_dotenv_overrides_shell_for_api():
    repo_root = Path(__file__).resolve().parents[1]
    env_path, existed, previous = _write_repo_env(
        repo_root,
        "\n".join(
            [
                "PAYMENT_MODE=real",
                "X402_ENABLED=true",
                "APP_ENV=testverify",
                "",
            ]
        ),
    )
    saved = {
        "PAYMENT_MODE": os.environ.get("PAYMENT_MODE"),
        "X402_ENABLED": os.environ.get("X402_ENABLED"),
        "APP_ENV": os.environ.get("APP_ENV"),
    }
    try:
        os.environ["PAYMENT_MODE"] = "demo"
        os.environ["X402_ENABLED"] = "false"
        os.environ["APP_ENV"] = "shell_should_lose"

        importlib.reload(main_module)

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
        assert "shell_should_lose" not in raw
    finally:
        for key, val in saved.items():
            if val is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = val
        _restore_repo_env(env_path, existed, previous)
        importlib.reload(main_module)
