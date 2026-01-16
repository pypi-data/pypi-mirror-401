"""MCP Tool schemas for sci-writer.

Defines available tools for LaTeX manuscript management.
"""

from __future__ import annotations

import mcp.types as types

from .compile import get_compile_schemas
from .content import get_content_schemas
from .inspection import get_inspection_schemas
from .jobs import get_jobs_schemas
from .media_crud import get_media_crud_schemas
from .project import get_project_schemas
from .validation import get_validation_schemas


def get_tool_schemas() -> list[types.Tool]:
    """Return list of all available MCP tools for sci-writer."""
    return [
        *get_compile_schemas(),
        *get_project_schemas(),
        *get_content_schemas(),
        *get_jobs_schemas(),
        *get_inspection_schemas(),
        *get_validation_schemas(),
        *get_media_crud_schemas(),
    ]


__all__ = ["get_tool_schemas"]
