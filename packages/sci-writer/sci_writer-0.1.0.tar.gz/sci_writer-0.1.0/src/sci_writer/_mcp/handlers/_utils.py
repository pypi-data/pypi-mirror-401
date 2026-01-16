"""Shared utilities for MCP handlers."""

from __future__ import annotations

import subprocess
import sys


def run_cli(args: list[str], timeout: int = 300) -> tuple[bool, str, str]:
    """Run sci-writer CLI command and return (success, stdout, stderr)."""
    cmd = [sys.executable, "-m", "sci_writer._cli"] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return (
            result.returncode == 0,
            result.stdout,
            result.stderr,
        )
    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout}s"
    except Exception as e:
        return False, "", str(e)
