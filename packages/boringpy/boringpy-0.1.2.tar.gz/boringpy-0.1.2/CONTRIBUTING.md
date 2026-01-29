# Contributing to BoringPy

Thank you for your interest in contributing to BoringPy! We welcome contributions from the community.

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Setup Development Environment

1. **Clone the repository**

```bash
git clone https://github.com/gverdugo-g14/boringpy14.git
cd boringpy14
```

2. **Install uv** (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Sync dependencies**

```bash
uv sync
```

4. **Verify installation**

```bash
uv run boringpy --version
```

## 🏗️ Project Structure

```
boringpy14/
├── src/
│   ├── boringpy/          # Main package
│   │   ├── cli/           # CLI commands
│   │   ├── core/          # Core generators & engines
│   │   ├── generators/    # Specific generators (API, lib, etc)
│   │   ├── templates/     # Bundled templates
│   │   └── utils/         # Utility functions
│   └── libs/              # Workspace libraries
├── tests/                 # Test suite (coming soon)
├── docs/                  # Documentation
└── dist/                  # Built packages
```

## 🧪 Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_generator.py
```

## 🎨 Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

### Before committing, always run:

```bash
# Format code
uv run ruff format .

# Lint and auto-fix
uv run ruff check --fix .

# Type check
uv run ty check .

# Run all checks
uv run ruff format . && uv run ruff check --fix . && uv run ty check .
```

### Code Standards

- **Line length**: 88 characters (Black-compatible)
- **Type hints**: Required for all function signatures
- **Docstrings**: Required for public functions (Google style)
- **Imports**: Sorted and grouped (stdlib → third-party → local)
- **Modern Python**: Use Python 3.13+ features

Example:

```python
from pathlib import Path

from rich.console import Console

from boringpy.core.generator import Generator


def create_api(name: str, destination: Path) -> Path:
    """
    Create a new FastAPI application.
    
    Args:
        name: Name of the API package
        destination: Directory where to create the API
    
    Returns:
        Path to the created API directory
    
    Raises:
        ValueError: If name is invalid
    """
    console = Console()
    console.print(f"Creating API: {name}")
    return destination / name
```

## 📝 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
feat(cli): add library generator command
fix(template): correct database URL in docker-compose
docs(readme): update installation instructions
refactor(generator): simplify template rendering logic
test(cli): add tests for init command
```

## 🔧 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clean, documented code
- Follow code style guidelines
- Add tests for new features
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run linting and formatting
uv run ruff format .
uv run ruff check --fix .

# Type check
uv run ty check .

# Run tests
uv run pytest

# Test CLI locally
uv run boringpy init test-workspace
cd test-workspace
uv run boringpy generate api test_api
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat(generator): add model generator"
```

### 5. Push and Create PR

```bash
git push origin feat/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots/demos if applicable

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **BoringPy version**: `boringpy --version`
2. **Python version**: `python --version`
3. **Operating system**
4. **Steps to reproduce**
5. **Expected behavior**
6. **Actual behavior**
7. **Error messages** (full stack trace)

## 💡 Suggesting Features

We love feature suggestions! Please:

1. Check if the feature already exists or is planned
2. Open an issue with the `enhancement` label
3. Describe the use case and expected behavior
4. Provide examples if possible

## 🎯 Areas for Contribution

Looking for ideas? Here are areas we need help with:

### High Priority

- [ ] Add tests for CLI commands
- [ ] Create library generator (`boringpy generate lib`)
- [ ] Add SQLModel generator (`boringpy generate model`)
- [ ] Improve error messages and user feedback
- [ ] Add authentication template options

### Medium Priority

- [ ] CRUD endpoint generator
- [ ] Add more database examples (MongoDB, Redis)
- [ ] Create deployment helpers (Docker, K8s)
- [ ] Shell completion scripts (bash, zsh, fish)
- [ ] Plugin system for custom templates

### Documentation

- [ ] Video tutorials
- [ ] More usage examples
- [ ] Architecture documentation
- [ ] Template creation guide

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [uv Documentation](https://github.com/astral-sh/uv)

## 🤝 Code Review Process

All contributions go through code review:

1. **Automated checks**: CI runs linting, type checking, tests
2. **Maintainer review**: We review code quality, design, documentation
3. **Feedback**: We provide constructive feedback
4. **Iteration**: Make requested changes
5. **Merge**: Once approved, we merge your PR!

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open an Issue
- **Chat**: (Coming soon)

## 🙏 Thank You!

Every contribution makes BoringPy better. We appreciate your time and effort!

---

**Happy coding! 🚀**
