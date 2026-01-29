"""Init command - Create a new BoringPy workspace."""

import re
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from boringpy import __version__
from boringpy.cli.utils.workspace import create_workspace_config, save_workspace_config

console = Console()

# Valid workspace name pattern (alphanumeric, hyphens, underscores)
WORKSPACE_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")


def init(
    name: str = typer.Argument(..., help="Workspace name"),
    directory: Path = typer.Option(
        None, "--dir", "-d", help="Parent directory (defaults to current directory)"
    ),
) -> None:
    """
    Initialize a new BoringPy workspace.

    Creates a workspace with the following structure:
    - src/apps/ (for FastAPI applications)
    - src/libs/ (for shared libraries)
    - src/scripts/ (for utility scripts)
    - boringpy.json (workspace configuration)
    - pyproject.toml (UV workspace root)
    - .gitignore
    - README.md
    """
    # Validate workspace name
    if not WORKSPACE_NAME_PATTERN.match(name):
        console.print("[red]Error: Invalid workspace name[/red]")
        console.print(
            "Workspace name must start with alphanumeric character and "
            "contain only letters, numbers, hyphens, and underscores."
        )
        raise typer.Exit(1)

    # Determine workspace path
    parent_dir = directory or Path.cwd()
    workspace_path = parent_dir / name

    # Check if workspace already exists
    if workspace_path.exists():
        console.print(f"[red]Error: Directory '{workspace_path}' already exists[/red]")
        raise typer.Exit(1)

    console.print(f"\n[cyan]Creating BoringPy workspace:[/cyan] {name}")
    console.print(f"[dim]Location: {workspace_path}[/dim]\n")

    try:
        # Create workspace directory structure
        workspace_path.mkdir(parents=True)
        (workspace_path / "src").mkdir()
        (workspace_path / "src" / "apps").mkdir()
        (workspace_path / "src" / "libs").mkdir()
        (workspace_path / "src" / "scripts").mkdir()

        # Create boringpy.json
        config = create_workspace_config(workspace_path)
        save_workspace_config(config, workspace_path)
        console.print("[green]✓[/green] Created boringpy.json")

        # Create pyproject.toml (UV workspace root)
        pyproject_content = f'''[project]
name = "{name}"
version = "0.1.0"
description = "BoringPy workspace"
requires-python = ">=3.13"

[tool.uv.workspace]
members = ["src/apps/*", "src/libs/*"]

[tool.uv.sources]
# Configure workspace dependencies here
'''
        (workspace_path / "pyproject.toml").write_text(pyproject_content)
        console.print("[green]✓[/green] Created pyproject.toml")

        # Create .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# UV
.uv/

# Docker
*.log
"""
        (workspace_path / ".gitignore").write_text(gitignore_content)
        console.print("[green]✓[/green] Created .gitignore")

        # Create README.md
        readme_content = f"""# {name}

BoringPy workspace for modern Python development.

## Structure

```
{name}/
├── src/
│   ├── apps/       # FastAPI applications
│   ├── libs/       # Shared libraries
│   └── scripts/    # Utility scripts
├── boringpy.json   # Workspace configuration
├── pyproject.toml  # UV workspace root
└── README.md
```

## Getting Started

### Generate a new API

```bash
boringpy generate api my-api --port 8000 --db postgresql
```

### Generate a new library

```bash
boringpy generate lib my-lib
```

## Development

This workspace uses:
- **UV** for package management
- **BoringPy** for code generation
- **FastAPI** for APIs
- **Docker** for containerization
- **Alembic** for database migrations

## Generated with

BoringPy v{__version__}
"""
        (workspace_path / "README.md").write_text(readme_content)
        console.print("[green]✓[/green] Created README.md")

        # Success message
        console.print()
        console.print(
            Panel(
                f"[green]✨ Workspace '{name}' created successfully![/green]\n\n"
                f"Next steps:\n"
                f"  [cyan]cd {name}[/cyan]\n"
                f"  [cyan]boringpy generate api my-api[/cyan]\n\n"
                f"Or explore the commands:\n"
                f"  [cyan]boringpy --help[/cyan]",
                title="Success",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(f"\n[red]Error creating workspace: {e}[/red]")
        # Cleanup on failure
        if workspace_path.exists():
            import shutil

            shutil.rmtree(workspace_path)
        raise typer.Exit(1)
