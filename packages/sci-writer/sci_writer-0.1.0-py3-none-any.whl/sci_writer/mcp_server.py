#!/usr/bin/env python3
"""MCP Server for sci-writer - LaTeX Manuscript Compilation.

Provides tools for:
- Compiling LaTeX documents (manuscript, supplementary, revision)
- Checking project status and dependencies
- Cleaning compilation artifacts
- Getting project information
- Background job management for long-running compilations
"""

from __future__ import annotations

import asyncio

# Graceful MCP dependency handling
try:
    import mcp.types as types
    from mcp.server import NotificationOptions, Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    types = None  # type: ignore
    Server = None  # type: ignore
    NotificationOptions = None  # type: ignore
    InitializationOptions = None  # type: ignore
    stdio_server = None  # type: ignore

from sci_writer import __version__

__all__ = ["WriterServer", "main", "MCP_AVAILABLE"]


class WriterServer:
    """MCP Server for LaTeX Manuscript Compilation."""

    def __init__(self):
        self.server = Server("sci-writer")
        self.setup_handlers()

    def setup_handlers(self):
        """Set up MCP server handlers."""
        from sci_writer._mcp.handlers import (
            check_handler,
            clean_handler,
            compile_async_handler,
            compile_handler,
            diff_handler,
            figure_create_handler,
            figure_delete_handler,
            figure_get_handler,
            figure_update_handler,
            figures_handler,
            get_project_info_handler,
            job_cancel_handler,
            job_list_handler,
            job_result_handler,
            job_status_handler,
            list_sections_handler,
            outline_handler,
            read_sections_handler,
            refs_handler,
            status_handler,
            table_create_handler,
            table_delete_handler,
            table_get_handler,
            table_update_handler,
            tables_handler,
            update_section_handler,
            versions_handler,
            wordcount_handler,
        )
        from sci_writer._mcp.tool_schemas import get_tool_schemas

        @self.server.list_tools()
        async def handle_list_tools():
            return get_tool_schemas()

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            # Map tool names to handlers
            handlers = {
                "compile": compile_handler,
                "compile_async": compile_async_handler,
                "status": status_handler,
                "clean": clean_handler,
                "get_project_info": get_project_info_handler,
                "read_sections": read_sections_handler,
                "update_section": update_section_handler,
                "list_sections": list_sections_handler,
                "job_status": job_status_handler,
                "job_list": job_list_handler,
                "job_cancel": job_cancel_handler,
                "job_result": job_result_handler,
                # Document inspection
                "outline": outline_handler,
                "wordcount": wordcount_handler,
                "figures": figures_handler,
                "tables": tables_handler,
                "refs": refs_handler,
                # Validation and history
                "check": check_handler,
                "versions": versions_handler,
                "diff": diff_handler,
                # Figure CRUD
                "figure_get": figure_get_handler,
                "figure_create": figure_create_handler,
                "figure_update": figure_update_handler,
                "figure_delete": figure_delete_handler,
                # Table CRUD
                "table_get": table_get_handler,
                "table_create": table_create_handler,
                "table_update": table_update_handler,
                "table_delete": table_delete_handler,
            }

            handler = handlers.get(name)
            if handler:
                result = await handler(arguments)
                return self._make_result(result)
            else:
                raise ValueError(f"Unknown tool: {name}")

        @self.server.list_resources()
        async def handle_list_resources():
            """List available resources."""
            return [
                types.Resource(
                    uri="sci-writer://help",
                    name="sci-writer Help",
                    description="Usage information for sci-writer",
                    mimeType="text/plain",
                ),
            ]

        @self.server.read_resource()
        async def handle_read_resource(uri: str):
            """Read a resource."""
            if uri == "sci-writer://help":
                help_text = """sci-writer - LaTeX Manuscript Compilation System

Compilation:
  compile        - Compile LaTeX documents (manuscript, supplementary, revision)
  compile_async  - Start compilation as background job
  status         - Show project status and check dependencies
  clean          - Clean compilation artifacts

Content:
  read_sections  - Read one or more manuscript sections
  update_section - Update a manuscript section with new content
  list_sections  - List available sections in a manuscript

Document Inspection:
  outline        - Show document outline with word counts
  wordcount      - Show word counts for document or section
  figures        - List all figures with captions and media files
  tables         - List all tables with captions
  refs           - List all references (\\ref{}, \\cite{})

Figure Management:
  figure_get     - Get details of a specific figure
  figure_create  - Create a new figure with caption
  figure_update  - Update a figure's caption
  figure_delete  - Delete a figure and its files

Table Management:
  table_get      - Get details of a specific table
  table_create   - Create a new table with caption
  table_update   - Update a table's caption
  table_delete   - Delete a table and its files

Validation:
  check          - Validate document (undefined refs, missing media, etc.)
  versions       - List archived document versions
  diff           - View diff between document versions

Job Management:
  job_status     - Get status of a background job
  job_list       - List all background jobs
  job_cancel     - Cancel a running job
  job_result     - Get result of completed job

Usage:
  All tools require a project parameter pointing to a valid sci-writer project.
"""
                return types.TextResourceContents(
                    uri=uri,
                    mimeType="text/plain",
                    text=help_text,
                )
            else:
                raise ValueError(f"Unknown resource URI: {uri}")

    def _make_result(self, result: str) -> list:
        """Wrap handler result as MCP TextContent."""
        return [
            types.TextContent(
                type="text",
                text=result,
            )
        ]


async def _run_server():
    """Run the MCP server (internal)."""
    server = WriterServer()
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="sci-writer",
                server_version=__version__,
                capabilities=server.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    """Main entry point for the MCP server."""
    if not MCP_AVAILABLE:
        import sys

        print("=" * 60)
        print("MCP Server 'sci-writer' requires the 'mcp' package.")
        print()
        print("Install with:")
        print("  pip install mcp")
        print()
        print("Or install sci-writer with MCP support:")
        print("  pip install sci-writer[mcp]")
        print("=" * 60)
        sys.exit(1)

    asyncio.run(_run_server())


if __name__ == "__main__":
    main()
