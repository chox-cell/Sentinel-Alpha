from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GITIGNORE = REPO_ROOT / ".gitignore"
POLICY_DOC = REPO_ROOT / "docs/16_launch/ENV_SAFETY_POLICY.md"


def test_env_is_gitignored():
    content = GITIGNORE.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    assert ".env" in lines


def test_env_safety_policy_doc_exists_and_mentions_core_rules():
    text = POLICY_DOC.read_text(encoding="utf-8").lower()
    required = [
        "sacred local secret state",
        "tests must never write to repo",
        ".env.example",
    ]
    for token in required:
        assert token in text


def test_no_test_writes_repo_env_directly():
    tests_dir = REPO_ROOT / "tests"
    py_files = list(tests_dir.glob("test_*.py"))
    forbidden_snippets = [
        'repo_root / ".env"',
        "env_path.write_text(",
        "def _write_repo_env(",
    ]
    offenders: list[str] = []
    for path in py_files:
        text = path.read_text(encoding="utf-8")
        if '.env.example' in text:
            continue
        if any(snippet in text for snippet in forbidden_snippets):
            offenders.append(str(path.relative_to(REPO_ROOT)))
    assert offenders == []
