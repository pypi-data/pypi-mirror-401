"""MCP handlers for content reading/writing operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


async def read_sections_handler(arguments: dict[str, Any]) -> str:
    """Handle read_sections tool invocation.

    Args:
        arguments: Tool arguments containing:
            - project_dir: Path to project directory (required)
            - sections: List of section names to read (required)
            - doc_type: Document type (manuscript/supplementary/revision)

    Returns:
        JSON string with section contents
    """
    from sci_writer._content import read_section

    project_dir = Path(arguments["project_dir"])
    sections = arguments.get("sections", [])
    doc_type = arguments.get("doc_type", "manuscript")

    if not project_dir.exists():
        return json.dumps(
            {
                "success": False,
                "error": f"Project directory not found: {project_dir}",
            }
        )

    results = {}
    for section_name in sections:
        section = read_section(project_dir, section_name, doc_type)
        if section:
            results[section_name] = {
                "content": section.content,
                "file_path": str(section.file_path),
            }
        else:
            results[section_name] = {"content": None, "error": "Section not found"}

    return json.dumps(
        {
            "success": True,
            "sections": results,
            "project_dir": str(project_dir),
            "doc_type": doc_type,
        }
    )


async def update_section_handler(arguments: dict[str, Any]) -> str:
    """Handle update_section tool invocation.

    Args:
        arguments: Tool arguments containing:
            - project_dir: Path to project directory (required)
            - section: Section name to update (required)
            - content: New content for the section (required)
            - doc_type: Document type (manuscript/supplementary/revision)

    Returns:
        JSON string with update result
    """
    from sci_writer._content import update_section

    project_dir = Path(arguments["project_dir"])
    section = arguments["section"]
    content = arguments["content"]
    doc_type = arguments.get("doc_type", "manuscript")

    if not project_dir.exists():
        return json.dumps(
            {
                "success": False,
                "error": f"Project directory not found: {project_dir}",
            }
        )

    success = update_section(project_dir, section, content, doc_type)

    return json.dumps(
        {
            "success": success,
            "section": section,
            "project_dir": str(project_dir),
            "doc_type": doc_type,
            "error": None if success else f"Failed to update section: {section}",
        }
    )


async def list_sections_handler(arguments: dict[str, Any]) -> str:
    """Handle list_sections tool invocation.

    Args:
        arguments: Tool arguments containing:
            - project_dir: Path to project directory (required)
            - doc_type: Document type (manuscript/supplementary/revision)

    Returns:
        JSON string with available sections
    """
    from sci_writer._content import list_sections

    project_dir = Path(arguments["project_dir"])
    doc_type = arguments.get("doc_type", "manuscript")

    if not project_dir.exists():
        return json.dumps(
            {
                "success": False,
                "error": f"Project directory not found: {project_dir}",
            }
        )

    sections = list_sections(project_dir, doc_type)

    return json.dumps(
        {
            "success": True,
            "sections": sections,
            "project_dir": str(project_dir),
            "doc_type": doc_type,
        }
    )


__all__ = ["read_sections_handler", "update_section_handler", "list_sections_handler"]
