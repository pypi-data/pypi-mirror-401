# HOLE Fonts - Professional Font Management System

**Version:** 2.0.0
**Status:** ✅ Production Ready
**Python:** 3.11+

Professional font library management with metadata extraction, intelligent search, duplicate detection, and format conversion.

---

## Installation

```bash
# From PyPI (coming soon)
pip install hole-fonts

# From source
git clone https://github.com/The-HOLE-Foundation/hole-fonts.git
cd hole-fonts
pip install .

# Verify
hole-fonts --help
```

See [INSTALLATION.md](INSTALLATION.md) for detailed installation options.

---

## Quick Start

```bash
# 1. Scan your fonts
hole-fonts scan /path/to/your/fonts --output my-fonts.json

# 2. Search by designer
hole-fonts search my-fonts.json --designer "Adrian Frutiger"

# 3. Find sans-serif fonts
hole-fonts search my-fonts.json --classification "sans-serif"

# 4. Find duplicates
hole-fonts dedup my-fonts.json
```

See [USER-QUICKSTART.md](USER-QUICKSTART.md) for complete usage guide.

---

## Overview

HOLE Fonts is a professional-grade font management system that provides:

- **Metadata Extraction** - Designer, foundry, copyright, description from font files
- **Intelligent Search** - Find fonts by designer, foundry, classification, weight, style
- **Duplicate Detection** - Find duplicate fonts with 95%+ accuracy
- **Format Conversion** - Convert between TTF, OTF, WOFF2
- **Variable Font Support** - Automatic detection and preservation
- **FontBase Integration** - Export for use with FontBase organizer

### Key Features (v2.0.0)

**🔍 Search & Discovery**
- Search 24,000+ fonts in milliseconds
- Filter by designer (93.9% coverage)
- Filter by foundry (94.9% coverage)
- Classification inference (sans-serif, serif, display, mono)
- Weight, width, italic filtering
- Variable font detection

**📊 Metadata Intelligence**
- Designer names extracted from font files
- Foundry/manufacturer information
- Copyright and licensing info (98.9% coverage)
- Font descriptions and history
- Vendor and designer URLs
- No external API dependency

**🎯 Duplicate Detection**
- Strict matching rules (95%+ name similarity)
- Weight/width/italic exact matching
- Monotype unique ID validation
- Confidence scoring
- Space savings calculation

**🔄 Format Conversion**
- TTF ↔ OTF ↔ WOFF2
- Variable font preservation
- Batch processing
- FontBase-optimized export

### The Smart Division of Labor

**HOLE Fonts** = Conversion Engine
- ✅ Batch font conversion (TTF ↔ OTF ↔ WOFF2)
- ✅ Variable font detection & preservation
- ✅ Automated export to FontBase-friendly structure
- ✅ 100% success rate on 126+ font families

**FontBase** (Free!) = Organization & Management
- ✅ Auto-import from watched folders
- ✅ Collections for virtual organization
- ✅ Font activation/deactivation
- ✅ Beautiful previews & search
- ✅ Design tool integration

---

## Quick Start

### 1. Export Your Fonts

```bash
# Single family
uv run python -m hole_fonts.cli export Input/FamilyName/

# All families (batch)
uv run python -m hole_fonts.cli export Input/Organized-Folders/

# Custom location
uv run python -m hole_fonts.cli export Input/Fonts/ --to ~/FontBase-Library/
```

### 2. Install FontBase

1. Download: https://fontba.se/
2. Install and launch
3. Add Folder → `FontBase-Export/`
4. Enable "Watch for changes"

### 3. Start Organizing!

Use FontBase Collections to organize fonts by:
- Project (Website 2025, Brand Guidelines)
- Foundry (Adobe, Monotype, Google)
- License (Commercial, Personal, Open Source)
- Style (Sans Serif, Serif, Display, Script)

---

## Features

### Font Conversion

- **Formats Supported:** TTF, OTF, WOFF, WOFF2
- **Variable Font Detection:** Automatic detection with axis preservation
- **Batch Processing:** Process entire directories
- **Format Conversion:** Convert between any supported formats
- **Quality:** Zero data loss, metadata preserved

### Export Structures

**flat-by-family** (Recommended for FontBase)
```
FontBase-Export/
├── AgencyFB/
│   ├── AgencyFB-Bold.ttf
│   ├── AgencyFB-Bold.otf
│   └── AgencyFB-Bold.woff2
└── Helvetica/
    └── ...
```

**format-separated**
```
FontBase-Export/
└── AgencyFB/
    ├── OTF/
    ├── TTF/
    └── WOFF2/
```

**single-flat**
```
FontBase-Export/
├── AgencyFB-Bold.ttf
├── AgencyFB-Bold.otf
└── AgencyFB-Bold.woff2
```

### Variable Font Support

- ✅ Automatic detection (fvar table)
- ✅ Axis information extraction
- ✅ Variation data preservation
- ✅ Named instances preserved
- ✅ Visual indicators in output (🎨)

**Supported axes:** wght, wdth, slnt, opsz, ital, SERF, CONT, and custom axes

---

## Project Structure

```
HOLE-Fonttools-Project/
├── hole_fonts/              # Core package
│   ├── converter.py        # Font conversion engine
│   ├── exporter.py         # FontBase integration
│   ├── organizer.py        # Library organization (legacy)
│   └── config.py           # Configuration
├── Input/                  # Source fonts
├── FontBase-Export/        # Exported fonts → Add to FontBase
├── Output/                 # Temporary conversions
├── config.yaml             # Configuration
├── pyproject.toml          # Package definition
└── Documentation/
    ├── QUICKSTART.md
    ├── FONTBASE_SETUP_GUIDE.md
    ├── IMPLEMENTATION_PLAN.md
    └── ARCHITECTURE_PROPOSAL.md
```

---

## Commands

### Scanning & Database Building

```bash
# Scan fonts directory and create database
hole-fonts scan /path/to/fonts --output my-fonts.json

# Scan with progress tracking (processes ~10-20 fonts/second)
hole-fonts scan ~/Library/Fonts --output system-fonts.json
```

### Searching Fonts

```bash
# Search by designer
hole-fonts search my-fonts.json --designer "Adrian Frutiger"

# Search by foundry
hole-fonts search my-fonts.json --foundry "Monotype"

# Search by classification
hole-fonts search my-fonts.json --classification "sans-serif"

# Find variable fonts
hole-fonts search my-fonts.json --variable

# Combine filters
hole-fonts search my-fonts.json --foundry "Adobe" --classification "sans-serif" --weight-min 700
```

### Duplicate Detection

```bash
# Find duplicate fonts
hole-fonts dedup my-fonts.json

# Use custom confidence threshold
hole-fonts dedup my-fonts.json --min-confidence 0.80

# Save report to file
hole-fonts dedup my-fonts.json > duplicates-report.txt
```

### Font Conversion

```bash
# Simple in-place conversion (creates format subdirectories)
hole-fonts convert-simple /path/to/fonts

# Convert single font to all formats
hole-fonts convert font.ttf

# Export to FontBase-friendly structure
hole-fonts export /path/to/fonts --to ~/FontBase-Export/
```

### Legacy Commands (v1.0)

```bash
# List library (old organization system)
uv run python -m hole_fonts.cli list

# Show family info
uv run python -m hole_fonts.cli info FamilyName

# Validate library structure
uv run python -m hole_fonts.cli validate
```

---

## Configuration

Edit `config.yaml`:

```yaml
export:
  default_path: 'FontBase-Export'
  structure: 'flat-by-family'

formats:
  - ttf
  - otf
  - woff2

processing:
  parallel_workers: 4
```

---

## Results

### Batch Conversion Stats

**First Batch (126 families):**
- ✅ 126/126 families processed successfully
- ✅ 0 failures (100% success rate)
- ✅ 7 variable fonts detected
- ✅ Thousands of fonts converted
- ✅ All formats generated

**Notable Collections:**
- Area: 175 fonts per format (525 total)
- BentonSans: 140 fonts (420 total)
- VariableFonts: 126 variable fonts (378 total)
- HelveticaNow: 96 fonts (288 total)
- And many more professional typefaces

### Variable Fonts Detected

**Width Variations:**
- wdth: Width (50-200)
- CONT: Contrast (1-1000)

**Weight Variations:**
- wght: Weight (100-900)

**Slant/Italics:**
- slnt: Slant (-12 to 12)
- ital: Italic (0-100)

**Optical Size:**
- opsz: Optical Size (6-72)

**Custom Axes:**
- SERF: Serif amount
- HGHT: Height
- SANS: Sans amount

---

## Workflow Examples

### New Font Project

```bash
# 1. Get fonts
cp ~/Downloads/NewFonts/* Input/ProjectName/

# 2. Export to FontBase
uv run python -m hole_fonts.cli export Input/ProjectName/

# 3. FontBase auto-imports (if watching)

# 4. Create Collection in FontBase
#    Name: "Website 2025"
#    Add fonts, activate, work!
```

### Web Font Generation

```bash
# Export only WOFF2
uv run python -m hole_fonts.cli export Input/Fonts/ \
    --formats woff2 \
    --to WebProject/public/fonts/
```

### Archive Preparation

```bash
# All formats, organized by type
uv run python -m hole_fonts.cli export Input/Archive/ \
    --structure format-separated \
    --to Archive-Library/
```

---

## Technical Details

### Dependencies

```toml
fonttools[woff] >= 4.61.1  # Core conversion
click >= 8.1.0              # CLI interface
pyyaml >= 6.0              # Configuration
rich >= 13.0.0             # Terminal UI
requests >= 2.31.0         # API calls (v0.2)
```

### Supported Platforms

- macOS (tested)
- Linux (supported)
- Windows (supported)

### Performance

- **Conversion Speed:** ~2-3 seconds per font
- **Batch Processing:** Handles 100+ families easily
- **Variable Fonts:** Full support with no performance penalty
- **Scalability:** Tested with 1000+ fonts

---

## Future Roadmap

### v0.2 - Metadata Integration

- Adobe Typekit API integration
- Font metadata enrichment (designer, foundry, history)
- Smart duplicate detection via UUID
- Search and filtering functionality
- HTML catalog generation

### v0.3 - Advanced Features

- CSS @font-face generation
- Font subsetting for web
- Web font optimization
- License management
- Font validation tools

### v0.4 - Team Collaboration

- Shared font registries
- Multi-library support
- Audit logs
- Font approval workflows
- Client project tracking

---

## Why This Architecture?

### Problem: Font Library Organization is Hard

Past attempts at automated organization often fail:
- Fonts split incorrectly by weight/style
- Every font becomes its own "family"
- Complex rules that don't match real-world usage
- Hard to fix mistakes without reconverting

### Solution: Separation of Concerns

**HOLE Fonts** does what computers do best:
- Fast, accurate format conversion
- Batch processing
- Variable font preservation
- Standardized export

**FontBase** does what humans do best (with great tools):
- Visual browsing and preview
- Intuitive organization via Collections
- Context-based grouping (project, client, style)
- Easy reorganization anytime

**Result:** Professional workflow, zero frustration

---

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[FONTBASE_SETUP_GUIDE.md](FONTBASE_SETUP_GUIDE.md)** - Complete FontBase integration guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference card
- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Full technical roadmap
- **[ARCHITECTURE_PROPOSAL.md](ARCHITECTURE_PROPOSAL.md)** - Design decisions explained

---

## Credits

**Powered by:**
- [FontTools](https://github.com/fonttools/fonttools) - Font conversion engine
- [FontBase](https://fontba.se/) - Font management (free!)
- Python 3.14 with uv package manager

**Created for:** HOLE Foundation
**Branch:** HOLE-FONTS-Ext
**Date:** December 2025

---

## License

Internal use for HOLE Foundation

---

## Support

**Issues or questions?**
Check the documentation in this repository or review the implementation logs.

**Next steps:**
Install FontBase and start organizing your professional font library!

---

**HOLE Fonts + FontBase = Professional Font Workflow** ✨
