"""MCP handlers for compilation operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ._utils import run_cli


async def compile_handler(arguments: dict[str, Any]) -> str:
    """Handle compile tool invocation via CLI.

    Args:
        arguments: Tool arguments containing:
            - project_dir: Path to project directory (required)
            - doc_type: Document type (manuscript/supplementary/revision/all)
            - quiet: Suppress output
            - no_diff: Skip diff generation
            - no_figs: Skip figure processing
            - no_tables: Skip table processing
            - draft: Single-pass compilation
            - dark_mode: Dark theme
            - engine: Compilation engine (auto/tectonic/latexmk/3pass)
            - timeout: Maximum compilation time

    Returns:
        JSON string with compilation result
    """
    project_dir = Path(arguments["project_dir"])
    doc_type = arguments.get("doc_type", "manuscript")
    timeout = arguments.get("timeout", 300)

    if not project_dir.exists():
        return json.dumps(
            {
                "success": False,
                "error": f"Project directory not found: {project_dir}",
            }
        )

    # Build CLI arguments: compile PROJECT DOC_TYPE
    cli_args = ["compile", str(project_dir), doc_type]

    if arguments.get("quiet", False):
        cli_args.append("-q")
    if arguments.get("verbose", False):
        cli_args.append("-v")
    if arguments.get("no_diff", False):
        cli_args.append("--no-diff")
    if arguments.get("no_figs", False):
        cli_args.append("--no-figs")
    if arguments.get("no_tables", False):
        cli_args.append("--no-tables")
    if arguments.get("draft", False):
        cli_args.append("--draft")
    if arguments.get("dark_mode", False):
        cli_args.append("--dark-mode")
    if arguments.get("crop_tif", False):
        cli_args.append("--crop-tif")
    if "engine" in arguments:
        cli_args.extend(["-e", arguments["engine"]])
    if "timeout" in arguments:
        cli_args.extend(["--timeout", str(arguments["timeout"])])

    success, stdout, stderr = run_cli(cli_args, timeout=timeout + 30)

    return json.dumps(
        {
            "success": success,
            "output": stdout,
            "error": stderr if not success else None,
            "project_dir": str(project_dir),
            "doc_type": doc_type,
        }
    )


__all__ = ["compile_handler"]
