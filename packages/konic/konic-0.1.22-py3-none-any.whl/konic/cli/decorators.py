"""CLI command decorators for error handling, output formatting, and loading indicators."""

import functools
import json
import time
from collections.abc import Callable
from enum import Enum
from typing import Any, TypeVar

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table

from konic.common.errors import KonicCLIError

__all__ = [
    "stdout_handler",
    "json_output",
    "pretty_output",
    "error_handler",
    "loading_indicator",
    "success_message",
    "table_output",
    "benchmark",
]

console = Console()
F = TypeVar("F", bound=Callable[..., Any])


class OutputFormat(str, Enum):
    JSON = "json"
    PRETTY = "pretty"
    PLAIN = "plain"


def error_handler(
    exit_on_error: bool = True,
    show_traceback: bool = False,
) -> Callable[[F], F]:
    """Handle CLI errors with formatted output and optional exit."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KonicCLIError as e:
                console.print(f"\n[bold red]✗ Error:[/bold red] {e.message}", style="red")
                if show_traceback:
                    console.print_exception()
                if exit_on_error:
                    raise typer.Exit(code=getattr(e, "exit_code", 1))
                return None

            except (SystemExit, KeyboardInterrupt, typer.Exit):
                raise

            except Exception as e:
                console.print(f"\n[bold red]✗ Unexpected Error:[/bold red] {str(e)}", style="red")
                if show_traceback:
                    console.print_exception()
                if exit_on_error:
                    raise typer.Exit(code=1)
                return None

        return wrapper  # type: ignore

    return decorator


def stdout_handler[F: Callable[..., Any]](func: F) -> F:
    """Auto-print command return values (dict/list as JSON, others as string)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            if isinstance(result, (dict | list)):
                console.print_json(data=result)
            elif isinstance(result, str):
                console.print(result)
            else:
                console.print(str(result))
        return result

    return wrapper  # type: ignore


def json_output(
    pretty: bool = True,
    indent: int = 2,
) -> Callable[[F], F]:
    """Output command results as JSON."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is not None:
                if pretty:
                    console.print_json(data=result, indent=indent)
                else:
                    print(json.dumps(result, separators=(",", ":")))
            return result

        return wrapper  # type: ignore

    return decorator


def pretty_output(
    title: str | None = None,
    border_style: str = "blue",
) -> Callable[[F], F]:
    """Display output in a Rich panel."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is not None:
                if isinstance(result, dict):
                    content = json.dumps(result, indent=2)
                    syntax = Syntax(content, "json", theme="monokai", line_numbers=False)
                    console.print(Panel(syntax, title=title, border_style=border_style))
                else:
                    console.print(Panel(str(result), title=title, border_style=border_style))
            return result

        return wrapper  # type: ignore

    return decorator


def loading_indicator(
    message: str = "Processing...",
    success_message: str | None = None,
) -> Callable[[F], F]:
    """Show spinner while command executes."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True,
            ) as progress:
                progress.add_task(description=message, total=None)
                result = func(*args, **kwargs)

            if success_message:
                console.print(f"[bold green]✓[/bold green] {success_message}")

            return result

        return wrapper  # type: ignore

    return decorator


def success_message(message: str) -> Callable[[F], F]:
    """Display success message after command execution."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            console.print(f"\n[bold green]✓[/bold green] {message}", style="green")
            return result

        return wrapper  # type: ignore

    return decorator


def table_output(
    title: str | None = None,
    columns: list[str] | None = None,
) -> Callable[[F], F]:
    """Display results as a Rich table."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if result is not None and isinstance(result, list) and len(result) > 0:
                table = Table(title=title, show_header=True, header_style="bold magenta")

                if columns:
                    for col in columns:
                        table.add_column(col)
                elif isinstance(result[0], dict):
                    for col in result[0].keys():
                        table.add_column(str(col))

                for item in result:
                    if isinstance(item, dict):
                        table.add_row(*[str(v) for v in item.values()])
                    else:
                        table.add_row(str(item))

                console.print(table)
            elif result is not None:
                console.print(result)

            return result

        return wrapper  # type: ignore

    return decorator


def benchmark(show_time: bool = True) -> Callable[[F], F]:
    """Measure and display command execution time."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time

            if show_time:
                console.print(
                    f"\n[dim]⏱  Executed in {elapsed_time:.2f}s[/dim]",
                    style="cyan",
                )

            return result

        return wrapper  # type: ignore

    return decorator
