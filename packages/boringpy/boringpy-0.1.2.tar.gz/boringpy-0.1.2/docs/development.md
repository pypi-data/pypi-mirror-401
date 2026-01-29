# BoringPy Development Guide for AI Agents

## Project Overview
BoringPy is a modern Python scaffolding framework for rapid project setup. It provides CLI commands to scaffold Python projects, APIs, libraries, and more using modern tooling from Astral (uv, ruff, ty).

**Goals:**
- CLI commands: `boringpy init`, `boringpy new api`, `boringpy new lib`
- Use FastAPI for all API scaffolding
- Leverage uv workspaces for project organization
- Modern Python 3.13+ with strict type checking
- Loguru for structured logging
- Configuration via `boringpy.json`

## Project Structure
```
src/
├── apps/      # FastAPI applications (generated from templates)
├── libs/      # Reusable libraries (e.g., lib_boring_logger)
└── scripts/   # Utility scripts
templates/     # Scaffolding templates
├── api/       # FastAPI app template
├── lib/       # Library template
└── script/    # Script template
boringpy.json  # Project configuration
```

## Essential Commands

### Package Management
```bash
# Install dependencies
uv sync

# Add runtime dependency
uv add <package>

# Add dev dependency
uv add --dev <package>

# Run command in venv
uv run <command>
```

### Linting & Formatting
```bash
# Format code (do this first, always)
uv run ruff format .

# Check formatting (dry-run)
uv run ruff format --check .

# Lint code
uv run ruff check .

# Lint and auto-fix
uv run ruff check --fix .

# Lint specific file
uv run ruff check src/apps/my_api/main.py
```

### Type Checking
```bash
# Type check entire project
uv run ty check .

# Type check specific file
uv run ty check src/apps/my_api/main.py

# Type check specific directory
uv run ty check src/libs/lib_boring_logger
```

### Testing (pytest)
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_logger.py

# Run single test function
uv run pytest tests/test_logger.py::test_create_logger

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run tests matching pattern
uv run pytest -k "test_api"

# Run with stdout visible (useful for debugging)
uv run pytest -s
```

### Full Quality Check (Pre-commit)
```bash
# Run all checks before commit
uv run ruff format . && uv run ruff check --fix . && uv run ty check . && uv run pytest
```

## Code Style Guidelines

### Imports
- Use absolute imports from project root
- Group imports: stdlib → third-party → local
- Sort alphabetically within groups
- Use `from typing import` for type hints (when needed)

```python
# Standard library
import os
from pathlib import Path

# Third-party
from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel

# Local
from lib_boring_logger import logger
from boringpy.core import scaffold
```

### Formatting (Ruff - 88 chars)
- Line length: 88 characters (Black-compatible)
- Use double quotes for strings
- Trailing commas in multi-line structures
- Ruff handles all formatting automatically - just run `ruff format`

### Type Annotations (ty)
- **Always** use type hints for function signatures
- Use modern Python 3.13+ type syntax (`list[str]` not `List[str]`)
- Use `None` for optional return types
- Type all function parameters and returns
- Avoid `type: ignore` - fix the underlying issue

```python
# Good - Modern Python 3.13+ syntax
def create_api(name: str, path: Path) -> dict[str, str]:
    return {"name": name, "path": str(path)}

def get_configs() -> list[dict[str, str | int]]:
    return [{"name": "api1", "port": 8000}]

# Bad - no types
def create_api(name, path):
    return {"name": name, "path": str(path)}
```

### Naming Conventions
- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`
- **Files/modules**: `snake_case.py`

```python
# Constants
DEFAULT_API_PORT = 8000
MAX_RETRIES = 3

# Classes
class ApiScaffolder:
    def __init__(self) -> None:
        self._config: dict[str, str] = {}
    
    def scaffold_api(self, name: str) -> None:
        pass

# Functions
def create_workspace(workspace_name: str) -> Path:
    pass
```

### Error Handling
- Use specific exception types (never bare `except:`)
- Raise built-in exceptions or create custom ones
- Include context in error messages
- Log errors before raising when appropriate
- Use FastAPI's HTTPException for API errors

```python
from lib_boring_logger import logger

# Good - specific exceptions with context
def load_config(path: Path) -> dict[str, str]:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as e:
        logger.error(f"Config file not found: {path}")
        raise FileNotFoundError(f"Config not found: {path}") from e
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config: {path}")
        raise ValueError(f"Invalid JSON in {path}") from e

# FastAPI endpoints
@app.get("/api/{api_id}")
async def get_api(api_id: str) -> dict[str, str]:
    if not api_exists(api_id):
        logger.warning(f"API not found: {api_id}")
        raise HTTPException(status_code=404, detail=f"API {api_id} not found")
    return {"id": api_id}
```

### Logging (Loguru)
- Use the `lib_boring_logger` library for terminal output
- Import and use directly: `from lib_boring_logger import logger`
- Log levels: `debug`, `info`, `success`, `warning`, `error`, `critical`
- Clean, colorized output perfect for CLI tools

```python
from lib_boring_logger import logger

# Simple usage - just import and log!
logger.info(f"Scaffolding new API: {api_name}")
logger.success(f"API created successfully!")
logger.debug(f"Config loaded from: {config_path}")
logger.warning(f"Deprecated feature used: {feature_name}")
logger.error(f"Failed to create workspace: {error_msg}")

# Change log level if needed
from lib_boring_logger import LoggerFactory
debug_logger = LoggerFactory.get_logger(level="DEBUG")
debug_logger.debug("Now showing debug messages")
```

### Docstrings
- Use triple-quoted strings for all public functions/classes
- Follow Google style
- Include Args, Returns, Raises sections for functions
- Keep it concise but informative

```python
def scaffold_fastapi_app(name: str, destination: Path) -> Path:
    """
    Create a new FastAPI application using uv workspace.
    
    Args:
        name: Name of the API application
        destination: Parent directory for the new app
    
    Returns:
        Path to the created application
    
    Raises:
        ValueError: If name is invalid or destination doesn't exist
        RuntimeError: If uv init command fails
    """
    pass
```

## Workspace Conventions

### Creating New Apps (FastAPI)
```bash
cd src/apps
uv init {api_name} --app
```
- Each app is a standalone FastAPI application
- Must have its own `pyproject.toml`
- Can depend on `src/libs` libraries

### Creating New Libraries
```bash
cd src/libs
uv init {lib_name} --lib
```
- Libraries are reusable modules
- Example: `lib_boring_logger`, `lib_database`, `lib_auth`
- Must have clear public APIs

### Dependencies Between Workspaces
- Add workspace dependencies in `pyproject.toml`
- Use relative paths for local workspace members
- Example: `lib-boring-logger = { path = "../libs/lib_boring_logger" }`

## Configuration (boringpy.json)

BoringPy projects use a `boringpy.json` file for configuration:

```json
{
  "project_name": "my_project",
  "python_version": "3.13",
  "logging": {
    "level": "INFO",
    "format": "{time} | {level} | {message}",
    "rotation": "10 MB"
  },
  "apis": {
    "default_port": 8000,
    "cors_enabled": true
  }
}
```

## Scaffolding System

### Template Structure

Templates are located in the `templates/` directory. Each template contains:

1. **`template.json`**: Metadata and variable definitions
2. **`.template` files**: Files requiring variable substitution
3. **Regular files**: Copied as-is
4. **`__variable_name__` directories**: Renamed based on variables

### Template Variables

Variables are defined in `template.json` and used with Jinja2 syntax:

```json
{
  "name": "api",
  "variables": {
    "package_name": {
      "description": "Name of the API package",
      "required": true,
      "pattern": "^[a-z][a-z0-9_]*$"
    },
    "port": {
      "default": 8000
    }
  }
}
```

### Using Variables in Templates

**In file contents:**
```python
# {{package_name}}/main.py
from {{package_name}}.config import settings

app = FastAPI(title="{{display_name}}")
```

**In directory names:**
```
__package_name__/  →  my_api/  (when package_name="my_api")
```

**In file names:**
```
{{package_name}}_config.py  →  my_api_config.py
```

### Creating New Templates

1. Create directory in `templates/`
2. Add `template.json` with metadata
3. Create template files (use `.template` for files needing substitution)
4. Use `{{variable_name}}` for substitutions
5. Use `__variable_name__` for dynamic directory names

### Template Best Practices

- Keep templates minimal but functional
- Provide sensible defaults
- Include tests in templates
- Follow project code style
- Add README explaining generated code
- Test that generated code works out of the box

## Best Practices

1. **Always run ruff format before committing** - formatting is non-negotiable
2. **Type check with ty** - no `type: ignore` without detailed comments explaining why
3. **Use uv for all package management** - no pip, poetry, or conda
4. **FastAPI for all APIs** - consistent framework across all apps
5. **Path objects over strings** - use `pathlib.Path` for file operations
6. **Async by default for APIs** - use `async def` in FastAPI endpoints
7. **Validate with Pydantic** - use `BaseModel` for data validation
8. **Log important operations** - use loguru via `lib_boring_logger`
9. **Test coverage** - aim for >80% coverage on critical code
10. **Workspace isolation** - each app/lib should be independently testable

## Pre-commit Checklist
Before committing code, ensure:
- [ ] `uv run ruff format .` - code is formatted
- [ ] `uv run ruff check --fix .` - no linting errors
- [ ] `uv run ty check .` - no type errors
- [ ] `uv run pytest` - all tests pass
- [ ] All functions have type annotations
- [ ] Public APIs have docstrings
- [ ] Error handling is in place
- [ ] Logging added for important operations
- [ ] No sensitive data in code or logs

## Common Patterns

### Creating a New FastAPI App
```python
from fastapi import FastAPI
from lib_boring_logger import logger

logger.info("Initializing FastAPI application")
app = FastAPI(title="My API")

@app.get("/")
async def root() -> dict[str, str]:
    logger.info("Root endpoint accessed")
    return {"message": "Hello from BoringPy"}
```

### Loading boringpy.json Configuration
```python
import json
from pathlib import Path

def load_boringpy_config() -> dict[str, str | int | dict]:
    config_path = Path("boringpy.json")
    if not config_path.exists():
        raise FileNotFoundError("boringpy.json not found in project root")
    return json.loads(config_path.read_text())
```

### Using lib_boring_logger
```python
from lib_boring_logger import logger

# Use it throughout your module
logger.info("Operation started")
logger.success("Operation completed successfully")
logger.error("Operation failed")
```

### Scaffolding from Templates
```python
from pathlib import Path
import json
import shutil
from jinja2 import Template

def scaffold_from_template(
    template_name: str,
    destination: Path,
    variables: dict[str, str | int]
) -> Path:
    """
    Generate code from a template.
    
    Args:
        template_name: Name of the template (e.g., "api")
        destination: Where to create the scaffolded code
        variables: Template variables to substitute
    
    Returns:
        Path to the created project
    """
    template_dir = Path("templates") / template_name
    
    # Load template config
    config = json.loads((template_dir / "template.json").read_text())
    
    # Render and copy files
    for file_path in template_dir.rglob("*"):
        if file_path.is_file() and file_path.name != "template.json":
            # Handle .template files with Jinja2
            if file_path.suffix == ".template":
                template = Template(file_path.read_text())
                content = template.render(**variables)
                # Write without .template extension
                dest_file = destination / file_path.stem
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                dest_file.write_text(content)
            else:
                # Copy regular files as-is
                dest_file = destination / file_path.relative_to(template_dir)
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_file)
    
    logger.success(f"Scaffolded {template_name} to {destination}")
    return destination
```
