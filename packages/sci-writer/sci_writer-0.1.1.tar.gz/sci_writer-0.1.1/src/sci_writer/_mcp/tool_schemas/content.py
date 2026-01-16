"""MCP Tool schemas for content reading/writing operations."""

from __future__ import annotations

import mcp.types as types


def get_content_schemas() -> list[types.Tool]:
    """Return list of content management MCP tools."""
    return [
        types.Tool(
            name="read_sections",
            description=(
                "Read one or more manuscript sections "
                "(abstract, introduction, methods, results, discussion, etc.)"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "project_dir": {
                        "type": "string",
                        "description": "Path to the project directory",
                    },
                    "sections": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Section names to read (e.g., ['abstract', 'introduction'])",
                    },
                    "doc_type": {
                        "type": "string",
                        "description": "Document type (manuscript, supplementary, revision)",
                        "enum": ["manuscript", "supplementary", "revision"],
                        "default": "manuscript",
                    },
                },
                "required": ["project_dir", "sections"],
            },
        ),
        types.Tool(
            name="update_section",
            description="Update a manuscript section with new content",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_dir": {
                        "type": "string",
                        "description": "Path to the project directory",
                    },
                    "section": {
                        "type": "string",
                        "description": "Section name to update",
                    },
                    "content": {
                        "type": "string",
                        "description": "New content for the section",
                    },
                    "doc_type": {
                        "type": "string",
                        "description": "Document type",
                        "enum": ["manuscript", "supplementary", "revision"],
                        "default": "manuscript",
                    },
                },
                "required": ["project_dir", "section", "content"],
            },
        ),
        types.Tool(
            name="list_sections",
            description="List available sections in a manuscript",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_dir": {
                        "type": "string",
                        "description": "Path to the project directory",
                    },
                    "doc_type": {
                        "type": "string",
                        "description": "Document type",
                        "enum": ["manuscript", "supplementary", "revision"],
                        "default": "manuscript",
                    },
                },
                "required": ["project_dir"],
            },
        ),
    ]
