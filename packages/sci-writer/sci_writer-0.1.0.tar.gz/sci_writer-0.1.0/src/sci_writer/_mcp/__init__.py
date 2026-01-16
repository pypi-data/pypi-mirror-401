"""MCP server components for sci-writer."""

from .handlers import (
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
from .tool_schemas import get_tool_schemas

__all__ = [
    "get_tool_schemas",
    # Compile
    "compile_handler",
    # Project
    "status_handler",
    "clean_handler",
    "get_project_info_handler",
    # Content
    "read_sections_handler",
    "update_section_handler",
    "list_sections_handler",
    # Jobs
    "compile_async_handler",
    "job_status_handler",
    "job_list_handler",
    "job_cancel_handler",
    "job_result_handler",
    # Inspection
    "outline_handler",
    "wordcount_handler",
    "figures_handler",
    "tables_handler",
    "refs_handler",
    # Validation
    "check_handler",
    "versions_handler",
    "diff_handler",
    # Media CRUD
    "figure_get_handler",
    "figure_create_handler",
    "figure_update_handler",
    "figure_delete_handler",
    "table_get_handler",
    "table_create_handler",
    "table_update_handler",
    "table_delete_handler",
]
