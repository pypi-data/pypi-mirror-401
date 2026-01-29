# BoringPy Templates

This directory contains scaffolding templates for BoringPy.

## 📁 Directory Structure

```
templates/
├── api/                    # FastAPI application template
│   ├── template.json       # Template metadata and configuration
│   ├── pyproject.toml.template
│   ├── README.md.template
│   ├── __package_name__/   # Package directory (name is variable)
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   └── routes/
│   └── tests/
│       └── test_main.py
├── lib/                    # Library template
└── script/                 # Script template
```

## 🎯 How It Works

### 1. Template Structure

Each template directory contains:
- **`template.json`**: Metadata and variable definitions
- **`.template` files**: Files that need variable substitution
- **Regular files**: Files that are copied as-is
- **`__variable_name__` directories**: Directories that get renamed

### 2. Variable Substitution

Variables are defined in `template.json` and can be used in:
- File contents using Jinja2 syntax: `{{variable_name}}`
- Directory names: `__variable_name__`
- File names: `file_{{variable_name}}.py`

### 3. Template Variables

Common variables:
- `package_name`: The Python package name (snake_case)
- `display_name`: Human-readable name
- `version`: Initial version number
- `port`: Default port for APIs

## 📝 Example: API Template

### template.json
```json
{
  "name": "api",
  "variables": {
    "package_name": {
      "required": true,
      "pattern": "^[a-z][a-z0-9_]*$"
    },
    "port": {
      "default": 8000
    }
  }
}
```

### Using Variables in Files

**pyproject.toml.template:**
```toml
[project]
name = "{{package_name}}"
version = "{{version}}"
```

**main.py:**
```python
from {{package_name}}.config import settings
```

### Directory Naming

`__package_name__/` → `my_api/` (when package_name="my_api")

## 🔧 Creating a New Template

1. Create a new directory under `templates/`
2. Add `template.json` with metadata
3. Create your template files (use `.template` extension for files needing substitution)
4. Use `{{variable_name}}` for variable substitution
5. Use `__variable_name__` for directory/file names that should be replaced

## 🚀 Usage (Future CLI)

```bash
# Create new API from template
boringpy new api my_awesome_api --port 8080

# Create new library from template
boringpy new lib my_library

# List available templates
boringpy templates list
```

## 🎨 Template Best Practices

1. **Keep it simple**: Templates should be minimal but functional
2. **Use meaningful defaults**: Provide sensible defaults for optional variables
3. **Document variables**: Add descriptions in template.json
4. **Test the output**: Ensure generated code works out of the box
5. **Follow conventions**: Match the project's code style (ruff, ty, pytest)
6. **Include tests**: Every template should include basic tests
7. **Add README**: Include a README.md.template explaining the generated code

## 📋 Template Checklist

- [ ] `template.json` with all required metadata
- [ ] Variable names are clear and follow conventions
- [ ] All files that need substitution have `.template` extension
- [ ] Generated code passes `ruff format` and `ruff check`
- [ ] Generated code passes `ty check`
- [ ] Tests are included and pass
- [ ] README explains how to use the generated code
- [ ] Dependencies are specified in pyproject.toml.template
