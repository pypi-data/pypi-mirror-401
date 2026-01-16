"""MCP Tool schemas for validation and history operations."""

from __future__ import annotations

import mcp.types as types


def get_validation_schemas() -> list[types.Tool]:
    """Return list of validation and history MCP tools."""
    return [
        types.Tool(
            name="check",
            description=(
                "Validate document for common issues: undefined references, "
                "unused labels, missing figure media, duplicate labels"
            ),
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
        types.Tool(
            name="versions",
            description="List all archived document versions",
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
        types.Tool(
            name="diff",
            description="View diff between document versions",
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
                    "version1": {
                        "type": "string",
                        "description": "First version (e.g., v003)",
                    },
                    "version2": {
                        "type": "string",
                        "description": "Second version (default: current)",
                    },
                },
                "required": ["project_dir"],
            },
        ),
    ]
