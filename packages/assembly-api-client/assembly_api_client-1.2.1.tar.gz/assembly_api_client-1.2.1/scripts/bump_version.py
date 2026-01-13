#!/usr/bin/env python3
"""Script to bump patch version in pyproject.toml"""

import re
from pathlib import Path


def bump_patch_version(pyproject_path: Path) -> str:
    """Bump patch version in pyproject.toml and return new version."""
    content = pyproject_path.read_text()

    # Find version line
    pattern = r'version = "(\d+)\.(\d+)\.(\d+)"'
    match = re.search(pattern, content)

    if not match:
        raise ValueError("Could not find version in pyproject.toml")

    major, minor, patch = match.groups()
    new_patch = int(patch) + 1
    new_version = f"{major}.{minor}.{new_patch}"

    # Replace version
    new_content = re.sub(pattern, f'version = "{new_version}"', content)
    pyproject_path.write_text(new_content)

    return new_version


if __name__ == "__main__":
    pyproject = Path("pyproject.toml")
    new_ver = bump_patch_version(pyproject)
    print(f"Bumped version to {new_ver}")
