"""CLI 'info' command group for document inspection.

Subcommands: outline, wordcount, figures, tables, refs
All commands delegate to Python modules - no original logic here.
"""

import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def _print_recursive_help(ctx, param, value):
    """Callback for --help-recursive flag."""
    if not value or ctx.resilient_parsing:
        return

    console.print("[bold cyan]━━━ sci-writer info ━━━[/bold cyan]")
    console.print(ctx.get_help())

    from sci_writer._cli.info_cmds import info as info_group

    for name, cmd in sorted(info_group.commands.items()):
        console.print(f"\n[bold cyan]━━━ sci-writer info {name} ━━━[/bold cyan]")
        sub_ctx = click.Context(cmd, info_name=name, parent=ctx)
        console.print(cmd.get_help(sub_ctx))

    ctx.exit(0)


def get_project_type():
    """Get the PROJECT type for click arguments."""
    from sci_writer._cli.main import PROJECT

    return PROJECT


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--help-recursive",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=_print_recursive_help,
    help="Show help for all subcommands.",
)
def info():
    """Inspect document content.

    \b
    Commands for examining manuscript structure

    \b
    Examples:
      sci-writer info outline .
      sci-writer info figures . --json
      sci-writer info wordcount . -s abstract
    """
    pass


@info.command(context_settings=CONTEXT_SETTINGS)
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
    Examples:
      sci-writer info outline .
      sci-writer info outline my-paper --json
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


@info.command(context_settings=CONTEXT_SETTINGS)
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
    Examples:
      sci-writer info wordcount .
      sci-writer info wordcount . -s abstract
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


@info.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project", type=get_project_type())
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["manuscript", "supplementary", "revision"]),
    default="manuscript",
    help="Document type",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def figures(project: Path, doc_type: str, as_json: bool):
    """List figures in a document.

    \b
    Examples:
      sci-writer info figures .
      sci-writer info figures my-paper --json
    """
    from sci_writer._media import list_figures

    figs = list_figures(project, doc_type)

    if as_json:
        data = [
            {
                "id": f.id,
                "label": f.label,
                "caption": f.caption,
                "media_files": [str(p) for p in f.media_files],
                "panels": f.panels,
            }
            for f in figs
        ]
        console.print(json.dumps(data, indent=2))
        return

    if not figs:
        console.print("[dim]No figures found[/dim]")
        return

    table = Table(title="Figures")
    table.add_column("ID", style="cyan")
    table.add_column("Label", style="green")
    table.add_column("Caption", max_width=50)
    table.add_column("Media", style="dim")

    for f in figs:
        caption = f.caption[:47] + "..." if len(f.caption) > 50 else f.caption
        media = ", ".join(p.name for p in f.media_files) or "[red]missing[/red]"
        table.add_row(f.id, f.label, caption, media)

    console.print(table)


@info.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project", type=get_project_type())
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["manuscript", "supplementary", "revision"]),
    default="manuscript",
    help="Document type",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def tables(project: Path, doc_type: str, as_json: bool):
    """List tables in a document.

    \b
    Examples:
      sci-writer info tables .
      sci-writer info tables my-paper --json
    """
    from sci_writer._media import list_tables

    tbls = list_tables(project, doc_type)

    if as_json:
        data = [{"id": t.id, "label": t.label, "caption": t.caption} for t in tbls]
        console.print(json.dumps(data, indent=2))
        return

    if not tbls:
        console.print("[dim]No tables found[/dim]")
        return

    table = Table(title="Tables")
    table.add_column("ID", style="cyan")
    table.add_column("Label", style="green")
    table.add_column("Caption", max_width=50)

    for t in tbls:
        caption = t.caption[:47] + "..." if len(t.caption) > 50 else t.caption
        table.add_row(t.id, t.label, caption)

    console.print(table)


@info.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project", type=get_project_type())
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["manuscript", "supplementary", "revision"]),
    default="manuscript",
    help="Document type",
)
@click.option(
    "--type",
    "ref_type",
    type=click.Choice(["figure", "table", "section", "equation", "citation"]),
    default=None,
    help="Filter by reference type",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def refs(project: Path, doc_type: str, ref_type: str, as_json: bool):
    """List references in the document.

    Shows all \\ref{} and \\cite{} commands found.

    \b
    Examples:
      sci-writer info refs .
      sci-writer info refs . --type figure
    """
    from sci_writer._media import find_references

    references = find_references(project, doc_type, ref_type)

    if as_json:
        data = [
            {
                "type": r.ref_type,
                "label": r.label,
                "file": str(r.file_path),
                "line": r.line_number,
            }
            for r in references
        ]
        console.print(json.dumps(data, indent=2))
        return

    if not references:
        console.print("[dim]No references found[/dim]")
        return

    table = Table(title="References")
    table.add_column("Type", style="cyan")
    table.add_column("Label", style="green")
    table.add_column("File", style="dim")
    table.add_column("Line", justify="right")

    for r in references:
        table.add_row(r.ref_type, r.label, r.file_path.name, str(r.line_number))

    console.print(table)


__all__ = ["info"]
