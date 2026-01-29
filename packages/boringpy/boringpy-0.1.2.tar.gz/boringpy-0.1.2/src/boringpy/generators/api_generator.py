"""FastAPI application generator."""

import re
from pathlib import Path
from typing import Any

from rich.console import Console

from boringpy.core.generator import Generator

console = Console()


class ApiGenerator(Generator):
    """
    Generator for FastAPI applications with database support.

    Creates a production-ready FastAPI application with:
    - SQLModel database configuration
    - Loguru logging with request tracking
    - Environment-based configuration
    - Test infrastructure with pytest
    - Modern Python 3.13+ with type checking
    """

    # Valid Python package name pattern
    PACKAGE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

    # Valid port range
    MIN_PORT = 1024
    MAX_PORT = 65535

    def validate_inputs(self, **kwargs: Any) -> dict[str, Any]:
        """
        Validate and normalize input variables for API generation.

        Args:
            **kwargs: Input variables including:
                - package_name (required): Name of the API package
                - port (optional): API port number, defaults to 8000
                - display_name (optional): Human-readable name
                - version (optional): API version, defaults to "0.1.0"

        Returns:
            Validated and normalized variables dictionary

        Raises:
            ValueError: If package_name is invalid or port is out of range
        """
        # Validate package_name (required)
        package_name = kwargs.get("package_name")
        if not package_name:
            raise ValueError("package_name is required")

        if not isinstance(package_name, str):
            raise ValueError(f"package_name must be a string, got {type(package_name)}")

        if not self.PACKAGE_NAME_PATTERN.match(package_name):
            raise ValueError(
                f"Invalid package_name '{package_name}'. "
                "Must start with lowercase letter and contain only lowercase letters, "
                "numbers, and underscores."
            )

        # Validate port (optional, defaults to 8000)
        port = kwargs.get("port", 8000)
        if isinstance(port, str):
            try:
                port = int(port)
            except ValueError:
                raise ValueError(f"Invalid port '{port}'. Must be a number.")

        if not isinstance(port, int):
            raise ValueError(f"port must be an integer, got {type(port)}")

        if not (self.MIN_PORT <= port <= self.MAX_PORT):
            raise ValueError(
                f"port {port} is out of valid range ({self.MIN_PORT}-{self.MAX_PORT})"
            )

        # Generate defaults
        display_name = kwargs.get(
            "display_name", package_name.replace("_", " ").title()
        )
        version = kwargs.get("version", "0.1.0")

        # Validate and configure database type
        db_type = kwargs.get("db_type", "postgresql")
        valid_db_types = ["postgresql", "mysql", "sqlite"]

        if db_type not in valid_db_types:
            raise ValueError(
                f"Invalid db_type '{db_type}'. Must be one of: {', '.join(valid_db_types)}"
            )

        # Calculate database URLs based on db_type
        if db_type == "postgresql":
            database_url = kwargs.get(
                "database_url",
                f"postgresql://{package_name}:devpassword@localhost:5432/{package_name}_db",
            )
            docker_database_url = f"postgresql://{package_name}:devpassword@postgres:5432/{package_name}_db"
        elif db_type == "mysql":
            database_url = kwargs.get(
                "database_url",
                f"mysql://{package_name}:devpassword@localhost:3306/{package_name}_db",
            )
            docker_database_url = (
                f"mysql://{package_name}:devpassword@mysql:3306/{package_name}_db"
            )
        else:  # sqlite
            database_url = kwargs.get("database_url", f"sqlite:///./{package_name}.db")
            docker_database_url = f"sqlite:////app/data/{package_name}.db"

        db_echo = kwargs.get("db_echo", False)
        db_pool_size = kwargs.get("db_pool_size", 5)
        db_max_overflow = kwargs.get("db_max_overflow", 10)

        validated = {
            "package_name": package_name,
            "port": port,
            "display_name": display_name,
            "version": version,
            "db_type": db_type,
            "database_url": database_url,
            "docker_database_url": docker_database_url,
            "db_echo": db_echo,
            "db_pool_size": db_pool_size,
            "db_max_overflow": db_max_overflow,
        }

        console.print(f"[dim]Validated inputs: {validated}[/dim]", style="dim")
        return validated

    def pre_generate(self, destination: Path, variables: dict[str, Any]) -> None:
        """
        Hook executed before generation starts.

        Args:
            destination: Target directory for the API
            variables: Validated template variables
        """
        console.print(
            f"[dim]Preparing to generate FastAPI app '{variables['package_name']}' "
            f"on port {variables['port']}[/dim]"
        )

        # Check if destination already exists
        target_dir = destination / variables["package_name"]
        if target_dir.exists():
            console.print(f"[yellow]Warning: Directory {target_dir} already exists[/yellow]")

    def post_generate(self, output_dir: Path, variables: dict[str, Any]) -> None:
        """
        Hook executed after generation completes.

        Logs success information and next steps.

        Args:
            output_dir: The generated API directory
            variables: Template variables used for generation
        """
        # This is now handled in the generate command to show rich panels
        # Just keep it simple here
        pass
