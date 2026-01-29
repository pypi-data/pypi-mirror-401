"""Workspace management utilities."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rich.console import Console

console = Console()


def find_workspace_root(start_path: Path | None = None) -> Path | None:
    """
    Find the workspace root by looking for boringpy.json.

    Walks up the directory tree from start_path (or cwd) looking for boringpy.json.

    Args:
        start_path: Starting directory (defaults to current working directory)

    Returns:
        Path to workspace root, or None if not found
    """
    current = start_path or Path.cwd()

    # Check current directory and all parents
    for directory in [current, *current.parents]:
        config_file = directory / "boringpy.json"
        if config_file.exists():
            return directory

    return None


def is_in_workspace(start_path: Path | None = None) -> bool:
    """
    Check if current directory is inside a BoringPy workspace.

    Args:
        start_path: Starting directory (defaults to current working directory)

    Returns:
        True if inside workspace, False otherwise
    """
    return find_workspace_root(start_path) is not None


def load_workspace_config(workspace_root: Path | None = None) -> dict[str, Any]:
    """
    Load workspace configuration from boringpy.json.

    Args:
        workspace_root: Workspace root directory (auto-detected if None)

    Returns:
        Workspace configuration dictionary

    Raises:
        FileNotFoundError: If boringpy.json not found
        ValueError: If boringpy.json is invalid JSON
    """
    if workspace_root is None:
        workspace_root = find_workspace_root()
        if workspace_root is None:
            raise FileNotFoundError("Not in a BoringPy workspace (boringpy.json not found)")

    config_file = workspace_root / "boringpy.json"
    if not config_file.exists():
        raise FileNotFoundError(f"boringpy.json not found in {workspace_root}")

    try:
        return json.loads(config_file.read_text())
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid boringpy.json: {e}")


def save_workspace_config(config: dict[str, Any], workspace_root: Path | None = None) -> None:
    """
    Save workspace configuration to boringpy.json.

    Args:
        config: Configuration dictionary to save
        workspace_root: Workspace root directory (auto-detected if None)

    Raises:
        FileNotFoundError: If workspace not found
    """
    if workspace_root is None:
        workspace_root = find_workspace_root()
        if workspace_root is None:
            raise FileNotFoundError("Not in a BoringPy workspace")

    config_file = workspace_root / "boringpy.json"
    config_file.write_text(json.dumps(config, indent=2) + "\n")


def update_workspace_config(updates: dict[str, Any], workspace_root: Path | None = None) -> None:
    """
    Update workspace configuration with new values.

    Args:
        updates: Dictionary of values to update
        workspace_root: Workspace root directory (auto-detected if None)

    Raises:
        FileNotFoundError: If workspace not found
        ValueError: If boringpy.json is invalid
    """
    config = load_workspace_config(workspace_root)
    config.update(updates)
    save_workspace_config(config, workspace_root)


def require_workspace() -> Path:
    """
    Require that current directory is in a workspace.

    Returns:
        Path to workspace root

    Raises:
        FileNotFoundError: If not in a workspace (with helpful message)
    """
    workspace_root = find_workspace_root()
    if workspace_root is None:
        console.print("[red]Error: Not in a BoringPy workspace[/red]")
        console.print("\nYou must be inside a workspace to run this command.")
        console.print("Create a workspace with: [cyan]boringpy init <workspace-name>[/cyan]")
        raise FileNotFoundError("Not in a BoringPy workspace")

    return workspace_root


def add_workspace_member(member_path: str, workspace_root: Path | None = None) -> None:
    """
    Add a new member to the workspace configuration.

    Args:
        member_path: Relative path to the workspace member (e.g., "src/apps/my_api")
        workspace_root: Workspace root directory (auto-detected if None)

    Raises:
        FileNotFoundError: If workspace not found
        ValueError: If boringpy.json is invalid
    """
    config = load_workspace_config(workspace_root)

    # Ensure workspace_members list exists
    if "workspace_members" not in config:
        config["workspace_members"] = []

    # Add member if not already present
    if member_path not in config["workspace_members"]:
        config["workspace_members"].append(member_path)
        save_workspace_config(config, workspace_root)


def create_workspace_config(workspace_root: Path) -> dict[str, Any]:
    """
    Create a new workspace configuration.

    Args:
        workspace_root: Path to the workspace root directory

    Returns:
        New workspace configuration dictionary
    """
    from boringpy import __version__

    return {
        "version": __version__,
        "type": "workspace",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "defaults": {"api": {"db_type": "postgresql", "port": 8000}},
        "workspace_members": [],
    }
