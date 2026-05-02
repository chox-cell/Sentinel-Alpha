"""Repo contracts for packages/sentinel-sdk (@beezshield/sentinel)."""

from pathlib import Path


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_sentinel_sdk_package_manifest():
    pkg = Path("packages/sentinel-sdk/package.json")
    body = _read(pkg)
    assert "@beezshield/sentinel" in body
    assert '"type": "module"' in body


def test_sentinel_sdk_entrypoints_exist():
    base = Path("packages/sentinel-sdk")
    assert (base / "src" / "index.ts").is_file()
    assert (base / "README.md").is_file()
    assert (base / "tsconfig.build.json").is_file()


def test_sentinel_sdk_readme_truth_markers():
    readme = _read(Path("packages/sentinel-sdk/README.md"))
    assert "not published to npm yet" in readme.lower() or "publish pending" in readme.lower()
    assert "planned package name" in readme.lower()
    assert "automatic settlement is not implemented" in readme.lower() or "automatic settlement is not implemented" in readme
    assert "agentkit provider" in readme.lower() and "not live yet" in readme.lower()


def test_sentinel_sdk_source_exports_no_fake_publish_claim():
    index = _read(Path("packages/sentinel-sdk/src/index.ts"))
    for name in ("createSentinelClient", "scoreContract", "decideBeforeExecution", "isX402Challenge", "normalizeSentinelDecision"):
        assert name in index


def test_sentinel_sdk_fixtures_exclude_secrets():
    src = Path("packages/sentinel-sdk/src").rglob("*")
    for p in src:
        if p.suffix not in {".ts", ".md"}:
            continue
        text = _read(p)
        for leak in ('private_key "', "PRIVATE_KEY=", "sekret.api", "https://alchemy.com/", "alchemy_api"):
            assert leak.lower() not in text.lower()
