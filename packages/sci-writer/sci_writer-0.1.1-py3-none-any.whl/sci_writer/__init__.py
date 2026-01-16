"""
sci-writer: LaTeX manuscript compilation system for scientific documents.

Usage:
    from sci_writer import compile_manuscript, compile_supplementary

    # Compile manuscript
    result = compile_manuscript("path/to/project")

    # Or use CLI
    # $ sci-writer compile manuscript
"""

from importlib.metadata import version

from sci_writer._compiler import (
    compile_manuscript,
    compile_revision,
    compile_supplementary,
)

__version__ = version("sci-writer")
__all__ = [
    "compile_manuscript",
    "compile_supplementary",
    "compile_revision",
    "__version__",
]
