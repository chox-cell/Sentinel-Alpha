from pathlib import Path


DOC = Path("docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md")


def test_data_provider_strategy_exists():
    assert DOC.exists(), f"missing {DOC}"


def test_data_provider_strategy_required_content():
    text = DOC.read_text(encoding="utf-8").lower()
    required = [
        "data ladder",
        "abi/source feed",
        "local bytecode analysis",
        "local postgres",
        "simulation provider adapter",
        "mempool/mev feed",
        "no paid quicknode by default",
        "no managed postgres by default",
        "no paid simulation provider by default",
        "v6.1 local bytecode analyzer first",
    ]
    for token in required:
        assert token in text
