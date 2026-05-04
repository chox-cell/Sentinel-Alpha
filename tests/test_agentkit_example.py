from pathlib import Path


def test_agentkit_example_files_exist():
    base = Path("examples/agentkit-sentinel")
    assert (base / "package.json").exists()
    assert (base / "README.md").exists()
    assert (base / ".env.example").exists()
    assert (base / "src" / "index.ts").exists()
    assert Path("docs/16_launch/SENTINEL_AGENTKIT_EXAMPLE.md").exists()


def test_agentkit_example_code_and_safety():
    content = Path("examples/agentkit-sentinel/src/index.ts").read_text(encoding="utf-8")
    assert "@beezshield/sentinel" in content
    assert "decideBeforeExecution" in content
    assert "SentinelPaymentRequiredError" in content
    assert "contract_address" in content

    forbidden = [
        "PRIVATE_KEY",
        "SECRET_KEY",
        "MNEMONIC",
        "guaranteed protection",
    ]
    for token in forbidden:
        assert token not in content


def test_agentkit_example_readme_truthfulness():
    text = Path("examples/agentkit-sentinel/README.md").read_text(encoding="utf-8").lower()
    assert "agentkit-style" in text
    assert "coinbase agentkit provider" in text
    assert "not" in text
    assert "official" in text
    assert "live" in text
    assert "coming next" in text
    assert "does not perform automatic x402 settlement" in text
    assert "does not guarantee protection" in text
    assert "npm install @beezshield/sentinel" in text
    assert "provider is live" not in text
