"""Generate command - Generate code from templates."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from boringpy.cli.utils.workspace import add_workspace_member, require_workspace
from boringpy.core.generator import GeneratorConfig
from boringpy.generators import ApiGenerator
from boringpy.utils.paths import get_template_path

app = typer.Typer(help="Generate code from templates")
console = Console()


@app.command()
def api(
    name: str = typer.Argument(..., help="API package name (snake_case)"),
    port: int = typer.Option(8000, "--port", "-p", help="API port number"),
    db_type: str = typer.Option(
        "postgresql",
        "--db",
        help="Database type (postgresql, mysql, sqlite)",
    ),
) -> None:
    """
    Generate a new FastAPI application.

    Creates a production-ready FastAPI application with:
    - Database configuration (SQLModel + Alembic)
    - Docker setup with docker-compose
    - Comprehensive Makefile
    - Testing infrastructure
    - Environment-based configuration
    - Structured logging

    The API will be created in src/apps/<name>/ directory.
    """
    # Ensure we're in a workspace
    try:
        workspace_root = require_workspace()
    except FileNotFoundError:
        raise typer.Exit(1)

    console.print(f"\n[cyan]Generating FastAPI application:[/cyan] {name}")
    console.print(f"[dim]Port: {port} | Database: {db_type}[/dim]\n")

    try:
        # Load template configuration
        template_path = get_template_path("api")
        config = GeneratorConfig.from_template_json(template_path)

        # Create generator
        generator = ApiGenerator(config)

        # Set destination (src/apps in workspace)
        destination = workspace_root / "src" / "apps"
        destination.mkdir(parents=True, exist_ok=True)

        # Generate the API
        output_dir = generator.generate(
            destination=destination,
            package_name=name,
            port=port,
            db_type=db_type,
        )

        # Add to workspace members
        relative_path = output_dir.relative_to(workspace_root)
        add_workspace_member(str(relative_path), workspace_root)

        # Success panel
        console.print()
        console.print(
            Panel(
                f"[green]✨ API '{name}' generated successfully![/green]\n\n"
                f"Location: [cyan]{relative_path}[/cyan]\n\n"
                f"Next steps:\n"
                f"  [cyan]cd {relative_path}[/cyan]\n"
                f"  [cyan]cp .env.example .env[/cyan]\n"
                f"  [cyan]make docker-up[/cyan]\n"
                f"  [cyan]make db-upgrade[/cyan]\n\n"
                f"Or see the README:\n"
                f"  [cyan]cat {relative_path}/README.md[/cyan]",
                title="Success",
                border_style="green",
            )
        )

    except ValueError as e:
        console.print(f"\n[red]Validation Error:[/red] {e}")
        raise typer.Exit(1)
    except FileNotFoundError as e:
        console.print(f"\n[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]Generation failed:[/red] {e}")
        console.print("\n[dim]Run with --help for usage information[/dim]")
        raise typer.Exit(1)


@app.command()
def lib(
    name: str = typer.Argument(..., help="Library name (snake_case)"),
) -> None:
    """
    Generate a new shared library (Coming soon).

    Creates a reusable Python library in src/libs/<name>/.
    """
    console.print("[yellow]Library generation coming soon![/yellow]")
    console.print("\nThis feature will create a shared library that can be")
    console.print("used across multiple APIs in your workspace.")
    raise typer.Exit(0)


@app.command()
def model(
    name: str = typer.Argument(..., help="Model name (PascalCase)"),
) -> None:
    """
    Generate a new SQLModel (Coming soon).

    Creates a database model in the current API project.
    """
    console.print("[yellow]Model generation coming soon![/yellow]")
    console.print("\nThis feature will create SQLModel classes with")
    console.print("proper type annotations and table configuration.")
    raise typer.Exit(0)
