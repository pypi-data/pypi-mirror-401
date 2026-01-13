# Publishing HOLE Fonts to PyPI

**Purpose**: Guide for publishing hole-fonts package to PyPI
**Audience**: Project maintainers
**Status**: Ready for first publish

---

## Prerequisites

### 1. PyPI Account

Create accounts on:
- **PyPI** (production): https://pypi.org/account/register/
- **TestPyPI** (testing): https://test.pypi.org/account/register/

### 2. API Tokens

Generate API tokens for publishing:

**PyPI**:
1. Go to https://pypi.org/manage/account/token/
2. Create token with scope "Entire account"
3. Save token securely (starts with `pypi-`)

**TestPyPI**:
1. Go to https://test.pypi.org/manage/account/token/
2. Create token
3. Save token securely

### 3. Install Publishing Tools

```bash
# Install build tools
uv pip install build twine

# Or using pip
pip install build twine
```

---

## Publishing Workflow

### Step 1: Prepare Release

```bash
# Update version in pyproject.toml
# Current: version = "0.1.0"
# New: version = "2.0.0"

# Update CHANGELOG.md with release notes

# Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 2.0.0"
git tag v2.0.0
git push origin HOLE-FONTS-Ext --tags
```

### Step 2: Clean Build

```bash
# Remove old builds
rm -rf dist/ build/ *.egg-info

# Build package
uv build
# Creates:
#   dist/hole_fonts-2.0.0.tar.gz (source)
#   dist/hole_fonts-2.0.0-py3-none-any.whl (wheel)
```

### Step 3: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# When prompted, use:
# Username: __token__
# Password: <your TestPyPI token>

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ hole-fonts

# Verify it works
hole-fonts --help
```

### Step 4: Publish to PyPI

```bash
# Upload to PyPI
twine upload dist/*

# When prompted, use:
# Username: __token__
# Password: <your PyPI token>

# Or use environment variables
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<your-pypi-token>
twine upload dist/*
```

### Step 5: Verify Publication

```bash
# Check package page
# https://pypi.org/project/hole-fonts/

# Test installation
pip install hole-fonts

# Verify version
hole-fonts --help
pip show hole-fonts
```

---

## Using .pypirc for Authentication

Create `~/.pypirc` to avoid entering credentials:

```ini
[pypi]
username = __token__
password = pypi-your-pypi-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
```

**Security**:
- Set permissions: `chmod 600 ~/.pypirc`
- Never commit this file to git

Then publish with:
```bash
twine upload dist/*
```

---

## GitHub Actions Automation (Future)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.13'

    - name: Install dependencies
      run: |
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: twine upload dist/*
```

**Setup**:
1. Add PyPI token to GitHub Secrets as `PYPI_TOKEN`
2. Create release on GitHub
3. Package auto-publishes to PyPI

---

## Pre-Publish Checklist

Before publishing, verify:

- [ ] Version updated in `pyproject.toml`
- [ ] CHANGELOG.md updated with release notes
- [ ] All tests passing (when tests exist)
- [ ] README.md accurate and complete
- [ ] Documentation up to date
- [ ] No sensitive data in code (API keys, tokens)
- [ ] Git tag created and pushed
- [ ] Clean build directory (`rm -rf dist/ build/`)

---

## Package Metadata

Update these fields in `pyproject.toml` before first publish:

```toml
[project]
name = "hole-fonts"
version = "2.0.0"
description = "Professional font library management with metadata extraction and search"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "HOLE Foundation", email = "contact@theholefoundation.org"}
]
keywords = ["fonts", "typography", "font-management", "ttf", "otf", "woff2"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    "Topic :: Text Processing :: Fonts",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
]

[project.urls]
Homepage = "https://github.com/The-HOLE-Foundation/hole-fonts"
Documentation = "https://github.com/The-HOLE-Foundation/hole-fonts#readme"
Repository = "https://github.com/The-HOLE-Foundation/hole-fonts"
Issues = "https://github.com/The-HOLE-Foundation/hole-fonts/issues"
Changelog = "https://github.com/The-HOLE-Foundation/hole-fonts/blob/main/CHANGELOG.md"
```

---

## Release Process

### Semantic Versioning

We follow [SemVer](https://semver.org/):

- **Major** (X.0.0): Breaking changes
- **Minor** (x.Y.0): New features, backward compatible
- **Patch** (x.y.Z): Bug fixes, backward compatible

### Version History

- **v0.1.0** - Initial conversion tool
- **v1.0.0** - FontBase integration
- **v2.0.0** - Metadata extraction, search, designer/foundry data

### Release Workflow

```bash
# 1. Update version
# Edit pyproject.toml

# 2. Update changelog
# Edit CHANGELOG.md

# 3. Commit
git add pyproject.toml CHANGELOG.md
git commit -m "chore: release v2.0.0"

# 4. Tag
git tag -a v2.0.0 -m "Release v2.0.0: Metadata extraction and search"

# 5. Push
git push origin HOLE-FONTS-Ext --tags

# 6. Build
rm -rf dist/
uv build

# 7. Test on TestPyPI
twine upload --repository testpypi dist/*

# 8. Test installation
pip install --index-url https://test.pypi.org/simple/ hole-fonts

# 9. Publish to PyPI
twine upload dist/*

# 10. Create GitHub Release
# Go to: https://github.com/The-HOLE-Foundation/hole-fonts/releases/new
# Upload dist/* files as release artifacts
```

---

## Distribution Files

### What Gets Published

After `uv build`, you'll have:

```
dist/
├── hole_fonts-2.0.0.tar.gz          # Source distribution
└── hole_fonts-2.0.0-py3-none-any.whl # Wheel (preferred)
```

**Wheel advantages**:
- Faster installation
- No build step required
- Platform-independent (pure Python)
- Includes compiled bytecode

### What NOT to Include

The following are automatically excluded (via `.gitignore` and build config):

- ❌ Virtual environments (`.venv/`)
- ❌ Database files (`*.json` except config files)
- ❌ Log files (`*.log`)
- ❌ Font files (`*.ttf`, `*.otf`, `*.woff2`)
- ❌ Build artifacts (`build/`, `dist/`)
- ❌ Cache files (`__pycache__/`, `*.pyc`)

---

## Security Best Practices

### API Keys & Secrets

**Never include in package**:
- Typekit API keys
- Database credentials
- Authentication tokens

**Use environment variables** instead:
```python
import os
api_key = os.environ.get('TYPEKIT_API_KEY')
```

### Token Storage

Store PyPI tokens securely:

1. **Local development**: Use `.pypirc` (chmod 600)
2. **CI/CD**: Use GitHub Secrets or environment variables
3. **Never** commit tokens to git

---

## Post-Publication

### Verification

```bash
# Wait 1-2 minutes for PyPI to index

# Check package page
open https://pypi.org/project/hole-fonts/

# Test fresh installation
python3 -m venv test-env
source test-env/bin/activate
pip install hole-fonts
hole-fonts --help
```

### Announce Release

1. Create GitHub Release with notes
2. Update project README with latest version
3. Announce on relevant channels (optional)

---

## Maintenance

### Updating Package

For bug fixes or new features:

1. Make code changes
2. Update version in `pyproject.toml` (e.g., 2.0.0 → 2.0.1)
3. Update `CHANGELOG.md`
4. Follow release workflow above

### Yanking a Release (Emergency)

If a release has critical bugs:

```bash
# Yank version from PyPI (makes it unavailable for new installs)
twine upload --skip-existing dist/*
pip install twine
# Then on PyPI web interface: "Manage" → "Yank release"
```

---

## Current Status

- [x] Package structure ready
- [x] `pyproject.toml` configured
- [x] Entry points defined (`hole-fonts` command)
- [x] Dependencies specified
- [ ] Published to TestPyPI
- [ ] Published to PyPI
- [ ] GitHub release created

**Next Step**: Publish v2.0.0 to PyPI

---

## Quick Reference

```bash
# Build
uv build

# Test publish
twine upload --repository testpypi dist/*

# Production publish
twine upload dist/*

# Verify
pip install hole-fonts
hole-fonts --help
```

---

**Last Updated**: 2026-01-09
**Ready for**: First PyPI publication
