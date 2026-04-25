import os
import subprocess
import sys
from pathlib import Path

import pytest


def _run_production_env_check(extra_env: dict) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(extra_env)
    return subprocess.run(
        [sys.executable, "scripts/production_env_check.py"],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def controlled_production_env():
    root = Path(__file__).resolve().parents[1]
    env_path = root / ".env"
    original = env_path.read_text(encoding="utf-8") if env_path.exists() else None
    env_path.write_text(
        "\n".join(
            [
                "APP_ENV=production",
                "PUBLIC_BASE_URL=https://api.sentinel-alpha.example",
                "PAYMENT_MODE=real",
                "X402_ENABLED=true",
                "X402_MOCK_ONCHAIN_VERIFY=false",
                "X402_ONCHAIN_VERIFY=true",
                "BASE_RPC_URL=https://base-rpc.example/secret",
                "QUICKNODE_SIGNATURE_REQUIRED=true",
                "RATE_LIMIT_ENABLED=true",
                "AGENT_WALLET_ADDRESS=0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "SENTINEL_TREASURY_WALLET=0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "",
            ]
        ),
        encoding="utf-8",
    )
    try:
        yield
    finally:
        if original is None:
            env_path.unlink(missing_ok=True)
        else:
            env_path.write_text(original, encoding="utf-8")


def test_production_env_check_ready_and_secret_safe(controlled_production_env):
    secret_rpc = "https://shell-secret-rpc.example/token"
    proc = _run_production_env_check({"BASE_RPC_URL": secret_rpc})
    assert proc.returncode == 0
    out = proc.stdout
    assert "APP_ENV=production: true" in out
    assert "PUBLIC_BASE_URL configured: true" in out
    assert "PAYMENT_MODE=real: true" in out
    assert "X402_ENABLED=true: true" in out
    assert "X402_MOCK_ONCHAIN_VERIFY=false: true" in out
    assert "X402_ONCHAIN_VERIFY=true: true" in out
    assert "BASE_RPC_URL configured: true" in out
    assert "QUICKNODE_SIGNATURE_REQUIRED=true: true" in out
    assert "RATE_LIMIT_ENABLED=true: true" in out
    assert "wallet configured: true" in out
    assert "treasury configured: true" in out
    assert "production ready: true" in out
    assert secret_rpc not in out


def test_production_env_check_not_ready_when_required_flags_missing(controlled_production_env):
    root = Path(__file__).resolve().parents[1]
    env_path = root / ".env"
    env_path.write_text(
        "\n".join(
            [
                "APP_ENV=production",
                "PUBLIC_BASE_URL=https://api.sentinel-alpha.example",
                "PAYMENT_MODE=real",
                "X402_ENABLED=true",
                "X402_MOCK_ONCHAIN_VERIFY=true",
                "X402_ONCHAIN_VERIFY=false",
                "BASE_RPC_URL=",
                "QUICKNODE_SIGNATURE_REQUIRED=false",
                "RATE_LIMIT_ENABLED=false",
                "AGENT_WALLET_ADDRESS=",
                "SENTINEL_TREASURY_WALLET=",
                "",
            ]
        ),
        encoding="utf-8",
    )
    proc = _run_production_env_check({})
    assert proc.returncode == 0
    out = proc.stdout
    assert "X402_MOCK_ONCHAIN_VERIFY=false: false" in out
    assert "X402_ONCHAIN_VERIFY=true: false" in out
    assert "BASE_RPC_URL configured: false" in out
    assert "production ready: false" in out
