import os
import subprocess
import sys
from pathlib import Path

import pytest


def _run_prelaunch_script(extra_env: dict) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(extra_env)
    return subprocess.run(
        [sys.executable, "scripts/prelaunch_check.py"],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def controlled_repo_env():
    root = Path(__file__).resolve().parents[1]
    env_path = root / ".env"
    original = env_path.read_text(encoding="utf-8") if env_path.exists() else None
    env_path.write_text(
        "\n".join(
            [
                "PAYMENT_MODE=real",
                "X402_ENABLED=true",
                "X402_MOCK_ONCHAIN_VERIFY=false",
                "BASE_RPC_URL=https://base-rpc.example/from-dotenv",
                "SENTINEL_TREASURY_WALLET=0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "AGENT_WALLET_ADDRESS=0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
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


def test_prelaunch_script_ready_path_and_required_lines(controlled_repo_env):
    proc = _run_prelaunch_script(
        {
            # Shell env conflicts with .env; script must use .env as SSOT.
            "PAYMENT_MODE": "demo",
            "X402_ENABLED": "false",
        }
    )
    assert proc.returncode == 0
    out = proc.stdout
    assert "pytest command reminder: python3 -m pytest tests/ -q --tb=no" in out
    assert "env source: .env" in out
    assert "PAYMENT_MODE: real" in out
    assert "payment real mode ready: true" in out
    assert "X402_ENABLED: true" in out
    assert "x402 enabled: true" in out
    assert "mock mode disabled: true" in out
    assert "BASE_RPC_URL configured: true" in out
    assert "wallet configured: true" in out
    assert "treasury configured: true" in out
    assert "agentic-market.json exists: true" in out
    assert "README exists: true" in out
    assert "SDK docs exist: true" in out
    assert "launch docs exist: true" in out
    assert "launch ready: true" in out
    assert "readiness verdict: ready" in out


def test_prelaunch_script_not_ready_and_does_not_print_secret_values(controlled_repo_env):
    secret_rpc = "https://super-secret-rpc.example/token-value"
    proc = _run_prelaunch_script(
        {
            # PAYMENT_MODE/X402_ENABLED should still come from .env due to override=True.
            "PAYMENT_MODE": "demo",
            "X402_ENABLED": "false",
            "X402_MOCK_ONCHAIN_VERIFY": "true",
            "BASE_RPC_URL": secret_rpc,
        }
    )
    assert proc.returncode == 0
    out = proc.stdout
    assert "PAYMENT_MODE: real" in out
    assert "X402_ENABLED: true" in out
    assert "mock mode disabled: true" in out
    assert "launch ready: true" in out
    assert "readiness verdict: ready" in out
    assert secret_rpc not in out
