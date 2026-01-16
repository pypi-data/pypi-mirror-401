"""MCP handlers for sci-writer tools.

Each handler delegates to CLI commands to maintain consistent behavior.
"""

from .compile import compile_handler
from .content import (
    list_sections_handler,
    read_sections_handler,
    update_section_handler,
)
from .inspection import (
    figures_handler,
    outline_handler,
    refs_handler,
    tables_handler,
    wordcount_handler,
)
from .jobs import (
    compile_async_handler,
    job_cancel_handler,
    job_list_handler,
    job_result_handler,
    job_status_handler,
)
from .media_crud import (
    figure_create_handler,
    figure_delete_handler,
    figure_get_handler,
    figure_update_handler,
    table_create_handler,
    table_delete_handler,
    table_get_handler,
    table_update_handler,
)
from .project import clean_handler, get_project_info_handler, status_handler
from .validation import check_handler, diff_handler, versions_handler

__all__ = [
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
