"""Base generator with lifecycle hooks and extensibility."""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from rich.console import Console

from boringpy.core.template_engine import TemplateEngine
from boringpy.core.uv_manager import UvManager

console = Console()


@dataclass
class GeneratorConfig:
    """
    Configuration for a generator.

    Attributes:
        name: Generator name
        description: Generator description
        template_dir: Path to template directory
        variables: Template variables with defaults
        dependencies: Runtime dependencies to install
        dev_dependencies: Development dependencies to install
        use_uv_init: Use `uv init` to create base structure
        init_type: Type for uv init ('app' or 'lib')
        exclude_patterns: Patterns to exclude from template
    """

    name: str
    description: str
    template_dir: Path
    variables: dict[str, Any] = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)
    dev_dependencies: list[str] = field(default_factory=list)
    use_uv_init: bool = True
    init_type: str = "app"  # 'app' or 'lib'
    exclude_patterns: list[str] = field(default_factory=list)

    @classmethod
    def from_template_json(cls, template_dir: Path) -> "GeneratorConfig":
        """
        Load generator config from template.json file.

        Args:
            template_dir: Directory containing template.json

        Returns:
            GeneratorConfig instance

        Raises:
            FileNotFoundError: If template.json not found
            ValueError: If template.json is invalid
        """
        config_path = template_dir / "template.json"

        if not config_path.exists():
            raise FileNotFoundError(f"template.json not found in {template_dir}")

        try:
            data = json.loads(config_path.read_text())

            return cls(
                name=data.get("name", template_dir.name),
                description=data.get("description", ""),
                template_dir=template_dir,
                variables=data.get("variables", {}),
                dependencies=data.get("dependencies", []),
                dev_dependencies=data.get("dev_dependencies", []),
                use_uv_init=data.get("use_uv_init", True),
                init_type=data.get("init_type", "app"),
                exclude_patterns=data.get("exclude_patterns", []),
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid template.json: {e}")


class Generator(ABC):
    """
    Base generator class with lifecycle hooks.

    Provides a framework for code generation with:
    - Lifecycle hooks (pre/post generation)
    - UV package manager integration
    - Template rendering
    - Dependency management
    - Extensibility through inheritance

    Usage:
        class ApiGenerator(Generator):
            def validate_inputs(self, **kwargs) -> dict[str, Any]:
                # Custom validation
                pass

            def post_generate(self, output_dir: Path, variables: dict[str, Any]):
                # Custom post-generation logic
                pass

        gen = ApiGenerator(config)
        gen.generate(
            destination=Path("src/apps"),
            package_name="my_api",
            port=8000
        )
    """

    def __init__(self, config: GeneratorConfig):
        """
        Initialize generator.

        Args:
            config: Generator configuration
        """
        self.config = config
        self.uv = UvManager()
        self.template_engine = TemplateEngine()

    @abstractmethod
    def validate_inputs(self, **kwargs: Any) -> dict[str, Any]:
        """
        Validate and prepare inputs for generation.

        Args:
            **kwargs: User-provided inputs

        Returns:
            Validated and processed variables

        Raises:
            ValueError: If validation fails
        """
        pass

    def pre_generate(self, destination: Path, variables: dict[str, Any]) -> None:
        """
        Hook called before generation starts.

        Override this to add custom pre-generation logic.

        Args:
            destination: Destination directory
            variables: Template variables
        """
        pass

    def post_generate(self, output_dir: Path, variables: dict[str, Any]) -> None:
        """
        Hook called after generation completes.

        Override this to add custom post-generation logic.

        Args:
            output_dir: Generated project directory
            variables: Template variables used
        """
        pass

    def _create_base_structure(self, package_name: str, destination: Path) -> Path:
        """
        Create base project structure using uv init.

        Args:
            package_name: Package name
            destination: Parent directory

        Returns:
            Path to created project

        Raises:
            UvCommandError: If uv init fails
        """
        if self.config.use_uv_init:
            if self.config.init_type == "lib":
                return self.uv.init_lib(package_name, destination)
            else:
                return self.uv.init_app(package_name, destination)
        else:
            # Manual directory creation
            project_dir = destination / package_name
            project_dir.mkdir(parents=True, exist_ok=True)
            console.print(f"[dim]Created directory: {project_dir}[/dim]")
            return project_dir

    def _install_dependencies(self, project_dir: Path) -> None:
        """
        Install dependencies using uv.

        Args:
            project_dir: Project directory

        Raises:
            UvCommandError: If dependency installation fails
        """
        # Install runtime dependencies
        if self.config.dependencies:
            console.print(f"[dim]Installing {len(self.config.dependencies)} dependencies[/dim]")
            self.uv.add_dependencies(
                self.config.dependencies,
                dev=False,
                cwd=project_dir,
            )

        # Install dev dependencies
        if self.config.dev_dependencies:
            console.print(
                f"[dim]Installing {len(self.config.dev_dependencies)} dev dependencies[/dim]"
            )
            self.uv.add_dependencies(
                self.config.dev_dependencies,
                dev=True,
                cwd=project_dir,
            )

        # Sync all dependencies
        self.uv.sync(cwd=project_dir)

    def _render_templates(self, output_dir: Path, variables: dict[str, Any]) -> None:
        """
        Render template files to output directory.

        Args:
            output_dir: Output directory
            variables: Template variables
        """
        self.template_engine.render_template(
            template_dir=self.config.template_dir,
            output_dir=output_dir,
            variables=variables,
            exclude_patterns=self.config.exclude_patterns,
        )

    def generate(self, destination: Path, **kwargs: Any) -> Path:
        """
        Generate project from template.

        This is the main entry point for generation.

        Args:
            destination: Parent directory for generated project
            **kwargs: Template variables and options

        Returns:
            Path to generated project

        Raises:
            ValueError: If validation fails
            UvCommandError: If uv commands fail
            FileNotFoundError: If template not found
        """
        # Validate inputs
        variables = self.validate_inputs(**kwargs)

        # Extract package name (required)
        package_name = variables.get("package_name")
        if not package_name:
            raise ValueError("package_name is required")

        # Pre-generation hook
        self.pre_generate(destination, variables)

        try:
            # Step 1: Create base structure with uv
            console.print(f"[dim]Generating {self.config.name}: {package_name}[/dim]")
            output_dir = self._create_base_structure(package_name, destination)

            # Step 2: Render templates
            console.print("[dim]Rendering templates...[/dim]")
            self._render_templates(output_dir, variables)

            # Step 3: Install dependencies
            console.print("[dim]Installing dependencies...[/dim]")
            self._install_dependencies(output_dir)

            # Post-generation hook
            self.post_generate(output_dir, variables)

            console.print(
                f"[green]✨ {self.config.name} '{package_name}' created successfully![/green]"
            )
            console.print(f"[dim]📁 Location: {output_dir}[/dim]")

            return output_dir

        except Exception as e:
            console.print(f"[red]Generation failed: {e}[/red]")
            raise


class SubGenerator(ABC):
    """
    Base class for sub-generators (e.g., generate model, generate crud).

    Sub-generators work within existing projects to add new components.

    Usage:
        class ModelGenerator(SubGenerator):
            def validate_inputs(self, **kwargs) -> dict[str, Any]:
                # Validate model name, fields, etc.
                pass

            def generate_in_project(self, project_dir: Path, variables: dict):
                # Create model file in project
                pass

        gen = ModelGenerator(config)
        gen.generate(
            project_dir=Path("src/apps/my_api"),
            model_name="User",
            fields={"name": "str", "email": "str"}
        )
    """

    def __init__(self, config: GeneratorConfig):
        """
        Initialize sub-generator.

        Args:
            config: Generator configuration
        """
        self.config = config
        self.template_engine = TemplateEngine()

    @abstractmethod
    def validate_inputs(self, **kwargs: Any) -> dict[str, Any]:
        """
        Validate and prepare inputs.

        Args:
            **kwargs: User-provided inputs

        Returns:
            Validated variables

        Raises:
            ValueError: If validation fails
        """
        pass

    @abstractmethod
    def generate_in_project(
        self, project_dir: Path, variables: dict[str, Any]
    ) -> list[Path]:
        """
        Generate component within existing project.

        Args:
            project_dir: Existing project directory
            variables: Template variables

        Returns:
            List of generated file paths

        Raises:
            FileNotFoundError: If project doesn't exist
        """
        pass

    def generate(self, project_dir: Path, **kwargs: Any) -> list[Path]:
        """
        Generate component in existing project.

        Args:
            project_dir: Existing project directory
            **kwargs: Template variables

        Returns:
            List of generated files

        Raises:
            ValueError: If validation fails
            FileNotFoundError: If project doesn't exist
        """
        if not project_dir.exists():
            raise FileNotFoundError(f"Project directory not found: {project_dir}")

        # Validate inputs
        variables = self.validate_inputs(**kwargs)

        # Generate
        console.print(f"[dim]Generating {self.config.name} in {project_dir.name}[/dim]")
        generated_files = self.generate_in_project(project_dir, variables)

        console.print(f"[green]✨ Generated {len(generated_files)} file(s)[/green]")
        for file in generated_files:
            console.print(f"  [dim]- {file.relative_to(project_dir)}[/dim]")

        return generated_files
