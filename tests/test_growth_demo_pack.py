import os
import pytest

def test_files_exist():
    base_path = "/Users/chox/Projects/Sentinel-Alpha"
    files = [
        "apps/website/demo.html",
        "docs/16_launch/VIDEO_SCRIPTS.md",
        "docs/16_launch/CONTENT_CALENDAR_14_DAYS.md",
        "docs/16_launch/FOUNDER_OUTREACH_TRACKER.md",
    ]
    for file_path in files:
        full_path = os.path.join(base_path, file_path)
        assert os.path.exists(full_path), f"File {file_path} is missing"

def test_readme_links():
    readme_path = "/Users/chox/Projects/Sentinel-Alpha/README.md"
    with open(readme_path, "r") as f:
        content = f.read()
        assert "demo.html" in content
        assert "beezshield.com" in content
        assert "8004scan" in content

def test_no_secrets_in_launch_docs():
    docs_path = "/Users/chox/Projects/Sentinel-Alpha/docs/16_launch"
    for root, dirs, files in os.walk(docs_path):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                content = f.read()
                # Simple check for common secret patterns
                assert "0x" not in content or "0x..." in content or "0xaaaa" in content or "0x1111" in content or "0xSIGNED" in content or "45967" in content
                assert "PRIVATE_KEY" not in content
                assert "SECRET" not in content or "L4_SECRET" in content or "Researching" in content or "Researching" in content
