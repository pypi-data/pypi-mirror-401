"""Version management and diff viewing for LaTeX documents."""

from __future__ import annotations

import difflib
import re
from pathlib import Path
from typing import Optional

DOC_DIRS = {
    "manuscript": "01_manuscript",
    "supplementary": "02_supplementary",
    "revision": "03_revision",
}


def view_diff(
    project_dir: Path,
    version1: Optional[str] = None,
    version2: Optional[str] = None,
    doc_type: str = "manuscript",
) -> Optional[str]:
    """View diff between document versions.

    Args:
        project_dir: Path to the project directory
        version1: First version (e.g., "v003") or None for previous
        version2: Second version or None for current
        doc_type: Document type

    Returns:
        Diff content or None if not available
    """
    doc_dir = DOC_DIRS.get(doc_type)
    if not doc_dir:
        return None

    archive_dir = project_dir / doc_dir / "archive"
    if not archive_dir.exists():
        return None

    # If no versions specified, get the most recent diff file
    if not version1 and not version2:
        diff_files = sorted(archive_dir.glob("*_diff.tex"), reverse=True)
        if diff_files:
            return diff_files[0].read_text(encoding="utf-8")
        return None

    # Get specific versions
    file1 = _resolve_version_file(archive_dir, version1, doc_type)
    if not file1:
        versions = sorted(archive_dir.glob("manuscript_v*.tex"))
        if len(versions) >= 2:
            file1 = versions[-2]
        else:
            return None

    file2 = _resolve_version_file(archive_dir, version2, doc_type)
    if not file2:
        file2 = project_dir / doc_dir / "manuscript.tex"

    if not file1.exists() or not file2.exists():
        return None

    content1 = file1.read_text(encoding="utf-8").splitlines()
    content2 = file2.read_text(encoding="utf-8").splitlines()

    diff = difflib.unified_diff(
        content1,
        content2,
        fromfile=file1.name,
        tofile=file2.name,
        lineterm="",
    )

    return "\n".join(diff)


def _resolve_version_file(
    archive_dir: Path,
    version: Optional[str],
    doc_type: str,
) -> Optional[Path]:
    """Resolve version string to file path."""
    if not version:
        return None

    candidates = [
        archive_dir / f"manuscript_{version}.tex",
        archive_dir / f"{doc_type}_{version}.tex",
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


def list_versions(
    project_dir: Path,
    doc_type: str = "manuscript",
) -> list[dict]:
    """List available document versions.

    Args:
        project_dir: Path to the project directory
        doc_type: Document type

    Returns:
        List of version info dicts with keys: version, file, modified, size, has_diff
    """
    doc_dir = DOC_DIRS.get(doc_type)
    if not doc_dir:
        return []

    archive_dir = project_dir / doc_dir / "archive"
    if not archive_dir.exists():
        return []

    versions = []
    for tex_file in sorted(archive_dir.glob("manuscript_v*.tex")):
        match = re.search(r"_v(\d+)\.tex$", tex_file.name)
        if match:
            version_num = match.group(1)
            stat = tex_file.stat()
            versions.append(
                {
                    "version": f"v{version_num}",
                    "file": str(tex_file),
                    "modified": stat.st_mtime,
                    "size": stat.st_size,
                    "has_diff": (
                        archive_dir / f"manuscript_v{version_num}_diff.tex"
                    ).exists(),
                }
            )

    return versions


__all__ = ["view_diff", "list_versions"]
