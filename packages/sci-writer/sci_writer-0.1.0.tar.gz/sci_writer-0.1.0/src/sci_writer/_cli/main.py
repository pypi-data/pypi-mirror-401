"""Command-line interface for sci-writer.

Thin wrapper that delegates to make/shell scripts.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console

console = Console()

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def _print_recursive_help(ctx, param, value):
    """Callback for --help-recursive flag."""
    if not value or ctx.resilient_parsing:
        return

    def _print_command_help(cmd, prefix: str, parent_ctx):
        """Recursively print help for a command and its subcommands."""
        console.print(f"\n[bold cyan]━━━ {prefix} ━━━[/bold cyan]")
        sub_ctx = click.Context(cmd, info_name=prefix.split()[-1], parent=parent_ctx)
        console.print(cmd.get_help(sub_ctx))

        if isinstance(cmd, click.Group):
            for sub_name, sub_cmd in sorted(cmd.commands.items()):
                _print_command_help(sub_cmd, f"{prefix} {sub_name}", sub_ctx)

    # Print main help
    console.print("[bold cyan]━━━ sci-writer ━━━[/bold cyan]")
    console.print(ctx.get_help())

    # Print all subcommands recursively
    from sci_writer._cli.main import main as main_group

    for name, cmd in sorted(main_group.commands.items()):
        _print_command_help(cmd, f"sci-writer {name}", ctx)

    ctx.exit(0)


class ProjectType(click.ParamType):
    """Custom Click type that accepts both paths and registered project names.

    Resolution order:
    1. If it's a path that exists, use it
    2. If it's a registered project name, resolve to that project's path
    3. Otherwise, fail with helpful error message
    """

    name = "project"

    def convert(self, value, param, ctx):
        if value is None:
            return None

        from sci_writer._project import resolve_project

        path = resolve_project(value)
        if path:
            return path

        self.fail(
            f"'{value}' is neither a valid path nor a registered project name.\n"
            "Use 'sci-writer list' to see registered projects.",
            param,
            ctx,
        )


PROJECT = ProjectType()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.option(
    "--help-recursive",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=_print_recursive_help,
    help="Show help for all commands recursively.",
)
@click.pass_context
def main(ctx):
    """sci-writer: LaTeX manuscript compilation system.

    A thin Python wrapper around shell scripts for compiling
    scientific LaTeX documents. Projects work independently
    with just 'make' or shell scripts.

    \b
    Quick start:
      sci-writer init my-paper .                      # Create new project
      sci-writer compile . manuscript                 # Compile current dir
      sci-writer compile my-paper manuscript          # Compile by name
      sci-writer status                               # Check all projects
    """
    pass


@main.command()
@click.argument("project", type=PROJECT)
@click.argument(
    "doc_type",
    type=click.Choice(["manuscript", "supplementary", "revision", "all"]),
)
@click.option("-q", "--quiet", is_flag=True, help="Suppress output")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed output")
@click.option("-nd", "--no-diff", is_flag=True, help="Skip diff generation")
@click.option("-nf", "--no-figs", is_flag=True, help="Skip figure processing")
@click.option("-nt", "--no-tables", is_flag=True, help="Skip table processing")
@click.option("-d", "--draft", is_flag=True, help="Single-pass (faster)")
@click.option("-dm", "--dark-mode", is_flag=True, help="Compile with dark theme")
@click.option("--crop-tif", is_flag=True, help="Crop TIF images")
@click.option("--timeout", type=int, default=300, help="Max time (seconds)")
def compile(
    project: Path,
    doc_type: str,
    quiet: bool,
    verbose: bool,
    no_diff: bool,
    no_figs: bool,
    no_tables: bool,
    draft: bool,
    dark_mode: bool,
    crop_tif: bool,
    timeout: int,
):
    """Compile LaTeX documents.

    \b
    PROJECT: Path or registered project name
    DOC_TYPE: manuscript | supplementary | revision | all

    \b
    Examples:
      sci-writer compile . manuscript           # Current directory
      sci-writer compile ./my-paper manuscript  # By path
      sci-writer compile my-paper manuscript    # By registered name
      sci-writer compile . all -q               # All docs, quiet
    """
    from sci_writer._compiler import compile_document

    if doc_type == "all":
        doc_types = ["manuscript", "supplementary", "revision"]
    else:
        doc_types = [doc_type]

    for dt in doc_types:
        if not quiet:
            console.print(f"[bold blue]Compiling {dt}...[/bold blue]")

        result = compile_document(
            doc_type=dt,
            project_dir=project,
            quiet=quiet,
            verbose=verbose,
            generate_diff=not no_diff,
            crop_tif=crop_tif,
            process_figures=not no_figs,
            process_tables=not no_tables,
            dark_mode=dark_mode,
            draft=draft,
            timeout=timeout,
        )

        if result.success:
            if not quiet:
                duration = f" ({result.duration:.1f}s)" if result.duration else ""
                console.print(
                    f"[bold green]Success:[/bold green] {result.output_path}{duration}"
                )
        else:
            console.print(f"[bold red]Failed:[/bold red] {result.error}")
            sys.exit(1)


@main.command()
@click.argument("projects", type=PROJECT, nargs=-1)
def status(projects: tuple[Path, ...]):
    """Show project status and check dependencies.

    \b
    PROJECTS: Paths or names (optional, multiple allowed)
              If omitted, shows all registered projects.

    \b
    Examples:
      sci-writer status                    # All registered
      sci-writer status .                  # Current directory
      sci-writer status my-paper           # By name
      sci-writer status ./p1 ./p2          # Multiple paths
    """
    from sci_writer._compiler import check_dependencies, get_project_info, get_status
    from sci_writer._project import list_projects

    def _show_project_status(proj_path: Path, name: str | None = None):
        if name:
            console.print(f"\n[bold cyan]━━━ {name} ━━━[/bold cyan]")
        console.print("[bold]Project Info[/bold]")
        info = get_project_info(proj_path)
        for key, value in info.items():
            status_str = "[green]✓[/green]" if value else "[red]✗[/red]"
            if isinstance(value, bool):
                console.print(f"  {key}: {status_str}")
            else:
                console.print(f"  {key}: {value}")

        console.print("\n[bold]PDF Status[/bold]")
        pdf_status = get_status(proj_path)
        for doc, exists in pdf_status.items():
            if doc != "make_output":
                status_str = "[green]✓[/green]" if exists else "[red]✗[/red]"
                console.print(f"  {doc}: {status_str}")

    if projects:
        for proj in projects:
            _show_project_status(proj)
    else:
        registered = list_projects()
        if not registered:
            console.print("[dim]No registered projects. Use 'sci-writer init'.[/dim]")
        else:
            for p in registered:
                proj_path = Path(p["path"])
                if proj_path.exists():
                    _show_project_status(proj_path, p["name"])

    console.print("\n[bold]Dependencies[/bold]")
    deps = check_dependencies()
    for name, available in deps.items():
        status_str = "[green]OK[/green]" if available else "[yellow]Missing[/yellow]"
        console.print(f"  {name}: {status_str}")


@main.command()
@click.argument("project", type=PROJECT)
def clean(project: Path):
    """Clean compilation artifacts.

    \b
    PROJECT: Path or registered project name

    \b
    Examples:
      sci-writer clean .              # Current directory
      sci-writer clean ./my-paper     # By path
      sci-writer clean my-paper       # By registered name
    """
    from sci_writer._compiler import clean_project

    clean_project(project)
    console.print("[green]Cleaned compilation artifacts[/green]")


@main.command()
@click.argument("name")
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.option("--description", default="", help="Project description")
def init(name: str, directory: Path, description: str):
    """Initialize a new sci-writer project.

    \b
    NAME: Project name (will create subdirectory)
    DIRECTORY: Parent directory for the project

    \b
    Examples:
      sci-writer init my-paper .
      sci-writer init my-paper ~/projects
    """
    from sci_writer._project import init_project

    success, message, project_path = init_project(
        name=name,
        target_dir=directory,
        description=description,
    )

    if success:
        console.print(f"[bold green]Created:[/bold green] {project_path}")
        console.print("\n[dim]Next steps:[/dim]")
        console.print(f"  cd {project_path}")
        console.print("  make manuscript")
    else:
        console.print(f"[bold red]Error:[/bold red] {message}")
        sys.exit(1)


@main.command("list")
def list_projects_cmd():
    """List registered projects."""
    from sci_writer._project import list_projects

    projects = list_projects()

    if not projects:
        console.print("[dim]No projects registered[/dim]")
        return

    console.print("[bold]Registered Projects[/bold]")
    for p in projects:
        marker = "[green]●[/green]" if p.get("is_active") else "[dim]○[/dim]"
        console.print(f"  {marker} {p['name']}: {p['path']}")


# Import and register command groups (use absolute to avoid circular import)
from sci_writer._cli.analysis_cmds import check, diff_cmd, versions  # noqa: E402
from sci_writer._cli.figure_cmds import figure as figure_group  # noqa: E402
from sci_writer._cli.info_cmds import info as info_group  # noqa: E402
from sci_writer._cli.jobs import jobs as jobs_group  # noqa: E402
from sci_writer._cli.mcp import mcp as mcp_group  # noqa: E402
from sci_writer._cli.table_cmds import table as table_group  # noqa: E402

main.add_command(mcp_group)
main.add_command(jobs_group)
main.add_command(info_group)
main.add_command(figure_group)
main.add_command(table_group)

# Keep frequently-used commands at top level
main.add_command(check)
main.add_command(versions)
main.add_command(diff_cmd, name="diff")


if __name__ == "__main__":
    main()
