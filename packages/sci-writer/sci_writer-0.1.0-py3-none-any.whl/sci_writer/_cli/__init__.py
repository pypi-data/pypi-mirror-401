"""CLI module for sci-writer."""

from .jobs import jobs
from .main import main
from .mcp import mcp

__all__ = ["main", "mcp", "jobs"]
