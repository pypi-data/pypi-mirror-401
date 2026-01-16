"""MCP Tool schemas for document inspection operations."""

from __future__ import annotations

import mcp.types as types


def get_inspection_schemas() -> list[types.Tool]:
    """Return list of document inspection MCP tools."""
    return [
        types.Tool(
            name="outline",
            description="Show document outline with word counts per section",
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
            name="wordcount",
            description="Show word counts for document or specific section",
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
                    "section": {
                        "type": "string",
                        "description": "Specific section to count (optional)",
                    },
                },
                "required": ["project_dir"],
            },
        ),
        types.Tool(
            name="figures",
            description="List all figures in the document with captions and media files",
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
            name="tables",
            description="List all tables in the document with captions",
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
            name="refs",
            description=(
                "List all references (\\ref{}, \\cite{}) in the document. "
                "Useful for finding cross-references and citations."
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
                    "ref_type": {
                        "type": "string",
                        "description": "Filter by reference type",
                        "enum": ["figure", "table", "section", "equation", "citation"],
                    },
                },
                "required": ["project_dir"],
            },
        ),
    ]
