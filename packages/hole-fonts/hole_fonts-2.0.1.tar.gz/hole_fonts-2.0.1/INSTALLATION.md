# HOLE Fonts - Installation Guide

**Version**: v2.0.0
**Python**: 3.11+
**Package Manager**: pip or uv

---

## Quick Install (Recommended)

### Option 1: Install from PyPI (Future)

Once published to PyPI:

```bash
# Using pip
pip install hole-fonts

# Using uv (faster)
uv pip install hole-fonts

# Verify installation
hole-fonts --help
```

### Option 2: Install from Source (Current)

```bash
# Clone or download the repository
git clone https://github.com/The-HOLE-Foundation/hole-fonts.git
cd hole-fonts

# Install using pip
pip install .

# Or install in development mode
pip install -e .

# Verify installation
hole-fonts --help
```

### Option 3: Install from Wheel

```bash
# Download the wheel file from releases
# https://github.com/The-HOLE-Foundation/hole-fonts/releases

# Install the wheel
pip install hole_fonts-2.0.0-py3-none-any.whl

# Verify installation
hole-fonts --help
```

---

## System Requirements

### Python Version
- **Minimum**: Python 3.11
- **Recommended**: Python 3.13+
- **Tested**: Python 3.14

Check your version:
```bash
python3 --version
```

### Disk Space
- **Application**: ~5 MB
- **Dependencies**: ~50 MB
- **Database files**: 10-50 MB per database (not included)

### Operating Systems
- **macOS**: Fully tested ✅
- **Linux**: Compatible ✅
- **Windows**: Compatible (not tested)

---

## Installation Methods

### Method 1: pip (Standard)

```bash
# Install from source directory
pip install /path/to/hole-fonts

# Install with development dependencies (future)
pip install hole-fonts[dev]

# Upgrade to latest version
pip install --upgrade hole-fonts
```

### Method 2: uv (Fast Modern Alternative)

```bash
# Install uv first (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install .

# Or install globally
uv pip install --system .
```

### Method 3: pipx (Isolated Installation)

```bash
# Install pipx first (if not installed)
pip install pipx
pipx ensurepath

# Install hole-fonts in isolated environment
pipx install /path/to/hole-fonts

# This creates a dedicated environment and makes `hole-fonts` available globally
```

---

## Post-Installation Setup

### 1. Verify Installation

```bash
# Check version
hole-fonts --help

# Should display:
# Usage: hole-fonts [OPTIONS] COMMAND [ARGS]...
#
# HOLE Fonts - Font library management system
#
# Commands:
#   convert         Convert fonts with multiple modes
#   convert-simple  Simple in-place font conversion
#   dedup           Find duplicate fonts in database
#   enrich          Enrich font metadata with Adobe Typekit data
#   export          Convert fonts and export to FontBase
#   info            Show detailed information about a font family
#   list            List all font families in library
#   scan            Scan font directory and build metadata database
#   search          Search fonts by criteria
#   validate        Validate library structure
```

### 2. Create Configuration (Optional)

Create a `config.yaml` file in your working directory:

```yaml
# HOLE Fonts Configuration

libraries:
  default: 'main'
  locations:
    main:
      name: 'My Font Library'
      path: '/path/to/your/fonts'
      database: '/path/to/your/font-database.json'

formats:
  - ttf
  - otf
  - woff2

processing:
  parallel_workers: 4
  skip_existing: true
```

### 3. Test with Sample Fonts

```bash
# Scan a directory of fonts
hole-fonts scan /path/to/fonts --output test-database.json

# Search the database
hole-fonts search test-database.json --classification "sans-serif"

# Convert a font
hole-fonts convert-simple /path/to/font.ttf
```

---

## Uninstallation

```bash
# Using pip
pip uninstall hole-fonts

# Using pipx
pipx uninstall hole-fonts

# Using uv
uv pip uninstall hole-fonts
```

---

## Troubleshooting

### "hole-fonts: command not found"

**Cause**: Installation path not in system PATH

**Solutions**:

1. **Verify installation**:
   ```bash
   pip show hole-fonts
   ```

2. **Find installation location**:
   ```bash
   python3 -m site --user-base
   ```

3. **Add to PATH** (if using --user install):
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   export PATH="$HOME/.local/bin:$PATH"
   ```

4. **Use pipx instead** (recommended):
   ```bash
   pipx install hole-fonts
   ```

### "No module named 'fonttools'"

**Cause**: Dependencies not installed

**Solution**:
```bash
pip install fonttools[woff] click pyyaml rich requests
```

### "Python version incompatible"

**Cause**: Python version < 3.11

**Solution**:
1. Install Python 3.13+ from python.org
2. Create virtual environment with correct version:
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install hole-fonts
   ```

### "Permission denied" on macOS/Linux

**Cause**: Installing to system Python

**Solutions**:
1. **Use virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install hole-fonts
   ```

2. **User install**:
   ```bash
   pip install --user hole-fonts
   ```

3. **Use pipx**:
   ```bash
   pipx install hole-fonts
   ```

---

## Development Installation

For developers who want to contribute:

```bash
# Clone repository
git clone https://github.com/The-HOLE-Foundation/hole-fonts.git
cd hole-fonts

# Install with uv (recommended)
uv sync

# Or with pip in development mode
pip install -e .

# Run tests (future)
pytest

# Build package
uv build
# Creates: dist/hole_fonts-2.0.0-py3-none-any.whl
```

---

## Advanced Installation

### Installing Specific Version

```bash
# Install specific version from PyPI (future)
pip install hole-fonts==2.0.0

# Install from git tag
pip install git+https://github.com/The-HOLE-Foundation/hole-fonts.git@v2.0.0

# Install from specific branch
pip install git+https://github.com/The-HOLE-Foundation/hole-fonts.git@HOLE-FONTS-Ext
```

### Custom Installation Location

```bash
# Install to specific directory
pip install --target=/custom/path hole-fonts

# Add to PYTHONPATH
export PYTHONPATH="/custom/path:$PYTHONPATH"
```

### Offline Installation

```bash
# Download dependencies first
pip download hole-fonts -d ./packages

# Install offline
pip install --no-index --find-links=./packages hole-fonts
```

---

## Verifying Installation

### Check Version

```bash
hole-fonts --help | head -3
```

### Test Core Functionality

```bash
# Test scanning
hole-fonts scan /path/to/test/fonts --output test.json

# Test search
hole-fonts search test.json --variable

# Test conversion (if you have a test font)
hole-fonts convert-simple test-font.ttf
```

### Check Dependencies

```bash
pip show hole-fonts
# Displays version, dependencies, location
```

---

## Upgrading

### From Earlier Versions

```bash
# Upgrade to latest
pip install --upgrade hole-fonts

# Or with uv
uv pip install --upgrade hole-fonts

# Verify new version
hole-fonts --help
```

### Database Compatibility

Database files from v1.x are **not compatible** with v2.0+. Re-scan your fonts to create new database:

```bash
# Re-scan library for v2.0
hole-fonts scan /path/to/fonts --output fonts-v2.json
```

---

## Getting Help

### Documentation

- **Quick Start**: See `QUICKSTART.md`
- **Commands**: Run `hole-fonts <command> --help`
- **Examples**: See `README.md`

### Support

- **Issues**: https://github.com/The-HOLE-Foundation/hole-fonts/issues
- **Discussions**: https://github.com/The-HOLE-Foundation/hole-fonts/discussions

---

**Last Updated**: 2026-01-09
**Version**: 2.0.0
