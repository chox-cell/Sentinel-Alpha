from pathlib import Path


def test_typescript_sdk_files_exist():
    assert Path("sdk/typescript/client.ts").exists()
    assert Path("sdk/typescript/README.md").exists()


def test_typescript_client_has_required_surface():
    content = Path("sdk/typescript/client.ts").read_text(encoding="utf-8")
    assert "class SentinelAlphaClient" in content
    assert "constructor(baseUrl: string, paymentHeader?: string)" in content
    assert "async scan(contractAddress: string, chain = \"base\", lane = \"basic\")" in content
    assert "\"X-SENTINEL-LANE\": lane" in content
    assert "/contracts/risk-score" in content
