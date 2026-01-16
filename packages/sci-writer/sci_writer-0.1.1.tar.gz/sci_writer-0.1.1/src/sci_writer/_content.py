"""Content management for sci-writer LaTeX documents.

Provides CRUD operations for manuscript sections like abstract,
introduction, methods, results, discussion, etc.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Section:
    """Represents a manuscript section."""

    name: str
    content: str
    file_path: Path
    doc_type: str = "manuscript"


# Section configuration: name -> (filename, wrapper pattern)
SECTIONS = {
    "abstract": ("abstract.tex", r"\\begin\{abstract\}(.*?)\\end\{abstract\}"),
    "introduction": ("introduction.tex", None),
    "methods": ("methods.tex", None),
    "results": ("results.tex", None),
    "discussion": ("discussion.tex", None),
    "highlights": ("highlights.tex", None),
    "data_availability": ("data_availability.tex", None),
    "graphical_abstract": ("graphical_abstract.tex", None),
}

SHARED_FILES = {
    "title": "title.tex",
    "authors": "authors.tex",
    "keywords": "keywords.tex",
    "journal_name": "journal_name.tex",
}

DOC_DIRS = {
    "manuscript": "01_manuscript",
    "supplementary": "02_supplementary",
    "revision": "03_revision",
}


def get_section_path(
    project_dir: Path,
    section: str,
    doc_type: str = "manuscript",
) -> Optional[Path]:
    """Get the path to a section file."""
    if section in SHARED_FILES:
        return project_dir / "00_shared" / SHARED_FILES[section]

    if section not in SECTIONS:
        return None

    doc_dir = DOC_DIRS.get(doc_type)
    if not doc_dir:
        return None

    filename = SECTIONS[section][0]
    return project_dir / doc_dir / "contents" / filename


def read_section(
    project_dir: Path,
    section: str,
    doc_type: str = "manuscript",
) -> Optional[Section]:
    """Read a section from the manuscript.

    Args:
        project_dir: Path to the project directory
        section: Section name (abstract, introduction, methods, etc.)
        doc_type: Document type (manuscript, supplementary, revision)

    Returns:
        Section object with content, or None if not found
    """
    file_path = get_section_path(project_dir, section, doc_type)
    if not file_path or not file_path.exists():
        return None

    content = file_path.read_text(encoding="utf-8")

    # Extract content from wrapper if defined
    if section in SECTIONS:
        pattern = SECTIONS[section][1]
        if pattern:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                content = match.group(1).strip()

    return Section(
        name=section,
        content=content,
        file_path=file_path,
        doc_type=doc_type,
    )


def update_section(
    project_dir: Path,
    section: str,
    content: str,
    doc_type: str = "manuscript",
) -> bool:
    """Update a section in the manuscript.

    Args:
        project_dir: Path to the project directory
        section: Section name
        content: New content for the section
        doc_type: Document type

    Returns:
        True if successful, False otherwise
    """
    file_path = get_section_path(project_dir, section, doc_type)
    if not file_path:
        return False

    # If file exists and has wrapper, preserve it
    if file_path.exists() and section in SECTIONS:
        pattern = SECTIONS[section][1]
        if pattern:
            existing = file_path.read_text(encoding="utf-8")
            # Replace content inside wrapper
            new_content = re.sub(
                pattern,
                lambda m: m.group(0).replace(m.group(1), f"\n{content}\n"),
                existing,
                flags=re.DOTALL,
            )
            file_path.write_text(new_content, encoding="utf-8")
            return True

    # Write content directly
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return True


def create_section(
    project_dir: Path,
    section: str,
    content: str = "",
    doc_type: str = "manuscript",
    template: Optional[str] = None,
) -> bool:
    """Create a new section file.

    Args:
        project_dir: Path to the project directory
        section: Section name
        content: Initial content
        doc_type: Document type
        template: Optional template to use

    Returns:
        True if successful, False otherwise
    """
    file_path = get_section_path(project_dir, section, doc_type)
    if not file_path:
        return False

    if file_path.exists():
        return False  # Already exists

    # Use template or create default structure
    if template:
        file_content = template
    elif section == "abstract":
        file_content = f"""%% -*- coding: utf-8 -*-
\\begin{{abstract}}
  \\pdfbookmark[1]{{Abstract}}{{abstract}}

{content}

\\end{{abstract}}

%%%% EOF"""
    else:
        file_content = f"""%% -*- coding: utf-8 -*-
%% {section.replace("_", " ").title()}

{content}

%%%% EOF"""

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(file_content, encoding="utf-8")
    return True


def delete_section(
    project_dir: Path,
    section: str,
    doc_type: str = "manuscript",
) -> bool:
    """Delete a section file.

    Args:
        project_dir: Path to the project directory
        section: Section name
        doc_type: Document type

    Returns:
        True if successful, False otherwise
    """
    file_path = get_section_path(project_dir, section, doc_type)
    if not file_path or not file_path.exists():
        return False

    file_path.unlink()
    return True


def list_sections(
    project_dir: Path,
    doc_type: str = "manuscript",
) -> list[str]:
    """List available sections in a document.

    Args:
        project_dir: Path to the project directory
        doc_type: Document type

    Returns:
        List of section names that exist
    """
    sections = []

    for section in SECTIONS:
        path = get_section_path(project_dir, section, doc_type)
        if path and path.exists():
            sections.append(section)

    return sections


# Convenience functions for common operations
def read_abstract(project_dir: Path) -> Optional[str]:
    """Read the abstract content."""
    section = read_section(project_dir, "abstract")
    return section.content if section else None


def update_abstract(project_dir: Path, content: str) -> bool:
    """Update the abstract content."""
    return update_section(project_dir, "abstract", content)


def read_introduction(project_dir: Path) -> Optional[str]:
    """Read the introduction content."""
    section = read_section(project_dir, "introduction")
    return section.content if section else None


def update_introduction(project_dir: Path, content: str) -> bool:
    """Update the introduction content."""
    return update_section(project_dir, "introduction", content)


def read_methods(project_dir: Path) -> Optional[str]:
    """Read the methods content."""
    section = read_section(project_dir, "methods")
    return section.content if section else None


def update_methods(project_dir: Path, content: str) -> bool:
    """Update the methods content."""
    return update_section(project_dir, "methods", content)


def read_results(project_dir: Path) -> Optional[str]:
    """Read the results content."""
    section = read_section(project_dir, "results")
    return section.content if section else None


def update_results(project_dir: Path, content: str) -> bool:
    """Update the results content."""
    return update_section(project_dir, "results", content)


def read_discussion(project_dir: Path) -> Optional[str]:
    """Read the discussion content."""
    section = read_section(project_dir, "discussion")
    return section.content if section else None


def update_discussion(project_dir: Path, content: str) -> bool:
    """Update the discussion content."""
    return update_section(project_dir, "discussion", content)


def read_title(project_dir: Path) -> Optional[str]:
    """Read the title content."""
    section = read_section(project_dir, "title")
    return section.content if section else None


def update_title(project_dir: Path, content: str) -> bool:
    """Update the title content."""
    return update_section(project_dir, "title", content)


__all__ = [
    # Core functions
    "read_section",
    "update_section",
    "create_section",
    "delete_section",
    "list_sections",
    "get_section_path",
    # Section dataclass
    "Section",
    # Convenience functions
    "read_abstract",
    "update_abstract",
    "read_introduction",
    "update_introduction",
    "read_methods",
    "update_methods",
    "read_results",
    "update_results",
    "read_discussion",
    "update_discussion",
    "read_title",
    "update_title",
]
