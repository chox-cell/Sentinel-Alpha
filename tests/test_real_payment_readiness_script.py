import json
import os
import subprocess
import sys
from pathlib import Path


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


def test_real_payment_readiness_script_outputs_required_fields(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "print_real_payment_readiness.py"
    assert script_path.exists()

    env_path, existed, previous = _write_repo_env(
        repo_root,
        "\n".join(
            [
                "PAYMENT_MODE=real",
                "X402_ENABLED=true",
                "X402_ONCHAIN_VERIFY=false",
                "BASE_RPC_URL=https://secret-rpc.example",
                "X402_REVENUE_ADDRESS=0x1111111111111111111111111111111111111111",
                "SENTINEL_TREASURY_WALLET=0x2222222222222222222222222222222222222222",
                "PRICE_BASIC=0.02",
                "PRICE_EXECUTIVE=0.05",
                "PRICE_PREMIUM=0.10",
                "PRICE_PRIORITY=0.15",
                "",
            ]
        ),
    )

    try:
        env = dict(os.environ)
        env.update(
            {
                "PAYMENT_MODE": "demo",
                "X402_ENABLED": "false",
                "X402_ONCHAIN_VERIFY": "true",
            }
        )

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
    finally:
        _restore_repo_env(env_path, existed, previous)

    output = result.stdout
    body = json.loads(output)
    assert set(body.keys()) == {
        "env_source",
        "payment_mode",
        "x402_enabled",
        "onchain_verify_enabled",
        "base_rpc_configured",
        "treasury_configured",
        "wallet_address_configured",
        "pricing_tiers",
        "readiness_verdict",
    }
    assert body["env_source"] == ".env"
    assert body["payment_mode"] == "real"
    assert body["x402_enabled"] is True
    assert body["onchain_verify_enabled"] is False
    assert body["base_rpc_configured"] is True
    assert body["treasury_configured"] is True
    assert body["wallet_address_configured"] is True
    assert body["readiness_verdict"] == "not_ready"
    assert "secret-rpc.example" not in output


def test_real_payment_readiness_wallet_vs_treasury_flags():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "print_real_payment_readiness.py"
    env_path, existed, previous = _write_repo_env(
        repo_root,
        "\n".join(
            [
                "PAYMENT_MODE=demo",
                "X402_ENABLED=false",
                "X402_ONCHAIN_VERIFY=false",
                "BASE_RPC_URL=",
                "X402_REVENUE_ADDRESS=",
                "SENTINEL_TREASURY_WALLET=",
                "AGENT_WALLET_ADDRESS=0x3333333333333333333333333333333333333333",
                "",
            ]
        ),
    )

    try:
        env = dict(os.environ)
        env.update(
            {
                "SENTINEL_TREASURY_WALLET": "0x4444444444444444444444444444444444444444",
            }
        )

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
    finally:
        _restore_repo_env(env_path, existed, previous)
    body = json.loads(result.stdout)
    assert body["wallet_address_configured"] is True
    assert body["treasury_configured"] is False


def test_real_payment_readiness_env_overrides_shell_payment_mode():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "print_real_payment_readiness.py"
    env_path, existed, previous = _write_repo_env(
        repo_root,
        "\n".join(
            [
                "PAYMENT_MODE=real",
                "X402_ENABLED=true",
                "X402_ONCHAIN_VERIFY=false",
                "",
            ]
        ),
    )
    try:
        env = dict(os.environ)
        env.update(
            {
                "PAYMENT_MODE": "demo",
                "X402_ENABLED": "false",
            }
        )
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
    finally:
        _restore_repo_env(env_path, existed, previous)

    body = json.loads(result.stdout)
    assert body["payment_mode"] == "real"
    assert body["x402_enabled"] is True
