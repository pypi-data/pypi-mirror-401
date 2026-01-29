# test-boringpy-workspace

BoringPy workspace for modern Python development.

## Structure

```
test-boringpy-workspace/
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

BoringPy v0.1.0
