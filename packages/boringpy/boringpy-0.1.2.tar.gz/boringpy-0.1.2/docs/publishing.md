# Publishing BoringPy to PyPI

## Prerequisites

1. **PyPI Account**
   - Create account at https://pypi.org/account/register/
   - Verify your email
   - Enable 2FA (required for new packages)

2. **TestPyPI Account** (for testing)
   - Create account at https://test.pypi.org/account/register/
   - Verify email

3. **API Tokens**
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - Save tokens securely!

## Step 1: Install Publishing Tools

```bash
pip install twine
```

## Step 2: Build the Package

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build wheel and source distribution
uv run python -m build

# Verify build
ls -lh dist/
# Should show:
# - boringpy-0.1.0-py3-none-any.whl
# - boringpy-0.1.0.tar.gz
```

## Step 3: Check Package

```bash
# Check package for common issues
twine check dist/*
```

## Step 4: Test with TestPyPI (RECOMMENDED)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# You'll be prompted for:
# Username: __token__
# Password: pypi-YOUR_TEST_API_TOKEN

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ boringpy

# Test the CLI
boringpy --version
boringpy init test-workspace
cd test-workspace
boringpy generate api test_api
```

**Note**: `--extra-index-url https://pypi.org/simple/` is needed because TestPyPI doesn't have all dependencies (jinja2, typer, rich).

## Step 5: Publish to PyPI (Production)

```bash
# Upload to production PyPI
twine upload dist/*

# You'll be prompted for:
# Username: __token__
# Password: pypi-YOUR_REAL_API_TOKEN
```

## Step 6: Verify on PyPI

1. Visit https://pypi.org/project/boringpy/
2. Check that:
   - README renders correctly
   - All metadata is correct
   - Version is correct
   - Links work

## Step 7: Test Real Installation

```bash
# Create fresh environment
python -m venv test-env
source test-env/bin/activate

# Install from PyPI
pip install boringpy

# Test
boringpy --version
boringpy init my-project
cd my-project
boringpy generate api my_api --port 8000 --db postgresql
```

## Configure API Tokens (One-Time Setup)

### Option 1: `.pypirc` file

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_REAL_API_TOKEN

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_API_TOKEN
```

```bash
chmod 600 ~/.pypirc
```

### Option 2: Environment Variables

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_API_TOKEN
```

### Option 3: Command-line (most secure)

```bash
twine upload dist/* -u __token__ -p pypi-YOUR_API_TOKEN
```

## Updating the Package

When releasing a new version:

1. **Update version** in `src/boringpy/__init__.py`:
   ```python
   __version__ = "0.2.0"
   ```

2. **Update version** in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

3. **Rebuild**:
   ```bash
   rm -rf dist/
   uv run python -m build
   ```

4. **Check**:
   ```bash
   twine check dist/*
   ```

5. **Upload**:
   ```bash
   twine upload dist/*
   ```

## Troubleshooting

### "File already exists"

PyPI doesn't allow reuploading the same version. Either:
- Bump the version number
- Delete the `dist/` folder and rebuild

### "Invalid credentials"

- Make sure you're using `__token__` as username (two underscores)
- Check that you copied the full token (starts with `pypi-`)
- Verify the token hasn't expired

### "README rendering issues"

- Test locally: `pip install readme-renderer[md]`
- Check: `python -m readme_renderer README.md`
- Common issues:
  - Invalid markdown syntax
  - Broken links
  - Missing images

### "Missing dependencies"

If dependencies aren't installing:
- Check `pyproject.toml` has correct dependency versions
- Verify dependencies exist on PyPI
- For local workspace dependencies, they must also be on PyPI

## Version Numbering

Follow semantic versioning (SemVer):
- **0.1.0** - Initial release
- **0.1.1** - Bug fixes
- **0.2.0** - New features (backward compatible)
- **1.0.0** - Stable API, production ready
- **2.0.0** - Breaking changes

## Current Package Info

- **Package Name**: `boringpy`
- **Current Version**: `0.1.0`
- **Author**: BoringPy Contributors
- **License**: MIT
- **Python**: >=3.13
- **Homepage**: https://github.com/yourusername/boringpy

## Security Best Practices

1. **Never commit API tokens** to git
2. **Add `.pypirc` to `.gitignore`**
3. **Use scoped tokens** (project-specific, not account-wide)
4. **Rotate tokens** regularly
5. **Enable 2FA** on PyPI account
6. **Review package contents** before uploading

## Useful Commands

```bash
# Check what's in the wheel
unzip -l dist/boringpy-0.1.0-py3-none-any.whl

# Check what's in the tarball
tar -tzf dist/boringpy-0.1.0.tar.gz

# Validate package metadata
twine check dist/*

# View package on TestPyPI
open https://test.pypi.org/project/boringpy/

# View package on PyPI
open https://pypi.org/project/boringpy/
```

## Next Steps After Publishing

1. ✅ Update GitHub repo with new tag
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. ✅ Create GitHub release
   - Go to https://github.com/yourusername/boringpy/releases
   - Click "Create a new release"
   - Select the tag you just created
   - Add release notes

3. ✅ Update documentation
   - Add installation instructions
   - Update examples
   - Add changelog

4. ✅ Announce
   - Reddit (r/Python)
   - Twitter/X
   - Dev.to blog post
   - HackerNews

## Resources

- **PyPI**: https://pypi.org/
- **TestPyPI**: https://test.pypi.org/
- **Packaging Guide**: https://packaging.python.org/
- **Twine Docs**: https://twine.readthedocs.io/
- **PEP 517/518**: Build system standards
