"""Template rendering engine with Jinja2."""

import re
import shutil
from pathlib import Path
from typing import Any

from jinja2 import Template


class TemplateEngine:
    """Simple template engine for rendering files and directories."""

    def render_template(
        self,
        template_dir: Path,
        output_dir: Path,
        variables: dict[str, Any],
        exclude_patterns: list[str] | None = None,
    ) -> None:
        """
        Render a template directory to output directory.

        Args:
            template_dir: Source template directory
            output_dir: Destination directory
            variables: Variables for template rendering
            exclude_patterns: File patterns to exclude
        """
        exclude_patterns = exclude_patterns or []

        if not template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {template_dir}")

        output_dir.mkdir(parents=True, exist_ok=True)

        # Process all files recursively
        for template_file in template_dir.rglob("*"):
            if not template_file.is_file():
                continue

            # Skip excluded files
            rel_path = template_file.relative_to(template_dir)
            if any(rel_path.match(pattern) for pattern in exclude_patterns):
                continue

            # Calculate output path
            output_path = output_dir / rel_path

            # Remove .template extension if present
            if output_path.suffix == ".template":
                output_path = output_path.with_suffix("")

            # Render file
            self._render_file(template_file, output_path, variables)

    def _render_file(
        self, template_file: Path, output_path: Path, variables: dict[str, Any]
    ) -> None:
        """Render a single file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if file should be rendered or copied
        if self._should_render(template_file):
            # Render with Jinja2
            template_content = template_file.read_text(encoding="utf-8")
            template = Template(template_content)
            rendered = template.render(**variables)
            output_path.write_text(rendered, encoding="utf-8")
        else:
            # Copy as-is
            shutil.copy2(template_file, output_path)

    def _should_render(self, file_path: Path) -> bool:
        """Check if file should be rendered with Jinja2."""
        # Always render .template files
        if file_path.suffix == ".template":
            return True

        # Render common text file extensions
        text_extensions = {
            ".py",
            ".toml",
            ".md",
            ".yaml",
            ".yml",
            ".json",
            ".txt",
            ".env",
            ".ini",
            ".cfg",
        }
        if file_path.suffix in text_extensions:
            return True

        # Render .env files
        if file_path.name.startswith(".env"):
            return True

        return False

    def render_string(self, template_string: str, variables: dict[str, Any]) -> str:
        """
        Render a template string.

        Args:
            template_string: Template string with {{variables}}
            variables: Variables for rendering

        Returns:
            Rendered string
        """
        template = Template(template_string)
        return template.render(**variables)
