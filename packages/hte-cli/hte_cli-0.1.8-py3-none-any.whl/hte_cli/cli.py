"""CLI commands for hte-cli.

Uses Click for command parsing and Rich for pretty output.
"""

import sys
import webbrowser

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from hte_cli import __version__, API_BASE_URL
from hte_cli.config import Config, get_eval_logs_dir
from hte_cli.api_client import APIClient, APIError

console = Console()

# Support email per spec
SUPPORT_EMAIL = "jacktpayne51@gmail.com"


@click.group()
@click.version_option(__version__, prog_name="hte-cli")
@click.pass_context
def cli(ctx):
    """Human Time-to-Completion Evaluation CLI.

    Run assigned cybersecurity tasks via Docker and sync results.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config.load()


# =============================================================================
# Auth Commands
# =============================================================================


@cli.group()
def auth():
    """Authentication commands."""
    pass


@auth.command("login")
@click.pass_context
def auth_login(ctx):
    """Log in via browser to get an API key."""
    config: Config = ctx.obj["config"]

    if config.is_authenticated():
        days = config.days_until_expiry()
        console.print(f"[green]Already logged in as {config.user_email}[/green]")
        if days is not None:
            console.print(f"API key expires in {days} days")
        if not click.confirm("Log in again?"):
            return

    # Show login URL
    login_url = f"{API_BASE_URL.replace('/api/v1/cli', '')}/cli/auth"
    console.print()
    console.print(
        Panel(
            f"[bold]Visit this URL to log in:[/bold]\n\n{login_url}",
            title="Login",
        )
    )
    console.print()

    # Try to open browser
    try:
        webbrowser.open(login_url)
        console.print("[dim]Browser opened. Complete login in browser.[/dim]")
    except Exception:
        console.print("[dim]Open the URL manually in your browser.[/dim]")

    console.print()

    # Get code from user
    code = click.prompt("Enter the code from the browser")

    # Exchange code for API key
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Authenticating...", total=None)

        try:
            api = APIClient(config)
            result = api.exchange_code_for_token(code)

            config.api_key = result["api_key"]
            config.api_key_expires_at = result["expires_at"]
            config.user_email = result["user_email"]
            config.user_name = result["user_name"]
            config.api_url = API_BASE_URL
            config.save()

        except APIError as e:
            console.print(f"[red]Login failed: {e}[/red]")
            sys.exit(1)

    console.print()
    console.print(f"[green]Logged in as {config.user_name} ({config.user_email})[/green]")
    days = config.days_until_expiry()
    if days is not None:
        console.print(f"API key expires in {days} days")


@auth.command("logout")
@click.pass_context
def auth_logout(ctx):
    """Clear stored credentials."""
    config: Config = ctx.obj["config"]
    config.clear()
    console.print("[green]Logged out successfully[/green]")


@auth.command("status")
@click.pass_context
def auth_status(ctx):
    """Show current authentication status."""
    config: Config = ctx.obj["config"]

    if not config.is_authenticated():
        console.print("[yellow]Not logged in[/yellow]")
        console.print("Run: hte-cli auth login")
        return

    console.print(f"[green]Logged in as:[/green] {config.user_name}")
    console.print(f"[green]Email:[/green] {config.user_email}")

    days = config.days_until_expiry()
    if days is not None:
        if days <= 7:
            console.print(f"[yellow]API key expires in {days} days[/yellow]")
        else:
            console.print(f"API key expires in {days} days")


# =============================================================================
# Tasks Commands
# =============================================================================


@cli.group()
def tasks():
    """Task commands."""
    pass


@tasks.command("list")
@click.pass_context
def tasks_list(ctx):
    """List pending task assignments."""
    config: Config = ctx.obj["config"]

    if not config.is_authenticated():
        console.print("[red]Not logged in. Run: hte-cli auth login[/red]")
        sys.exit(1)

    api = APIClient(config)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Fetching assignments...", total=None)

        try:
            assignments = api.get_assignments()
        except APIError as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)

    if not assignments:
        console.print("[yellow]No pending assignments[/yellow]")
        return

    table = Table(title="Pending Assignments")
    table.add_column("Task ID", style="cyan")
    table.add_column("Benchmark", style="green")
    table.add_column("Mode")
    table.add_column("Priority", justify="right")
    table.add_column("Status")

    for a in assignments:
        status = "In Progress" if a.get("session_id") else "Pending"
        status_style = "yellow" if a.get("session_id") else ""

        table.add_row(
            a["task_id"],
            a["benchmark"],
            a["mode"],
            str(a["priority"]),
            f"[{status_style}]{status}[/{status_style}]" if status_style else status,
        )

    console.print(table)
    console.print()
    console.print("Run: [bold]hte-cli tasks run[/bold] to start the highest priority task")


@tasks.command("run")
@click.argument("task_id", required=False)
@click.pass_context
def tasks_run(ctx, task_id: str | None):
    """Run a task (default: highest priority pending task)."""
    config: Config = ctx.obj["config"]

    if not config.is_authenticated():
        console.print("[red]Not logged in. Run: hte-cli auth login[/red]")
        sys.exit(1)

    # Check Docker
    if not _check_docker():
        console.print("[red]Docker is not running or not installed.[/red]")
        console.print()
        console.print("Install Docker: https://docs.docker.com/get-docker/")
        sys.exit(1)

    api = APIClient(config)

    # Get assignments
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Fetching assignments...", total=None)
        try:
            assignments = api.get_assignments()
        except APIError as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)

    if not assignments:
        console.print("[yellow]No pending assignments[/yellow]")
        return

    # Find the assignment to run
    assignment = None
    if task_id:
        for a in assignments:
            if a["task_id"] == task_id:
                assignment = a
                break
        if not assignment:
            console.print(f"[red]Task not found in your assignments: {task_id}[/red]")
            sys.exit(1)
    else:
        # Take highest priority (first in list, already sorted by server)
        assignment = assignments[0]

    console.print()
    console.print(
        Panel(
            f"[bold]Task:[/bold] {assignment['task_id']}\n"
            f"[bold]Benchmark:[/bold] {assignment['benchmark']}\n"
            f"[bold]Mode:[/bold] {assignment['mode']}",
            title="Starting Task",
        )
    )
    console.print()

    # Import runner and events
    from hte_cli.runner import TaskRunner
    from hte_cli.events import EventStreamer

    # Step 1: Start session (or resume existing)
    session_id = assignment.get("session_id")
    if not session_id:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Starting session...", total=None)
            try:
                session_info = api.start_session(assignment["assignment_id"])
                session_id = session_info["session_id"]
            except APIError as e:
                console.print(f"[red]Failed to start session: {e}[/red]")
                sys.exit(1)
    else:
        console.print(f"[yellow]Resuming session: {session_id}[/yellow]")

    # Create event streamer
    events = EventStreamer(api, session_id)

    # Step 2: Download task files and compose
    files_zip = None
    compose_yaml = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Download files
        task_id_display = progress.add_task("Downloading task files...", total=None)
        try:
            files_zip = api.get_assignment_files(assignment["assignment_id"])
        except APIError as e:
            # Files are optional for some benchmarks
            console.print(f"[dim]Note: {e}[/dim]")

        # Download compose
        progress.update(task_id_display, description="Downloading compose file...")
        try:
            compose_yaml = api.get_assignment_compose(assignment["assignment_id"])
        except APIError as e:
            # Compose is optional for simple benchmarks
            console.print(f"[dim]Note: {e}[/dim]")

    # Step 3: Send session_started event
    events.session_started(
        {
            "cli_version": __version__,
            "task_id": assignment["task_id"],
        }
    )

    # Step 4: Show pre-task message (benchmark-specific)
    benchmark = assignment.get("benchmark", "").lower()
    single_shot_benchmarks = {"nl2bash", "cybashbench"}

    console.print()
    if benchmark in single_shot_benchmarks:
        # Single-shot benchmarks - no task score available
        console.print(
            Panel(
                "[bold]Instructions[/bold]\n\n"
                "You are about to enter the task environment.\n\n"
                "[yellow]IMPORTANT: This is a SINGLE-SHOT task.[/yellow]\n"
                "[yellow]You get ONE submission attempt - no retries![/yellow]\n\n"
                "Commands available:\n"
                "  [cyan]task status[/cyan]  - Show elapsed time\n"
                '  [cyan]task submit "answer"[/cyan]  - Submit your FINAL answer (ends task)\n'
                "  [cyan]task quit[/cyan]  - Quit without submitting\n"
                '  [cyan]task note "text"[/cyan]  - Record observations\n',
                title="Task Environment",
            )
        )
    else:
        # CTF/sandbox benchmarks - task score available
        console.print(
            Panel(
                "[bold]Instructions[/bold]\n\n"
                "You are about to enter the task environment.\n\n"
                "Commands available:\n"
                "  [cyan]task status[/cyan]  - Show elapsed time\n"
                '  [cyan]task score "answer"[/cyan]  - CHECK if correct (does NOT end task)\n'
                '  [cyan]task submit "answer"[/cyan]  - Submit FINAL answer (ends task)\n'
                "  [cyan]task quit[/cyan]  - Quit without submitting\n"
                '  [cyan]task note "text"[/cyan]  - Record observations\n\n'
                "[green]TIP: Use 'task score' to verify before submitting![/green]\n",
                title="Task Environment",
            )
        )
    console.print()

    if not click.confirm("Ready to start?"):
        console.print("[yellow]Cancelled[/yellow]")
        return

    # Step 5: Run Inspect's human_cli
    runner = TaskRunner()
    console.print()
    console.print("[bold]Starting task environment...[/bold]")
    console.print("[dim]This may take a moment to start Docker containers.[/dim]")
    console.print()

    events.docker_started()

    eval_log_bytes = None
    local_eval_path = None
    try:
        result = runner.run_from_assignment(
            assignment=assignment,
            compose_yaml=compose_yaml,
            files_zip=files_zip,
        )
        # Read eval log BEFORE cleanup (cleanup deletes the temp directory)
        if result.eval_log_path and result.eval_log_path.exists():
            eval_log_bytes = result.eval_log_path.read_bytes()

            # Save local copy for safety
            eval_logs_dir = get_eval_logs_dir()
            eval_logs_dir.mkdir(parents=True, exist_ok=True)
            local_eval_path = eval_logs_dir / result.eval_log_path.name
            local_eval_path.write_bytes(eval_log_bytes)
    except Exception as e:
        events.docker_stopped(exit_code=1)
        console.print(f"[red]Task execution failed: {e}[/red]")
        sys.exit(1)
    finally:
        runner.cleanup()

    events.docker_stopped(exit_code=0)

    # Step 6: Show post-task summary
    console.print()
    console.print(
        Panel(
            f"[bold]Time spent:[/bold] {result.time_seconds / 60:.1f} minutes\n"
            f"[bold]Answer:[/bold] {result.answer or '(none)'}\n"
            f"[bold]Score:[/bold] {result.score if result.score is not None else 'pending'}",
            title="Task Complete",
        )
    )

    # Step 7: Upload result
    events.session_completed(
        elapsed_seconds=result.time_seconds,
        answer=result.answer,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Uploading result...", total=None)

        # Warn if eval log is large
        if eval_log_bytes:
            size_mb = len(eval_log_bytes) / 1024 / 1024
            if size_mb > 50:
                console.print(f"[yellow]Warning: Large eval log ({size_mb:.1f} MB)[/yellow]")

        try:
            upload_result = api.upload_result(
                session_id=session_id,
                answer=result.answer or "",
                client_active_seconds=result.time_seconds,
                eval_log_bytes=eval_log_bytes,
                score=result.score,
                score_binarized=result.score_binarized,
            )
        except APIError as e:
            console.print(f"[red]Failed to upload result: {e}[/red]")
            if local_eval_path:
                console.print(f"[yellow]Eval log saved locally: {local_eval_path}[/yellow]")
            console.print("[yellow]Your result was saved locally but not uploaded.[/yellow]")
            sys.exit(1)

    console.print()
    console.print("[green]Result uploaded successfully![/green]")

    # Show local eval log path
    if local_eval_path:
        console.print(f"[dim]Eval log saved to: {local_eval_path}[/dim]")

    # Show next task if available
    if upload_result.get("next_assignment_id"):
        console.print()
        console.print("Run [bold]hte-cli tasks run[/bold] for the next task.")


@tasks.command("pull-images")
@click.option("--count", "-n", default=5, help="Number of upcoming tasks to pull images for")
@click.pass_context
def tasks_pull_images(ctx, count: int):
    """Pre-pull Docker images for upcoming tasks."""
    config: Config = ctx.obj["config"]

    if not config.is_authenticated():
        console.print("[red]Not logged in. Run: hte-cli auth login[/red]")
        sys.exit(1)

    # Check Docker
    if not _check_docker():
        console.print("[red]Docker is not running or not installed.[/red]")
        sys.exit(1)

    api = APIClient(config)

    # Get assignments
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Fetching assignments...", total=None)
        try:
            assignments = api.get_assignments()
        except APIError as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)

    if not assignments:
        console.print("[yellow]No pending assignments[/yellow]")
        return

    # Take first N
    to_pull = assignments[:count]

    console.print(f"Pulling images for {len(to_pull)} task(s)...")
    console.print()

    # TODO: Download compose files and extract image names, then pull
    console.print("[yellow]Image pulling not yet implemented.[/yellow]")


# =============================================================================
# Helper Functions
# =============================================================================


def _check_docker() -> bool:
    """Check if Docker is installed and running."""
    import subprocess

    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


if __name__ == "__main__":
    cli()
