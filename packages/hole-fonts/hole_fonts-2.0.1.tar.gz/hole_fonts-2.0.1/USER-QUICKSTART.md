# HOLE Fonts - User Quick Start

**Welcome!** This guide will get you started with HOLE Fonts in 5 minutes.

---

## Installation

```bash
# Install (once published to PyPI)
pip install hole-fonts

# Verify installation
hole-fonts --help
```

For detailed installation options, see [INSTALLATION.md](INSTALLATION.md)

---

## First Time Setup

### 1. Scan Your Fonts

Create a searchable database of your font collection:

```bash
# Scan your fonts directory
hole-fonts scan /path/to/your/fonts --output my-fonts.json

# Example: Scan system fonts on macOS
hole-fonts scan ~/Library/Fonts --output system-fonts.json
```

This creates a database file with complete metadata for all your fonts including:
- Font family and style info
- Designer names
- Foundry information
- Weight, width, italic status
- Variable font detection

**Time**: ~10-20 fonts per second (10 minutes for 5,000 fonts)

---

## Common Tasks

### Search Your Fonts

```bash
# Find all fonts by a designer
hole-fonts search my-fonts.json --designer "Adrian Frutiger"

# Find fonts from a foundry
hole-fonts search my-fonts.json --foundry "Monotype"

# Find sans-serif fonts
hole-fonts search my-fonts.json --classification "sans-serif"

# Find variable fonts
hole-fonts search my-fonts.json --variable

# Find bold fonts (700+ weight)
hole-fonts search my-fonts.json --weight-min 700

# Combine filters
hole-fonts search my-fonts.json --foundry "Adobe" --classification "sans-serif" --variable
```

### Find Duplicates

```bash
# Detect duplicate fonts
hole-fonts dedup my-fonts.json

# Save report
hole-fonts dedup my-fonts.json > duplicates-report.txt

# Use custom confidence threshold
hole-fonts dedup my-fonts.json --min-confidence 0.80
```

### Convert Fonts

```bash
# Simple in-place conversion (creates TTF/, OTF/, WOFF2/ folders)
hole-fonts convert-simple /path/to/fonts

# Convert to all formats
hole-fonts convert font.ttf
# Creates: font.ttf, font.otf, font.woff2

# Convert entire directory
hole-fonts convert /path/to/font/folder
```

---

## Real-World Examples

### Example 1: "I need to find all Helvetica variants"

```bash
hole-fonts search my-fonts.json --family "Helvetica"
```

**Result**: All Helvetica fonts grouped by family with file locations

### Example 2: "Which fonts did Adrian Frutiger design?"

```bash
hole-fonts search my-fonts.json --designer "Frutiger"
```

**Result**:
- Univers (125 fonts)
- Avenir (40 fonts)
- Frutiger (54 fonts)
- And more...

### Example 3: "Find bold sans-serif fonts for web"

```bash
hole-fonts search my-fonts.json \
  --classification "sans-serif" \
  --weight-min 700 \
  --format woff2
```

**Result**: Bold sans-serif WOFF2 files ready for web deployment

### Example 4: "Do I have duplicate fonts wasting space?"

```bash
hole-fonts dedup my-fonts.json
```

**Result**:
- List of duplicate font pairs
- Confidence scores
- Space savings if deleted
- Recommendations

### Example 5: "Convert TTF fonts to web format"

```bash
hole-fonts convert-simple /path/to/ttf/fonts
```

**Result**:
```
/path/to/ttf/fonts/
├── TTF/ (originals)
├── OTF/ (converted)
└── WOFF2/ (converted for web)
```

---

## Understanding the Output

### Search Results

When you search, you'll see:

```
Found 382 matching fonts:

Avenir LT Pro (12 fonts)
  • Avenir85Heavy-1246009.otf
  • Avenir65Medium-1246005.otf
  • Avenir45Book-1246003.otf
  ... and 9 more

Univers Next Pro (125 fonts)
  • UniversNext220CondensedThin.ttf
  • UniversNext330BasicRegular.otf
  ... and 123 more
```

- **Family grouping**: Fonts grouped by family name
- **File count**: Total files in each family
- **Samples**: First few files shown
- **Full list**: Run with `--verbose` for all files (future)

### Duplicate Detection

```
Found 101 duplicate font pairs:

Match #1 (Confidence: 0.95)
  Font 1: Arial-Bold.ttf (Size: 723 KB)
  Font 2: Arial-Bold-Copy.ttf (Size: 723 KB)
  Reason: Identical hash, same metadata
  Can auto-delete: Yes
  Space savings: 723 KB
```

- **Confidence**: How certain we are it's a duplicate (0.0-1.0)
- **Reason**: Why they're considered duplicates
- **Auto-delete**: Safe to automatically remove
- **Savings**: Disk space recovered if deleted

---

## Tips & Tricks

### 1. Keep Your Database Updated

When you add new fonts, update your database:

```bash
# Re-scan
hole-fonts scan /path/to/fonts --output my-fonts.json

# Or scan just new fonts and merge (future feature)
```

### 2. Database Files Are Portable

You can share your font database with colleagues:

```bash
# Copy database to shared location
cp my-fonts.json /shared/team-fonts.json

# Anyone can search it
hole-fonts search /shared/team-fonts.json --designer "Helvetica"
```

### 3. Multiple Libraries

Organize different font collections:

```bash
# Personal fonts
hole-fonts scan ~/Fonts --output personal-fonts.json

# Work fonts
hole-fonts scan /work/fonts --output work-fonts.json

# Search each separately
hole-fonts search personal-fonts.json --foundry "Adobe"
hole-fonts search work-fonts.json --classification "sans-serif"
```

### 4. Web Font Workflow

```bash
# 1. Find fonts you need
hole-fonts search my-fonts.json --format woff2 --family "Open Sans"

# 2. Copy to web project
cp /path/from/search/result/*.woff2 ~/my-website/public/fonts/

# 3. Use in CSS
# Add @font-face rules
```

### 5. Font Discovery

```bash
# "What variable fonts do I have?"
hole-fonts search my-fonts.json --variable

# "Show me all Monotype fonts"
hole-fonts search my-fonts.json --foundry "Monotype"

# "What serif fonts are available?"
hole-fonts search my-fonts.json --classification "serif"
```

---

## Advanced Usage

### Custom Confidence for Duplicates

```bash
# More strict (fewer matches, higher confidence)
hole-fonts dedup my-fonts.json --min-confidence 0.90

# More lenient (more matches, lower confidence)
hole-fonts dedup my-fonts.json --min-confidence 0.50
```

### Search with Multiple Criteria

```bash
# Italic sans-serif fonts from Linotype
hole-fonts search my-fonts.json \
  --foundry "Linotype" \
  --classification "sans-serif" \
  --italic

# Variable fonts with weight axis from Adobe
hole-fonts search my-fonts.json \
  --foundry "Adobe" \
  --variable \
  --has-axis wght
```

### Configuration File

Create `config.yaml` for persistent settings:

```yaml
libraries:
  default: 'main'
  locations:
    main:
      path: '/Users/you/Fonts'
      database: '/Users/you/font-database.json'

processing:
  parallel_workers: 4
  skip_existing: true
```

---

## What's Next?

### Learn More
- **Full commands**: Run `hole-fonts <command> --help`
- **Architecture**: See [ARCHITECTURE_PROPOSAL.md](ARCHITECTURE_PROPOSAL.md)
- **Roadmap**: See [ROADMAP.md](ROADMAP.md)

### Feature Requests
- Report issues: https://github.com/The-HOLE-Foundation/hole-fonts/issues
- Suggest features: https://github.com/The-HOLE-Foundation/hole-fonts/discussions

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Scan fonts | `hole-fonts scan <dir> --output db.json` |
| Search by designer | `hole-fonts search db.json --designer "Name"` |
| Search by foundry | `hole-fonts search db.json --foundry "Name"` |
| Find sans-serif | `hole-fonts search db.json --classification "sans-serif"` |
| Find variable fonts | `hole-fonts search db.json --variable` |
| Find duplicates | `hole-fonts dedup db.json` |
| Convert fonts | `hole-fonts convert-simple <dir>` |
| Get help | `hole-fonts --help` |
| Command help | `hole-fonts <command> --help` |

---

**Happy font hunting!** 🎨

**Last Updated**: 2026-01-09
**Version**: 2.0.0
