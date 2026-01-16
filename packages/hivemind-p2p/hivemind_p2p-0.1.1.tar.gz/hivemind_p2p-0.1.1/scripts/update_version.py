#!/usr/bin/env python3
"""
Script to update version in both pyproject.toml and Cargo.toml
Usage: python scripts/update_version.py <version>
Example: python scripts/update_version.py 0.1.2
"""

import sys
import re
from pathlib import Path

def update_pyproject_version(version: str) -> None:
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Update version line
    updated_content = re.sub(
        r'^version = ".*"',
        f'version = "{version}"',
        content,
        flags=re.MULTILINE
    )
    
    pyproject_path.write_text(updated_content)
    print(f"Updated pyproject.toml version to {version}")

def update_cargo_version(version: str) -> None:
    """Update version in Cargo.toml"""
    cargo_path = Path("Cargo.toml")
    content = cargo_path.read_text()
    
    # Update version line in [package] section
    updated_content = re.sub(
        r'^version = ".*"',
        f'version = "{version}"',
        content,
        flags=re.MULTILINE
    )
    
    cargo_path.write_text(updated_content)
    print(f"Updated Cargo.toml version to {version}")

def validate_version(version: str) -> bool:
    """Validate semantic version format"""
    pattern = r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9-]+)*(?:\+[a-zA-Z0-9-]+)*$'
    return bool(re.match(pattern, version))

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/update_version.py <version>")
        print("Example: python scripts/update_version.py 0.1.2")
        sys.exit(1)
    
    version = sys.argv[1]
    
    if not validate_version(version):
        print(f"Error: Invalid version format '{version}'")
        print("Expected format: MAJOR.MINOR.PATCH (e.g., 1.2.3)")
        sys.exit(1)
    
    try:
        update_pyproject_version(version)
        update_cargo_version(version)
        print(f"✅ Successfully updated version to {version}")
    except Exception as e:
        print(f"❌ Error updating version: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()