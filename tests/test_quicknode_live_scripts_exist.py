from pathlib import Path


def test_quicknode_live_scripts_exist():
    expected = [
        Path("scripts/check_quicknode_live_ready.py"),
        Path("scripts/test_quicknode_webhook_local.py"),
        Path("scripts/test_quicknode_webhook_public.py"),
    ]
    for path in expected:
        assert path.exists(), f"Missing script: {path}"
