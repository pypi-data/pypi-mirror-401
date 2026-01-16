"""Media management for sci-writer LaTeX documents.

Provides CRUD operations for figures and tables:
- List, get, create, update, delete figures
- List, get, create, update, delete tables
- Find references and labels in documents
"""

from __future__ import annotations

from ._utils import DOC_DIRS, parse_caption_file
from .figures import (
    FigureInfo,
    create_figure,
    delete_figure,
    get_figure,
    list_figures,
    update_figure_caption,
)
from .references import Reference, find_labels, find_references
from .tables import (
    TableInfo,
    create_table,
    delete_table,
    get_table,
    list_tables,
    update_table_caption,
)

__all__ = [
    # Utils
    "DOC_DIRS",
    "parse_caption_file",
    # Figures
    "FigureInfo",
    "list_figures",
    "get_figure",
    "create_figure",
    "update_figure_caption",
    "delete_figure",
    # Tables
    "TableInfo",
    "list_tables",
    "get_table",
    "create_table",
    "update_table_caption",
    "delete_table",
    # References
    "Reference",
    "find_references",
    "find_labels",
]
