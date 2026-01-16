"""Document analysis for sci-writer LaTeX documents.

Provides analysis tools for writing assistance:
- Document outline with word counts
- Word count per section and total
- Document validation (broken refs, missing labels)
- Compile log parsing
- Version diff viewing
"""

from sci_writer._analysis.outline import OutlineItem, get_outline
from sci_writer._analysis.validation import (
    ValidationIssue,
    ValidationResult,
    check_document,
    get_compile_log,
    parse_compile_errors,
)
from sci_writer._analysis.versions import list_versions, view_diff
from sci_writer._analysis.wordcount import WordCountResult, get_word_count

__all__ = [
    # Outline
    "OutlineItem",
    "get_outline",
    # Word count
    "WordCountResult",
    "get_word_count",
    # Validation
    "ValidationIssue",
    "ValidationResult",
    "check_document",
    "get_compile_log",
    "parse_compile_errors",
    # Versions
    "list_versions",
    "view_diff",
]
