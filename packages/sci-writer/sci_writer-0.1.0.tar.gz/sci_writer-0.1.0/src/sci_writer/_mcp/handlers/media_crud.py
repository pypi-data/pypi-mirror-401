"""MCP handlers for figure and table CRUD operations.

Each handler delegates to CLI commands to maintain consistent behavior.
"""

from ._utils import run_cli


async def figure_get_handler(arguments: dict) -> str:
    """Handle figure get request."""
    project = arguments.get("project", ".")
    figure_id = arguments.get("figure_id", "")
    doc_type = arguments.get("doc_type", "manuscript")

    return await run_cli(
        ["figure", "get", project, figure_id, "-t", doc_type, "--json"]
    )


async def figure_create_handler(arguments: dict) -> str:
    """Handle figure create request."""
    project = arguments.get("project", ".")
    figure_id = arguments.get("figure_id", "")
    caption = arguments.get("caption", "")
    doc_type = arguments.get("doc_type", "manuscript")

    return await run_cli(
        ["figure", "create", project, figure_id, "-c", caption, "-t", doc_type]
    )


async def figure_update_handler(arguments: dict) -> str:
    """Handle figure update request."""
    project = arguments.get("project", ".")
    figure_id = arguments.get("figure_id", "")
    caption = arguments.get("caption", "")
    doc_type = arguments.get("doc_type", "manuscript")

    return await run_cli(
        ["figure", "update", project, figure_id, "-c", caption, "-t", doc_type]
    )


async def figure_delete_handler(arguments: dict) -> str:
    """Handle figure delete request."""
    project = arguments.get("project", ".")
    figure_id = arguments.get("figure_id", "")
    doc_type = arguments.get("doc_type", "manuscript")

    return await run_cli(
        ["figure", "delete", project, figure_id, "-t", doc_type, "--force"]
    )


async def table_get_handler(arguments: dict) -> str:
    """Handle table get request."""
    project = arguments.get("project", ".")
    table_id = arguments.get("table_id", "")
    doc_type = arguments.get("doc_type", "manuscript")

    return await run_cli(["table", "get", project, table_id, "-t", doc_type, "--json"])


async def table_create_handler(arguments: dict) -> str:
    """Handle table create request."""
    project = arguments.get("project", ".")
    table_id = arguments.get("table_id", "")
    caption = arguments.get("caption", "")
    doc_type = arguments.get("doc_type", "manuscript")

    return await run_cli(
        ["table", "create", project, table_id, "-c", caption, "-t", doc_type]
    )


async def table_update_handler(arguments: dict) -> str:
    """Handle table update request."""
    project = arguments.get("project", ".")
    table_id = arguments.get("table_id", "")
    caption = arguments.get("caption", "")
    doc_type = arguments.get("doc_type", "manuscript")

    return await run_cli(
        ["table", "update", project, table_id, "-c", caption, "-t", doc_type]
    )


async def table_delete_handler(arguments: dict) -> str:
    """Handle table delete request."""
    project = arguments.get("project", ".")
    table_id = arguments.get("table_id", "")
    doc_type = arguments.get("doc_type", "manuscript")

    return await run_cli(
        ["table", "delete", project, table_id, "-t", doc_type, "--force"]
    )


__all__ = [
    "figure_get_handler",
    "figure_create_handler",
    "figure_update_handler",
    "figure_delete_handler",
    "table_get_handler",
    "table_create_handler",
    "table_update_handler",
    "table_delete_handler",
]
