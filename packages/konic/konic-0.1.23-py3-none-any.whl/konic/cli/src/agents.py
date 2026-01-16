"""CLI commands for agent management."""

import json
import zipfile
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from konic.cli.client import client
from konic.cli.decorators import error_handler, loading_indicator
from konic.cli.env_keys import KonicCLIEnvVars
from konic.cli.utils import (
    apply_host_override,
    bump_version,
    create_artifact_zip,
    find_entrypoint_file,
    format_file_size,
    get_agent_by_id,
    resolve_agent_identifier,
)
from konic.common.errors import (
    KonicAgentConflictError,
    KonicAgentNotFoundError,
    KonicHTTPError,
    KonicValidationError,
)

app = typer.Typer(
    name="agent",
    help="Manage agents on Konic Cloud Platform",
    no_args_is_help=True,
)

console = Console()


def _sanitize_path_component(name: str) -> str:
    """Sanitize string for safe use in file paths."""
    sanitized = name.replace("/", "_").replace("\\", "_")
    sanitized = sanitized.replace("..", "_")

    # Remove any leading dots or dashes that could cause issues
    sanitized = sanitized.lstrip(".-")

    # If the result is empty or only whitespace, provide a default
    if not sanitized or sanitized.isspace():
        sanitized = "agent"

    return sanitized


def _compile_agent_directory(path: Path, agent_version: str = "v1", agent_type: str = "rl") -> Path:
    """Compile agent directory into a zip artifact."""
    if not path.exists():
        raise KonicValidationError(f"Path does not exist: {path}", field="path")

    if not path.is_dir():
        raise KonicValidationError(f"Path must be a directory, not a file: {path}", field="path")

    entrypoint = find_entrypoint_file(path)
    if not entrypoint:
        raise KonicValidationError(
            f"No entrypoint file found in {path}. "
            "Ensure your agent calls 'register_agent()' in a Python file.",
            field="path",
        )

    return create_artifact_zip(
        path,
        str(entrypoint.relative_to(path)),
        agent_version=agent_version,
        agent_type=agent_type,
    )


def _cleanup_artifact(zip_path: Path, keep: bool) -> None:
    if not keep and zip_path.exists():
        zip_path.unlink()


def _detect_agent_type(path: Path) -> str:
    """Detect agent type from imports. Returns 'rl' or 'finetuning'."""
    finetuning_patterns = [
        "from konic.finetuning",
        "import konic.finetuning",
        "KonicFineTuningAgent",
    ]

    for py_file in path.rglob("*.py"):
        try:
            content = py_file.read_text()
            for pattern in finetuning_patterns:
                if pattern in content:
                    return "finetuning"
        except (OSError, UnicodeDecodeError):
            continue

    return "rl"


def _display_agent_table(agents: list[dict]) -> None:
    table = Table(
        title="Agents",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Name", style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Version", style="green")
    table.add_column("Konic Version", style="yellow")
    table.add_column("Size", justify="right")
    table.add_column("Updated At")

    for agent in agents:
        table.add_row(
            agent.get("agent_name", "N/A"),
            agent.get("id", "N/A"),
            agent.get("agent_version", "N/A"),
            agent.get("konic_version", "N/A"),
            format_file_size(agent.get("file_size", 0)),
            agent.get("updated_at", "N/A")[:19].replace("T", " "),
        )

    console.print(table)


def _display_agent_detail(agent: dict) -> None:
    versions_info = ""
    if agent.get("versions"):
        versions_info = "\n\n[bold]Versions:[/bold]\n"
        for v in agent["versions"]:
            versions_info += f"  • {v['version']} ({format_file_size(v.get('file_size', 0))}) - {v.get('created_at', 'N/A')[:19]}\n"

    content = f"""[bold cyan]Name:[/bold cyan] {agent.get("agent_name", "N/A")}
[bold cyan]ID:[/bold cyan] {agent.get("id", "N/A")}
[bold cyan]Current Version:[/bold cyan] {agent.get("agent_version", "N/A")}
[bold cyan]Konic Version:[/bold cyan] {agent.get("konic_version", "N/A")}
[bold cyan]Entrypoint:[/bold cyan] {agent.get("entrypoint", "N/A")}
[bold cyan]File Size:[/bold cyan] {format_file_size(agent.get("file_size", 0))}
[bold cyan]Created:[/bold cyan] {agent.get("created_at", "N/A")[:19].replace("T", " ")}
[bold cyan]Updated:[/bold cyan] {agent.get("updated_at", "N/A")[:19].replace("T", " ")}{versions_info}"""

    console.print(Panel(content, title="Agent Details", border_style="blue"))


@app.command(name="push")
@error_handler(exit_on_error=True)
@loading_indicator(message="Compiling and uploading agent...")
def push_agent(
    path: Annotated[
        Path,
        typer.Argument(
            help="Path to the agent directory to compile and push",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ],
    host: Annotated[
        str | None,
        typer.Option(
            "--host",
            "-h",
            help="Override the Konic API host URL",
            envvar=KonicCLIEnvVars.KONIC_HOST.value,
        ),
    ] = None,
    keep_artifact: Annotated[
        bool,
        typer.Option(
            "--keep-artifact",
            "-k",
            help="Keep the compiled zip artifact after upload",
        ),
    ] = False,
    agent_type: Annotated[
        str | None,
        typer.Option(
            "--type",
            "-t",
            help="Agent type: 'rl' or 'finetuning'. Auto-detected if not specified.",
        ),
    ] = None,
) -> None:
    """Compile and push a new agent to Konic Cloud Platform."""
    apply_host_override(host)
    if agent_type is None:
        agent_type = _detect_agent_type(path)
    elif agent_type not in ("rl", "finetuning"):
        raise KonicValidationError(
            f"Invalid agent type: {agent_type}. Must be 'rl' or 'finetuning'.",
            field="type",
        )

    zip_path = _compile_agent_directory(path, agent_type=agent_type)

    try:
        result = client.upload_file_json(
            "/agents/upload",
            zip_path,
        )
        console.print("\n[bold green]✓[/bold green] Agent pushed successfully!")
        _display_agent_detail(result)
    except KonicHTTPError as e:
        if e.status_code == 409:
            name = json.loads(str(e.response_body))["detail"]["agent_name"]
            raise KonicAgentConflictError(name)
        raise
    finally:
        _cleanup_artifact(zip_path, keep_artifact)


@app.command(name="update")
@error_handler(exit_on_error=True)
@loading_indicator(message="Compiling and updating agent...")
def update_agent(
    path: Annotated[
        Path,
        typer.Argument(
            help="Path to the agent directory to compile and update",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ],
    agent: Annotated[
        str,
        typer.Option(
            "--agent",
            "-a",
            help="Agent name or ID to update",
        ),
    ],
    host: Annotated[
        str | None,
        typer.Option(
            "--host",
            "-h",
            help="Override the Konic API host URL",
            envvar=KonicCLIEnvVars.KONIC_HOST.value,
        ),
    ] = None,
    keep_artifact: Annotated[
        bool,
        typer.Option(
            "--keep-artifact",
            "-k",
            help="Keep the compiled zip artifact after upload",
        ),
    ] = False,
) -> None:
    """Update an existing agent with a new version."""
    apply_host_override(host)

    agent_id = resolve_agent_identifier(client, agent)

    current_agent = get_agent_by_id(client, agent_id)
    current_version = current_agent.get("agent_version", "v0")
    next_version = bump_version(current_version)

    # Detect agent type from source code
    agent_type = _detect_agent_type(path)

    console.print(f"[dim]Bumping version: {current_version} → {next_version}[/dim]")

    zip_path = _compile_agent_directory(path, agent_version=next_version, agent_type=agent_type)

    try:
        result = client.upload_file_json(f"/agents/{agent_id}/versions", zip_path)
        console.print("\n[bold green]✓[/bold green] Agent updated successfully!")
        _display_agent_detail(result)
    except KonicHTTPError as e:
        if e.status_code == 404:
            raise KonicAgentNotFoundError(agent)
        raise
    finally:
        _cleanup_artifact(zip_path, keep_artifact)


@app.command(name="delete")
@error_handler(exit_on_error=True)
def delete_agent(
    agent: Annotated[
        str,
        typer.Option(
            "--agent",
            "-a",
            help="Agent name or ID to delete",
        ),
    ],
    host: Annotated[
        str | None,
        typer.Option(
            "--host",
            "-h",
            help="Override the Konic API host URL",
            envvar=KonicCLIEnvVars.KONIC_HOST.value,
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Skip confirmation prompt",
        ),
    ] = False,
) -> None:
    """Delete an agent (soft delete)."""
    apply_host_override(host)

    agent_id = resolve_agent_identifier(client, agent)

    agent_info = get_agent_by_id(client, agent_id)
    agent_name = agent_info.get("agent_name", agent_id)

    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete agent '{agent_name}'?")
        if not confirm:
            console.print("[yellow]Aborted.[/yellow]")
            raise typer.Exit(0)

    try:
        client.delete(f"/agents/{agent_id}")
        console.print(f"[bold green]✓[/bold green] Agent '{agent_name}' deleted successfully!")
    except KonicHTTPError as e:
        if e.status_code == 404:
            raise KonicAgentNotFoundError(agent)
        raise


@app.command(name="list")
@error_handler(exit_on_error=True)
@loading_indicator(message="Fetching agents...")
def list_agents(
    name: Annotated[
        str | None,
        typer.Option(
            "--name",
            "-n",
            help="Filter by agent name",
        ),
    ] = None,
    konic_version: Annotated[
        str | None,
        typer.Option(
            "--konic-version",
            help="Filter by Konic version",
        ),
    ] = None,
    start: Annotated[
        int,
        typer.Option(
            "--start",
            help="Pagination start index",
        ),
    ] = 0,
    end: Annotated[
        int,
        typer.Option(
            "--end",
            help="Pagination end index",
        ),
    ] = 20,
    host: Annotated[
        str | None,
        typer.Option(
            "--host",
            "-h",
            help="Override the Konic API host URL",
            envvar=KonicCLIEnvVars.KONIC_HOST.value,
        ),
    ] = None,
    output_json: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Output as JSON instead of table",
        ),
    ] = False,
) -> None:
    """List all agents with optional filters."""
    apply_host_override(host)

    params: dict = {"_start": start, "_end": end}
    if name:
        params["agent_name"] = name
    if konic_version:
        params["konic_version"] = konic_version

    agents = client.get_json("/agents", params=params)

    if output_json:
        console.print_json(data=agents)
    elif not agents:
        console.print("[yellow]No agents found.[/yellow]")
    else:
        _display_agent_table(agents)


@app.command(name="get")
@error_handler(exit_on_error=True)
@loading_indicator(message="Fetching agent...")
def get_agent(
    agent_id: Annotated[
        str,
        typer.Argument(help="Agent ID to retrieve"),
    ],
    host: Annotated[
        str | None,
        typer.Option(
            "--host",
            "-h",
            help="Override the Konic API host URL",
            envvar=KonicCLIEnvVars.KONIC_HOST.value,
        ),
    ] = None,
    output_json: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Output as JSON instead of formatted panel",
        ),
    ] = False,
) -> None:
    """Get details of a specific agent by ID."""
    apply_host_override(host)

    agent = get_agent_by_id(client, agent_id)

    if output_json:
        console.print_json(data=agent)
    else:
        _display_agent_detail(agent)


@app.command(name="download")
@error_handler(exit_on_error=True)
@loading_indicator(message="Downloading agent...")
def download_agent(
    agent_id: Annotated[
        str,
        typer.Argument(help="Agent ID to download"),
    ],
    version: Annotated[
        str | None,
        typer.Option(
            "--version",
            "-v",
            help="Specific version to download (default: latest)",
        ),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output directory path (default: ./<agent_name>-<version>/)",
        ),
    ] = None,
    host: Annotated[
        str | None,
        typer.Option(
            "--host",
            "-h",
            help="Override the Konic API host URL",
            envvar=KonicCLIEnvVars.KONIC_HOST.value,
        ),
    ] = None,
    keep_zip: Annotated[
        bool,
        typer.Option(
            "--keep-zip",
            "-k",
            help="Keep the downloaded zip file after extraction",
        ),
    ] = False,
) -> None:
    """Download and extract an agent."""
    apply_host_override(host)

    agent = get_agent_by_id(client, agent_id)
    agent_name = agent.get("agent_name", "agent")
    agent_version = version or agent.get("agent_version", "latest")

    # Sanitize agent_name to prevent path traversal attacks
    safe_agent_name = _sanitize_path_component(agent_name)
    safe_agent_version = _sanitize_path_component(agent_version)

    if output is None:
        output_dir = Path(f"{safe_agent_name}-{safe_agent_version}")
    else:
        output_dir = output

    zip_path = Path(f"{safe_agent_name}-{safe_agent_version}.zip")

    params = {}
    if version:
        params["version"] = version

    downloaded_path = client.download_file(
        f"/agents/{agent_id}/download",
        zip_path,
        params=params if params else None,
    )

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(downloaded_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        console.print(f"[bold green]✓[/bold green] Agent extracted to: {output_dir}")
    finally:
        if not keep_zip and downloaded_path.exists():
            downloaded_path.unlink()
        elif keep_zip:
            console.print(f"[dim]Zip file kept at: {downloaded_path}[/dim]")
