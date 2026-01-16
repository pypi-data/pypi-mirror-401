"""Tests for hivemind-p2p binary locator and basic functionality."""

import subprocess
import sys
from pathlib import Path

import pytest

from hivemind_p2p import get_binary_path


def test_binary_path_exists():
    """Test that get_binary_path returns a valid path."""
    binary_path = get_binary_path()
    assert binary_path.exists(), f"Binary not found at {binary_path}"
    assert binary_path.is_file(), f"Binary path is not a file: {binary_path}"


def test_binary_is_executable():
    """Test that the binary is executable."""
    binary_path = get_binary_path()
    # On Unix, check executable bit; on Windows, .exe is always executable
    if sys.platform != "win32":
        import os
        assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"


def test_binary_version_or_help():
    """Test that the binary responds to --help."""
    binary_path = get_binary_path()
    result = subprocess.run(
        [str(binary_path), "--help"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, f"Binary --help failed: {result.stderr}"
    assert "hivemind-p2p" in result.stdout.lower() or "share" in result.stdout.lower()


def test_share_command_help():
    """Test that share subcommand help works."""
    binary_path = get_binary_path()
    result = subprocess.run(
        [str(binary_path), "share", "--help"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, f"share --help failed: {result.stderr}"
    assert "frontend" in result.stdout.lower() or "hub" in result.stdout.lower()


def test_join_command_help():
    """Test that join subcommand help works."""
    binary_path = get_binary_path()
    result = subprocess.run(
        [str(binary_path), "join", "--help"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, f"join --help failed: {result.stderr}"
    assert "ticket" in result.stdout.lower() or "join-code" in result.stdout.lower()
