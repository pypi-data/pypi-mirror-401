"""MCP Tool schemas for background job management."""

from __future__ import annotations

import mcp.types as types


def get_jobs_schemas() -> list[types.Tool]:
    """Return list of job management MCP tools."""
    return [
        types.Tool(
            name="compile_async",
            description=(
                "Start compilation as a background job. Returns immediately with a "
                "job_id. Use job_status to check progress and job_result to get output."
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
                        "description": "Type of document to compile",
                        "enum": ["manuscript", "supplementary", "revision", "all"],
                        "default": "manuscript",
                    },
                    "quiet": {
                        "type": "boolean",
                        "description": "Suppress output",
                        "default": True,
                    },
                    "no_diff": {
                        "type": "boolean",
                        "description": "Skip diff generation",
                        "default": False,
                    },
                    "no_figs": {
                        "type": "boolean",
                        "description": "Skip figure processing",
                        "default": False,
                    },
                    "draft": {
                        "type": "boolean",
                        "description": "Single-pass compilation (faster)",
                        "default": False,
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Maximum compilation time in seconds",
                        "default": 300,
                    },
                },
                "required": ["project_dir"],
            },
        ),
        types.Tool(
            name="job_status",
            description="Get the status of a background job",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "Job ID returned from compile_async",
                    },
                },
                "required": ["job_id"],
            },
        ),
        types.Tool(
            name="job_list",
            description="List all background jobs",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status",
                        "enum": [
                            "pending",
                            "running",
                            "completed",
                            "failed",
                            "cancelled",
                        ],
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of jobs to return",
                        "default": 20,
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="job_cancel",
            description="Cancel a running background job",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "Job ID to cancel",
                    },
                },
                "required": ["job_id"],
            },
        ),
        types.Tool(
            name="job_result",
            description="Get the result of a completed job",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "Job ID to get result for",
                    },
                },
                "required": ["job_id"],
            },
        ),
    ]
