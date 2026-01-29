"""Script to test API scaffolding - simulates 'boringpy new api' command."""

import json
import re
import shutil
import subprocess
from pathlib import Path

from jinja2 import Template
from lib_boring_logger import logger


def validate_package_name(name: str) -> bool:
    """Validate package name follows Python conventions."""
    pattern = r"^[a-z][a-z0-9_]*$"
    return bool(re.match(pattern, name))


def render_template_file(template_path: Path, variables: dict[str, str | int]) -> str:
    """Render a Jinja2 template file."""
    template_content = template_path.read_text()
    template = Template(template_content)
    return template.render(**variables)


def replace_variable_in_path(path_part: str, variables: dict[str, str | int]) -> str:
    """Replace __variable_name__ with actual value."""
    for var_name, var_value in variables.items():
        placeholder = f"__{var_name}__"
        if placeholder in path_part:
            return path_part.replace(placeholder, str(var_value))
    return path_part


def scaffold_api(
    package_name: str,
    destination: Path,
    port: int = 8000,
    version: str = "0.1.0",
) -> Path:
    """
    Scaffold a new FastAPI application from template.

    Args:
        package_name: Name of the API package (snake_case)
        destination: Parent directory where to create the app
        port: Default port for the API
        version: Initial version number

    Returns:
        Path to the created application

    Raises:
        ValueError: If package name is invalid
        FileExistsError: If destination already exists
    """
    # Validate package name
    if not validate_package_name(package_name):
        raise ValueError(
            f"Invalid package name: {package_name}. "
            "Must be lowercase with underscores only."
        )

    # Prepare destination
    app_dir = destination / package_name
    if app_dir.exists():
        raise FileExistsError(f"Directory already exists: {app_dir}")

    logger.info(f"Creating FastAPI app: {package_name}")

    # Load template config
    template_dir = Path(__file__).parent.parent.parent / "templates" / "api"
    template_config_path = template_dir / "template.json"

    if not template_config_path.exists():
        raise FileNotFoundError(f"Template config not found: {template_config_path}")

    template_config = json.loads(template_config_path.read_text())
    logger.debug(f"Loaded template config: {template_config['name']}")

    # Prepare variables
    variables = {
        "package_name": package_name,
        "display_name": package_name.replace("_", " ").title(),
        "port": port,
        "version": version,
    }

    logger.info(f"Variables: {variables}")

    # Create app directory
    app_dir.mkdir(parents=True)
    logger.success(f"Created directory: {app_dir}")

    # Process all files in template

    for template_file in template_dir.rglob("*"):
        if template_file.is_file() and template_file.name != "template.json":
            # Calculate relative path
            rel_path = template_file.relative_to(template_dir)

            # Replace variables in path
            path_parts = list(rel_path.parts)
            path_parts = [
                replace_variable_in_path(part, variables) for part in path_parts
            ]
            dest_rel_path = Path(*path_parts)

            # Remove .template extension if present
            if dest_rel_path.suffix == ".template":
                dest_rel_path = dest_rel_path.with_suffix("")

            dest_file = app_dir / dest_rel_path

            # Create parent directories
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Check if file needs rendering
            # Render all Python files, .template files, and common config files
            needs_rendering = template_file.suffix in [
                ".py",
                ".template",
                ".md",
                ".toml",
                ".example",
            ] or template_file.name in ["README.md", ".env.example"]

            if needs_rendering:
                # Render template
                try:
                    content = render_template_file(template_file, variables)
                    dest_file.write_text(content)
                    logger.debug(f"Rendered: {dest_rel_path}")
                except Exception as e:
                    logger.error(f"Failed to render {template_file}: {e}")
                    raise
            else:
                # Copy file as-is
                shutil.copy2(template_file, dest_file)
                logger.debug(f"Copied: {dest_rel_path}")

    logger.success(f"Scaffolded files to {app_dir}")

    # Add to workspace
    logger.info("Adding to workspace...")
    workspace_config = Path("pyproject.toml")
    if workspace_config.exists():
        content = workspace_config.read_text()
        app_dir_str = str(app_dir)
        # Simple append to members (you might want to parse TOML properly)
        if f'"{app_dir_str}"' not in content:
            # This is a simple approach - in production use tomli/tomllib
            content = content.replace(
                "members = [",
                f'members = [\n    "{app_dir_str}",',
            )
            workspace_config.write_text(content)
            logger.success("Added to workspace")

    # Run post-scaffold commands
    post_commands = template_config.get("post_scaffold_commands", [])
    for command in post_commands:
        logger.info(f"Running: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=app_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            logger.success(f"Command completed: {command}")
            if result.stdout:
                logger.debug(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {command}")
            logger.error(e.stderr)
            raise

    logger.success(f"✨ API '{package_name}' created successfully!")
    logger.info(f"📁 Location: {app_dir}")
    logger.info(
        f"🚀 Run with: cd {app_dir} && uv run uvicorn app.main:app --reload --port {port}"
    )

    return app_dir


def main() -> None:
    """Main entry point for testing."""
    import sys

    if len(sys.argv) < 2:
        logger.error(
            "Usage: uv run python src/scripts/scaffold_api.py <package_name> [port]"
        )
        logger.info(
            "Example: uv run python src/scripts/scaffold_api.py my_awesome_api 8080"
        )
        sys.exit(1)

    package_name = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    try:
        destination = Path("src/apps")
        destination.mkdir(parents=True, exist_ok=True)

        scaffold_api(package_name, destination, port=port)

        logger.success("🎉 Done! Your API is ready to use.")
        logger.info("Next steps:")
        logger.info(f"  1. cd src/apps/{package_name}")
        logger.info(f"  2. uv run uvicorn app.main:app --reload --port {port}")
        logger.info(f"  3. Open http://localhost:{port}/docs")

    except Exception as e:
        logger.error(f"Failed to scaffold API: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
