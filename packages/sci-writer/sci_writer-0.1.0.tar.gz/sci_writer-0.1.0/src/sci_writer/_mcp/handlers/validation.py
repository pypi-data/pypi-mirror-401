"""MCP handlers for validation and history operations.

All handlers delegate to CLI commands to maintain MCP->CLI->Python chain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ._utils import run_cli


async def check_handler(arguments: dict[str, Any]) -> str:
    """Handle check tool invocation via CLI.

    Args:
        arguments: Tool arguments containing:
            - project_dir: Path to project directory (required)
            - doc_type: Document type (manuscript/supplementary/revision)

    Returns:
        JSON string with validation results
    """
    project_dir = Path(arguments["project_dir"])
    doc_type = arguments.get("doc_type", "manuscript")

    if not project_dir.exists():
        return json.dumps(
            {"success": False, "error": f"Project directory not found: {project_dir}"}
        )

    cli_args = ["check", str(project_dir), "-t", doc_type, "--json"]
    success, stdout, stderr = run_cli(cli_args)

    if stdout.strip():
        try:
            data = json.loads(stdout)
            return json.dumps({"success": True, **data})
        except json.JSONDecodeError:
            pass

    return json.dumps(
        {
            "success": success,
            "output": stdout,
            "error": stderr if not success else None,
        }
    )


async def versions_handler(arguments: dict[str, Any]) -> str:
    """Handle versions tool invocation via CLI.

    Args:
        arguments: Tool arguments containing:
            - project_dir: Path to project directory (required)
            - doc_type: Document type (manuscript/supplementary/revision)

    Returns:
        JSON string with list of document versions
    """
    project_dir = Path(arguments["project_dir"])
    doc_type = arguments.get("doc_type", "manuscript")

    if not project_dir.exists():
        return json.dumps(
            {"success": False, "error": f"Project directory not found: {project_dir}"}
        )

    cli_args = ["versions", str(project_dir), "-t", doc_type, "--json"]
    success, stdout, stderr = run_cli(cli_args)

    if success and stdout.strip():
        try:
            data = json.loads(stdout)
            return json.dumps({"success": True, "versions": data})
        except json.JSONDecodeError:
            pass

    return json.dumps(
        {
            "success": success,
            "output": stdout,
            "error": stderr if not success else None,
        }
    )


async def diff_handler(arguments: dict[str, Any]) -> str:
    """Handle diff tool invocation via CLI.

    Args:
        arguments: Tool arguments containing:
            - project_dir: Path to project directory (required)
            - doc_type: Document type (manuscript/supplementary/revision)
            - version1: First version (optional)
            - version2: Second version (optional)

    Returns:
        JSON string with diff content
    """
    project_dir = Path(arguments["project_dir"])
    doc_type = arguments.get("doc_type", "manuscript")
    version1 = arguments.get("version1")
    version2 = arguments.get("version2")

    if not project_dir.exists():
        return json.dumps(
            {"success": False, "error": f"Project directory not found: {project_dir}"}
        )

    cli_args = ["diff", str(project_dir), "-t", doc_type]
    if version1:
        cli_args.extend(["-v1", version1])
    if version2:
        cli_args.extend(["-v2", version2])

    success, stdout, stderr = run_cli(cli_args)

    return json.dumps(
        {
            "success": success,
            "diff": stdout if success else None,
            "error": stderr if not success else None,
        }
    )


__all__ = ["check_handler", "versions_handler", "diff_handler"]
