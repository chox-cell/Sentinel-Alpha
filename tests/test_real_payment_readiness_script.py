import json
import os
import subprocess
import sys
from pathlib import Path


def test_real_payment_readiness_script_outputs_required_fields(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "print_real_payment_readiness.py"
    assert script_path.exists()

    env = dict(os.environ)
    env.update(
        {
            "PAYMENT_MODE": "real",
            "X402_ENABLED": "true",
            "X402_ONCHAIN_VERIFY": "false",
            "BASE_RPC_URL": "https://secret-rpc.example",
            "X402_REVENUE_ADDRESS": "0x1111111111111111111111111111111111111111",
            "SENTINEL_TREASURY_WALLET": "0x2222222222222222222222222222222222222222",
            "PRICE_BASIC": "0.02",
            "PRICE_EXECUTIVE": "0.05",
            "PRICE_PREMIUM": "0.10",
            "PRICE_PRIORITY": "0.15",
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

    output = result.stdout
    body = json.loads(output)
    assert set(body.keys()) == {
        "payment_mode",
        "x402_enabled",
        "onchain_verify_enabled",
        "base_rpc_configured",
        "treasury_configured",
        "wallet_address_configured",
        "pricing_tiers",
        "readiness_verdict",
    }
    assert body["payment_mode"] == "real"
    assert body["x402_enabled"] is True
    assert body["onchain_verify_enabled"] is False
    assert body["base_rpc_configured"] is True
    assert body["treasury_configured"] is True
    assert body["wallet_address_configured"] is True
    assert body["readiness_verdict"] == "not_ready"
    assert "secret-rpc.example" not in output
