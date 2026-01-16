"""Jobs subcommands for sci-writer CLI."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

console = Console()


def _print_recursive_help(ctx, param, value):
    """Callback for --help-recursive flag."""
    if not value or ctx.resilient_parsing:
        return

    console.print("[bold cyan]━━━ sci-writer jobs ━━━[/bold cyan]")
    console.print(ctx.get_help())

    from sci_writer._cli.jobs import jobs as jobs_group

    for name, cmd in sorted(jobs_group.commands.items()):
        console.print(f"\n[bold cyan]━━━ sci-writer jobs {name} ━━━[/bold cyan]")
        sub_ctx = click.Context(cmd, info_name=name, parent=ctx)
        console.print(cmd.get_help(sub_ctx))

    ctx.exit(0)


@click.group()
@click.option(
    "--help-recursive",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=_print_recursive_help,
    help="Show help for all subcommands.",
)
def jobs():
    """Manage background compilation jobs.

    \b
    Long-running compilations can be started as background jobs.
    Use these commands to monitor and manage them.

    \b
    Examples:
      sci-writer jobs list                    # List all jobs
      sci-writer jobs status <job_id>         # Check job status
      sci-writer jobs cancel <job_id>         # Cancel a running job
      sci-writer jobs result <job_id>         # Get job result
    """
    pass


@jobs.command("list")
@click.option(
    "-s",
    "--status",
    type=click.Choice(["pending", "running", "completed", "failed", "cancelled"]),
    help="Filter by status",
)
@click.option("-n", "--limit", type=int, default=20, help="Max jobs to show")
def jobs_list(status: str | None, limit: int):
    """List background jobs.

    \b
    Examples:
      sci-writer jobs list                    # All jobs
      sci-writer jobs list -s running         # Only running
      sci-writer jobs list -n 5               # Last 5 jobs
    """
    from sci_writer._jobs import JobStatus, job_manager

    status_filter = JobStatus(status) if status else None
    jobs_list = job_manager.list_jobs(status=status_filter, limit=limit)

    if not jobs_list:
        console.print("[dim]No jobs found[/dim]")
        return

    table = Table(title="Background Jobs")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Type", style="blue")
    table.add_column("Status", style="bold")
    table.add_column("Created", style="dim")
    table.add_column("Project", style="green")

    for job in jobs_list:
        status_style = {
            "pending": "yellow",
            "running": "blue",
            "completed": "green",
            "failed": "red",
            "cancelled": "dim",
        }.get(job.status.value, "white")

        project = job.arguments.get("project_dir", "")
        if project:
            project = project.split("/")[-1]  # Just show dir name

        table.add_row(
            job.id[:8],  # Short ID
            job.job_type,
            f"[{status_style}]{job.status.value}[/{status_style}]",
            job.created_at.strftime("%H:%M:%S") if job.created_at else "-",
            project,
        )

    console.print(table)


@jobs.command("status")
@click.argument("job_id")
def jobs_status(job_id: str):
    """Show status of a specific job.

    \b
    JOB_ID: Job ID (can use short form, e.g., first 8 chars)

    \b
    Examples:
      sci-writer jobs status abc12345
      sci-writer jobs status abc12345-6789-...
    """
    from sci_writer._jobs import job_manager

    job = job_manager.get_job(job_id)

    if not job:
        # Try prefix match
        all_jobs = job_manager.list_jobs(limit=100)
        matches = [j for j in all_jobs if j.id.startswith(job_id)]
        if len(matches) == 1:
            job = matches[0]
        elif len(matches) > 1:
            console.print(f"[yellow]Multiple jobs match '{job_id}':[/yellow]")
            for j in matches:
                console.print(f"  {j.id}")
            return
        else:
            console.print(f"[red]Job not found:[/red] {job_id}")
            return

    status_style = {
        "pending": "yellow",
        "running": "blue",
        "completed": "green",
        "failed": "red",
        "cancelled": "dim",
    }.get(job.status.value, "white")

    console.print(f"[bold]Job ID:[/bold] {job.id}")
    console.print(f"[bold]Type:[/bold] {job.job_type}")
    console.print(
        f"[bold]Status:[/bold] [{status_style}]{job.status.value}[/{status_style}]"
    )
    console.print(f"[bold]Created:[/bold] {job.created_at}")

    if job.started_at:
        console.print(f"[bold]Started:[/bold] {job.started_at}")
    if job.completed_at:
        console.print(f"[bold]Completed:[/bold] {job.completed_at}")

    if job.arguments:
        console.print("[bold]Arguments:[/bold]")
        for key, value in job.arguments.items():
            console.print(f"  {key}: {value}")

    if job.error:
        console.print(f"[bold red]Error:[/bold red] {job.error}")


@jobs.command("cancel")
@click.argument("job_id")
def jobs_cancel(job_id: str):
    """Cancel a running job.

    \b
    JOB_ID: Job ID to cancel

    \b
    Examples:
      sci-writer jobs cancel abc12345
    """
    from sci_writer._jobs import job_manager

    # Try prefix match
    job = job_manager.get_job(job_id)
    if not job:
        all_jobs = job_manager.list_jobs(limit=100)
        matches = [j for j in all_jobs if j.id.startswith(job_id)]
        if len(matches) == 1:
            job_id = matches[0].id
        elif len(matches) > 1:
            console.print(f"[yellow]Multiple jobs match '{job_id}':[/yellow]")
            for j in matches:
                console.print(f"  {j.id}")
            return
        else:
            console.print(f"[red]Job not found:[/red] {job_id}")
            return

    if job_manager.cancel_job(job_id):
        console.print(f"[green]Cancelled:[/green] {job_id}")
    else:
        console.print(f"[red]Cannot cancel:[/red] {job_id} (not running or not found)")


@jobs.command("result")
@click.argument("job_id")
def jobs_result(job_id: str):
    """Get result of a completed job.

    \b
    JOB_ID: Job ID to get result for

    \b
    Examples:
      sci-writer jobs result abc12345
    """
    from sci_writer._jobs import JobStatus, job_manager

    # Try prefix match
    job = job_manager.get_job(job_id)
    if not job:
        all_jobs = job_manager.list_jobs(limit=100)
        matches = [j for j in all_jobs if j.id.startswith(job_id)]
        if len(matches) == 1:
            job = matches[0]
        elif len(matches) > 1:
            console.print(f"[yellow]Multiple jobs match '{job_id}':[/yellow]")
            for j in matches:
                console.print(f"  {j.id}")
            return
        else:
            console.print(f"[red]Job not found:[/red] {job_id}")
            return

    if job.status not in (JobStatus.COMPLETED, JobStatus.FAILED):
        console.print(
            f"[yellow]Job not finished:[/yellow] status is {job.status.value}"
        )
        return

    if job.status == JobStatus.COMPLETED:
        console.print("[bold green]Job completed successfully[/bold green]")
        if job.result:
            console.print(f"[bold]Result:[/bold]\n{job.result}")
    else:
        console.print("[bold red]Job failed[/bold red]")
        if job.error:
            console.print(f"[bold]Error:[/bold] {job.error}")


@jobs.command("clear")
@click.option("--all", "clear_all", is_flag=True, help="Clear all jobs")
@click.option("--completed", is_flag=True, help="Clear completed jobs")
@click.option("--failed", is_flag=True, help="Clear failed jobs")
@click.confirmation_option(prompt="Clear jobs?")
def jobs_clear(clear_all: bool, completed: bool, failed: bool):
    """Clear jobs from history.

    \b
    Examples:
      sci-writer jobs clear --completed        # Clear completed
      sci-writer jobs clear --failed           # Clear failed
      sci-writer jobs clear --all              # Clear all
    """
    from sci_writer._jobs import JobStatus, job_manager

    if not (clear_all or completed or failed):
        console.print("[yellow]Specify --all, --completed, or --failed[/yellow]")
        return

    statuses = []
    if clear_all:
        statuses = list(JobStatus)
    else:
        if completed:
            statuses.append(JobStatus.COMPLETED)
        if failed:
            statuses.append(JobStatus.FAILED)

    count = job_manager.clear_jobs(statuses)
    console.print(f"[green]Cleared {count} jobs[/green]")
