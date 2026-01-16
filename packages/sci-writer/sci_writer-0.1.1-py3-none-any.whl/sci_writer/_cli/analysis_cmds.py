"""CLI commands for document analysis (outline, wordcount, check, versions, diff).

All commands delegate to Python modules - no original logic here.
"""

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def get_project_type():
    """Get the PROJECT type for click arguments."""
    from sci_writer._cli.main import PROJECT

    return PROJECT


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project", type=get_project_type())
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["manuscript", "supplementary", "revision"]),
    default="manuscript",
    help="Document type",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def outline(project: Path, doc_type: str, as_json: bool):
    """Show document outline with word counts.

    \b
    PROJECT: Path or registered project name

    \b
    Examples:
      sci-writer outline .
      sci-writer outline my-paper --json
    """
    from sci_writer._analysis import get_outline

    items = get_outline(project, doc_type)

    if as_json:
        data = [
            {
                "name": item.name,
                "level": item.level,
                "word_count": item.word_count,
                "char_count": item.char_count,
            }
            for item in items
        ]
        console.print(json.dumps(data, indent=2))
        return

    if not items:
        console.print("[dim]No sections found[/dim]")
        return

    table = Table(title="Document Outline")
    table.add_column("Section", style="cyan")
    table.add_column("Words", justify="right", style="green")
    table.add_column("Chars", justify="right", style="dim")

    total_words = 0
    total_chars = 0
    for item in items:
        table.add_row(item.name, str(item.word_count), str(item.char_count))
        total_words += item.word_count
        total_chars += item.char_count

    table.add_section()
    table.add_row("[bold]Total[/bold]", f"[bold]{total_words}[/bold]", str(total_chars))

    console.print(table)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project", type=get_project_type())
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["manuscript", "supplementary", "revision"]),
    default="manuscript",
    help="Document type",
)
@click.option("-s", "--section", default=None, help="Specific section to count")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def wordcount(project: Path, doc_type: str, section: str, as_json: bool):
    """Show word counts for document or section.

    \b
    PROJECT: Path or registered project name

    \b
    Examples:
      sci-writer wordcount .
      sci-writer wordcount . -s abstract
      sci-writer wordcount my-paper --json
    """
    from sci_writer._analysis import get_word_count

    result = get_word_count(project, doc_type, section)

    if as_json:
        data = {
            "total_words": result.total_words,
            "total_chars": result.total_chars,
            "total_chars_no_spaces": result.total_chars_no_spaces,
            "sections": result.sections,
        }
        console.print(json.dumps(data, indent=2))
        return

    console.print(f"[bold]Total words:[/bold] {result.total_words}")
    console.print(f"[bold]Total chars:[/bold] {result.total_chars}")

    if result.sections:
        console.print("\n[bold]By section:[/bold]")
        for sec, count in result.sections.items():
            if count > 0:
                console.print(f"  {sec}: {count}")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project", type=get_project_type())
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["manuscript", "supplementary", "revision"]),
    default="manuscript",
    help="Document type",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def check(project: Path, doc_type: str, as_json: bool):
    """Validate document for common issues.

    Checks for:
    - Undefined references
    - Unused labels
    - Missing figure media
    - Duplicate labels

    \b
    PROJECT: Path or registered project name

    \b
    Examples:
      sci-writer check .
      sci-writer check my-paper --json
    """
    from sci_writer._analysis import check_document

    result = check_document(project, doc_type)

    if as_json:
        data = {
            "is_valid": result.is_valid,
            "summary": result.summary,
            "issues": [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "message": i.message,
                    "file": str(i.file_path) if i.file_path else None,
                    "line": i.line_number,
                    "suggestion": i.suggestion,
                }
                for i in result.issues
            ],
        }
        console.print(json.dumps(data, indent=2))
        return

    if result.is_valid:
        console.print("[bold green]✓ Document is valid[/bold green]")
    else:
        console.print("[bold red]✗ Document has issues[/bold red]")

    console.print(
        f"  Errors: {result.summary.get('error', 0)}, "
        f"Warnings: {result.summary.get('warning', 0)}"
    )

    if result.issues:
        console.print("\n[bold]Issues:[/bold]")
        for issue in result.issues:
            if issue.severity == "error":
                icon = "[red]✗[/red]"
            elif issue.severity == "warning":
                icon = "[yellow]![/yellow]"
            else:
                icon = "[dim]i[/dim]"

            loc = ""
            if issue.file_path:
                loc = f" ({issue.file_path.name}"
                if issue.line_number:
                    loc += f":{issue.line_number}"
                loc += ")"

            console.print(f"  {icon} [{issue.category}] {issue.message}{loc}")

    if not result.is_valid:
        sys.exit(1)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project", type=get_project_type())
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["manuscript", "supplementary", "revision"]),
    default="manuscript",
    help="Document type",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def versions(project: Path, doc_type: str, as_json: bool):
    """List document versions.

    \b
    PROJECT: Path or registered project name

    \b
    Examples:
      sci-writer versions .
      sci-writer versions my-paper --json
    """
    from sci_writer._analysis import list_versions

    vers = list_versions(project, doc_type)

    if as_json:
        console.print(json.dumps(vers, indent=2))
        return

    if not vers:
        console.print("[dim]No versions found[/dim]")
        return

    table = Table(title="Document Versions")
    table.add_column("Version", style="cyan")
    table.add_column("Has Diff", style="green")
    table.add_column("Size", justify="right", style="dim")

    for v in vers:
        diff_str = "✓" if v["has_diff"] else ""
        size_str = f"{v['size'] // 1024}KB"
        table.add_row(v["version"], diff_str, size_str)

    console.print(table)


@click.command("diff", context_settings=CONTEXT_SETTINGS)
@click.argument("project", type=get_project_type())
@click.option("-v1", "--version1", default=None, help="First version (e.g., v003)")
@click.option(
    "-v2", "--version2", default=None, help="Second version (default: current)"
)
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["manuscript", "supplementary", "revision"]),
    default="manuscript",
    help="Document type",
)
def diff_cmd(project: Path, version1: str, version2: str, doc_type: str):
    """View diff between document versions.

    \b
    PROJECT: Path or registered project name

    \b
    Examples:
      sci-writer diff .                     # Latest diff
      sci-writer diff . -v1 v003 -v2 v004   # Between versions
    """
    from sci_writer._analysis import view_diff

    diff_content = view_diff(project, version1, version2, doc_type)

    if not diff_content:
        console.print("[dim]No diff available[/dim]")
        return

    for line in diff_content.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            console.print(f"[green]{line}[/green]")
        elif line.startswith("-") and not line.startswith("---"):
            console.print(f"[red]{line}[/red]")
        elif line.startswith("@@"):
            console.print(f"[cyan]{line}[/cyan]")
        else:
            console.print(line)


__all__ = ["outline", "wordcount", "check", "versions", "diff_cmd"]
