"""Locate the bundled hivemind-p2p binary."""

import shutil
import sys
from pathlib import Path


def get_binary_path() -> Path:
    """Get path to the hivemind-p2p binary.

    When installed via pip with maturin, the binary is placed in the
    scripts directory alongside the Python executable.

    Returns:
        Path to the hivemind-p2p binary.

    Raises:
        FileNotFoundError: If the binary cannot be located.
    """
    binary_name = "hivemind-p2p.exe" if sys.platform == "win32" else "hivemind-p2p"

    # Check alongside Python executable (virtual environment)
    python_dir = Path(sys.executable).parent
    binary_path = python_dir / binary_name
    if binary_path.exists():
        return binary_path

    # Fallback: check system PATH
    system_path = shutil.which("hivemind-p2p")
    if system_path:
        return Path(system_path)

    raise FileNotFoundError(
        "hivemind-p2p binary not found. "
        "Please reinstall the package: pip install hivemind-p2p"
    )
