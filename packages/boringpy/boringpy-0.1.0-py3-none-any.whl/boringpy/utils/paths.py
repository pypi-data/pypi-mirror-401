"""Path utilities for templates and resources."""

from pathlib import Path


def get_templates_dir() -> Path:
    """
    Get the bundled templates directory.

    Returns:
        Path to the templates directory

    Raises:
        FileNotFoundError: If templates directory not found
    """
    # Use __file__ to locate templates relative to this module
    # This works for both editable installs and regular installs
    templates_dir = Path(__file__).parent.parent / "templates"

    if not templates_dir.exists():
        raise FileNotFoundError(
            f"Templates directory not found at {templates_dir}. "
            "This may indicate a corrupted installation."
        )

    return templates_dir


def get_template_path(template_name: str) -> Path:
    """
    Get path to a specific template.

    Args:
        template_name: Name of the template (e.g., "api", "lib", "script")

    Returns:
        Path to the template directory

    Raises:
        FileNotFoundError: If template not found
    """
    templates_dir = get_templates_dir()
    template_path = templates_dir / template_name

    if not template_path.exists():
        available = [
            d.name for d in templates_dir.iterdir() if d.is_dir() and not d.name.startswith(".")
        ]
        raise FileNotFoundError(
            f"Template '{template_name}' not found. Available templates: {', '.join(available)}"
        )

    return template_path


def list_available_templates() -> list[str]:
    """
    List all available templates.

    Returns:
        List of template names
    """
    templates_dir = get_templates_dir()
    return [d.name for d in templates_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
