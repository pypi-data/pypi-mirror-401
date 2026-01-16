"""
sci-writer: LaTeX manuscript compilation system for scientific documents.

Usage:
    from sci_writer import compile_manuscript, compile_supplementary

    # Compile manuscript
    result = compile_manuscript("path/to/project")

    # Or use CLI
    # $ sci-writer compile manuscript
"""

from sci_writer._compiler import (
    compile_manuscript,
    compile_revision,
    compile_supplementary,
)

__version__ = "0.1.0"
__all__ = [
    "compile_manuscript",
    "compile_supplementary",
    "compile_revision",
    "__version__",
]
