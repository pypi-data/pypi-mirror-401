# Changelog

All notable changes to BoringPy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-16

### Added

- **Initial Release** 🎉
- CLI with `boringpy` command
- `boringpy init <workspace>` - Initialize workspace with UV monorepo structure
- `boringpy generate api <name>` - Generate complete FastAPI application
- Multi-database support: PostgreSQL, MySQL, SQLite
- Docker & docker-compose configuration
- Alembic database migrations setup
- SQLModel ORM integration
- Loguru structured logging with request tracing
- Environment-based configuration with Pydantic Settings
- Professional Makefile with 30+ commands
- pytest test infrastructure
- Health check endpoints
- API documentation (Swagger/ReDoc)
- Type-safe code with full type annotations
- Ruff formatting and linting configuration
- Template engine with Jinja2
- Workspace member management

### Template Features

- Multi-stage Dockerfile for production builds
- Docker Compose with hot reload for development
- Alembic migrations pre-configured
- Structured application layout (core, models, api, services)
- Example SQLModel with CRUD operations
- Request ID tracing for distributed systems
- Global exception handling
- Comprehensive README for generated projects

### Developer Experience

- Rich CLI output with colors and formatting
- Progress indicators for long operations
- Clear error messages and validation
- Auto-installation of dependencies with UV
- Git initialization for generated projects

### Infrastructure

- Published to PyPI: https://pypi.org/project/boringpy/
- GitHub repository: https://github.com/gverdugo-g14/boringpy14
- MIT License
- Python 3.13+ support
- UV workspace compatibility

## [Unreleased]

### Planned

- Library generator (`boringpy generate lib`)
- SQLModel generator (`boringpy generate model`)
- CRUD endpoint generator
- Authentication templates
- AWS/GCP deployment helpers
- Plugin system for custom templates
- Shell completion scripts

---

[0.1.0]: https://github.com/gverdugo-g14/boringpy14/releases/tag/v0.1.0
