from pathlib import Path


def test_public_launch_docs_exist():
    assert Path("README.md").exists()
    assert Path("docs/14_distribution/API_QUICKSTART.md").exists()
    assert Path("docs/14_distribution/BOT_INTEGRATION_GUIDE.md").exists()
    assert Path("docs/14_distribution/PRE_LAUNCH_CHECKLIST.md").exists()


def test_readme_has_required_public_launch_content():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "Execution Fidelity Layer for Bots and Agents" in readme
    assert "What Problem It Solves" in readme
    assert "What The API Returns" in readme
    assert "/contracts/risk-score" in readme
    assert "x402" in readme
    assert "eip155:8453" in readme
    assert "`basic`: `0.02`" in readme
    assert "`executive`: `0.05`" in readme
    assert "`premium`: `0.10`" in readme
    assert "`priority`: `0.15`" in readme
    assert "Real Base USDC payment verified" in readme
    assert "x402 replay protection active" in readme
    assert "settlement ledger active" in readme
    assert "smoke test pass" in readme
    assert "v1.5.0" in readme
    assert "X402-PAYMENT: tx:0x" in readme
    assert "Python SDK Quickstart" in readme
    assert "TypeScript SDK Quickstart" in readme
    assert "agentic-market.json" in readme
    assert "marketplace-submission.json" in readme
    assert "identity-manifest.json" in readme
    assert "local DID active" in readme
    assert "ERC-8004 planned / adapter stub" in readme
    assert "Real payment test is required before launch" in readme
    assert "Do not enable mock verification in production" in readme
    assert "Never commit `.env`" in readme
