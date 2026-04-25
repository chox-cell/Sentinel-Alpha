import os
import subprocess
import sys
from pathlib import Path


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


def test_prelaunch_script_ready_path_and_required_lines():
    proc = _run_prelaunch_script(
        {
            "PAYMENT_MODE": "real",
            "X402_ENABLED": "true",
            "X402_MOCK_ONCHAIN_VERIFY": "false",
            "BASE_RPC_URL": "https://base-rpc.example",
            "SENTINEL_TREASURY_WALLET": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "AGENT_WALLET_ADDRESS": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        }
    )
    assert proc.returncode == 0
    out = proc.stdout
    assert "pytest command reminder: python3 -m pytest tests/ -q --tb=no" in out
    assert "env source: .env" in out
    assert "PAYMENT_MODE: real" in out
    assert "X402_ENABLED: true" in out
    assert "X402_MOCK_ONCHAIN_VERIFY must be false: true" in out
    assert "BASE_RPC_URL configured: true" in out
    assert "wallet configured: true" in out
    assert "treasury configured: true" in out
    assert "agentic-market.json exists: true" in out
    assert "README exists: true" in out
    assert "SDK docs exist: true" in out
    assert "launch docs exist: true" in out
    assert "readiness verdict: ready" in out


def test_prelaunch_script_not_ready_and_does_not_print_secret_values():
    secret_rpc = "https://super-secret-rpc.example/token-value"
    proc = _run_prelaunch_script(
        {
            "PAYMENT_MODE": "real",
            "X402_ENABLED": "true",
            "X402_MOCK_ONCHAIN_VERIFY": "true",
            "BASE_RPC_URL": secret_rpc,
            "SENTINEL_TREASURY_WALLET": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "AGENT_WALLET_ADDRESS": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        }
    )
    assert proc.returncode == 0
    out = proc.stdout
    assert "X402_MOCK_ONCHAIN_VERIFY must be false: false" in out
    assert "readiness verdict: not_ready" in out
    assert secret_rpc not in out
