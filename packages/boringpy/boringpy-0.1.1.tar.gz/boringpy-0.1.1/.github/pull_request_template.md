# Pull Request

## 📝 Description

Provide a clear description of what this PR does.

## 🔗 Related Issues

Fixes #(issue number)
Closes #(issue number)

## 🎯 Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Style/formatting change (no functional changes)
- [ ] ♻️ Code refactoring
- [ ] 🧪 Test addition or update
- [ ] 🔧 Configuration change

## ✅ Checklist

Before submitting, please ensure:

- [ ] My code follows the project's code style (`ruff format`, `ruff check`)
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have added/updated docstrings for public functions
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## 🧪 Testing

Describe the tests you ran to verify your changes:

```bash
# Example commands
uv run boringpy init test-workspace
cd test-workspace
uv run boringpy generate api test_api
cd src/apps/test_api
make docker-up
make test
```

**Test Configuration:**
- Python version: 3.13
- OS: macOS / Linux / Windows
- uv version: 0.4.0

## 📸 Screenshots / Demo

If applicable, add screenshots or GIFs showing the changes:

## 🔍 Code Quality

- [ ] Ran `uv run ruff format .`
- [ ] Ran `uv run ruff check --fix .`
- [ ] Ran `uv run ty check .`
- [ ] Tested in clean environment

## 📚 Documentation

What documentation did you update?

- [ ] README.md
- [ ] CONTRIBUTING.md
- [ ] CHANGELOG.md
- [ ] Docstrings
- [ ] Other: ___

## 💡 Additional Notes

Any additional information or context about the PR:

---

**Thank you for contributing to BoringPy! 🎉**
