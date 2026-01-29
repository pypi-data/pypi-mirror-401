"""Main Typer CLI application for BoringPy."""

import typer
from rich.console import Console

from boringpy import __version__
from boringpy.cli.commands import generate, init

app = typer.Typer(
    name="boringpy",
    help="Modern Python scaffolding framework inspired by NestJS CLI",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"BoringPy version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """BoringPy - NestJS-inspired scaffolding for Python."""
    pass


# Register commands
app.command(name="init")(init.init)
app.add_typer(generate.app, name="generate")
