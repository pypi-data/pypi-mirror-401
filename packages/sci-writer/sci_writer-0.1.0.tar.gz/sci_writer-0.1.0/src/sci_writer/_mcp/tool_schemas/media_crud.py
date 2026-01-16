"""Tool schemas for figure and table CRUD operations."""

from __future__ import annotations

import mcp.types as types

DOC_TYPE_ENUM = ["manuscript", "supplementary", "revision"]


def get_media_crud_schemas() -> list[types.Tool]:
    """Return schemas for figure and table CRUD tools."""
    return [
        # Figure CRUD
        types.Tool(
            name="figure_get",
            description="Get details of a specific figure (caption, label, media files)",
            inputSchema={
                "type": "object",
                "required": ["project", "figure_id"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project path or registered name",
                    },
                    "figure_id": {
                        "type": "string",
                        "description": "Figure ID (e.g., '01' or '01_example')",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": DOC_TYPE_ENUM,
                        "default": "manuscript",
                        "description": "Document type",
                    },
                },
            },
        ),
        types.Tool(
            name="figure_create",
            description="Create a new figure with caption",
            inputSchema={
                "type": "object",
                "required": ["project", "figure_id", "caption"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project path or registered name",
                    },
                    "figure_id": {
                        "type": "string",
                        "description": "Figure ID (e.g., '03_new_figure')",
                    },
                    "caption": {
                        "type": "string",
                        "description": "Figure caption text",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": DOC_TYPE_ENUM,
                        "default": "manuscript",
                        "description": "Document type",
                    },
                },
            },
        ),
        types.Tool(
            name="figure_update",
            description="Update a figure's caption",
            inputSchema={
                "type": "object",
                "required": ["project", "figure_id", "caption"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project path or registered name",
                    },
                    "figure_id": {
                        "type": "string",
                        "description": "Figure ID (e.g., '01' or '01_example')",
                    },
                    "caption": {
                        "type": "string",
                        "description": "New caption text",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": DOC_TYPE_ENUM,
                        "default": "manuscript",
                        "description": "Document type",
                    },
                },
            },
        ),
        types.Tool(
            name="figure_delete",
            description="Delete a figure and its associated files",
            inputSchema={
                "type": "object",
                "required": ["project", "figure_id"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project path or registered name",
                    },
                    "figure_id": {
                        "type": "string",
                        "description": "Figure ID (e.g., '01' or '01_example')",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": DOC_TYPE_ENUM,
                        "default": "manuscript",
                        "description": "Document type",
                    },
                },
            },
        ),
        # Table CRUD
        types.Tool(
            name="table_get",
            description="Get details of a specific table (caption, label)",
            inputSchema={
                "type": "object",
                "required": ["project", "table_id"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project path or registered name",
                    },
                    "table_id": {
                        "type": "string",
                        "description": "Table ID (e.g., '01' or '01_example')",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": DOC_TYPE_ENUM,
                        "default": "manuscript",
                        "description": "Document type",
                    },
                },
            },
        ),
        types.Tool(
            name="table_create",
            description="Create a new table with caption",
            inputSchema={
                "type": "object",
                "required": ["project", "table_id", "caption"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project path or registered name",
                    },
                    "table_id": {
                        "type": "string",
                        "description": "Table ID (e.g., '03_new_table')",
                    },
                    "caption": {
                        "type": "string",
                        "description": "Table caption text",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": DOC_TYPE_ENUM,
                        "default": "manuscript",
                        "description": "Document type",
                    },
                },
            },
        ),
        types.Tool(
            name="table_update",
            description="Update a table's caption",
            inputSchema={
                "type": "object",
                "required": ["project", "table_id", "caption"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project path or registered name",
                    },
                    "table_id": {
                        "type": "string",
                        "description": "Table ID (e.g., '01' or '01_example')",
                    },
                    "caption": {
                        "type": "string",
                        "description": "New caption text",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": DOC_TYPE_ENUM,
                        "default": "manuscript",
                        "description": "Document type",
                    },
                },
            },
        ),
        types.Tool(
            name="table_delete",
            description="Delete a table and its associated files",
            inputSchema={
                "type": "object",
                "required": ["project", "table_id"],
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project path or registered name",
                    },
                    "table_id": {
                        "type": "string",
                        "description": "Table ID (e.g., '01' or '01_example')",
                    },
                    "doc_type": {
                        "type": "string",
                        "enum": DOC_TYPE_ENUM,
                        "default": "manuscript",
                        "description": "Document type",
                    },
                },
            },
        ),
    ]


__all__ = ["get_media_crud_schemas"]
