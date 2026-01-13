# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**HOLE Fonts** is a professional font library management system for managing the HOLE Foundation's extensive font collection (11,000+ fonts). The system provides:

- **Font Conversion**: Convert between TTF, OTF, and WOFF2 formats using FontTools
- **Metadata Extraction**: Extract comprehensive font metadata (weight, width, italic, variable axes, glyph count)
- **Duplicate Detection**: Identify duplicate fonts with strict confidence scoring
- **Search & Filter**: Find fonts by family, weight, classification, designer, foundry
- **Adobe Typekit Enrichment**: Optional metadata enhancement via Typekit API

**Current Version**: v2.0.0 (Production-ready)

**Tech Stack**: Python 3.14, FontTools 4.61.1, Click, Rich, PyYAML, Requests

**Package Manager**: uv (NOT pip)

---

## Critical Context

### Resume Points After Reboot

After any system reboot or new session, always read these files IN THIS ORDER:

1. **`PROJECT-STATUS.md`** - Current project status and recent accomplishments
2. **`SESSION-MEMORY.md`** - Last session context, decisions, and testing results
3. **`DIRECTORIES.md`** - All critical file paths and volume locations

These files contain session-specific context that is essential for continuing work.

### Font Library Locations

**Primary (FAST - Use for all bulk operations):**
```
/Volumes/HOLE-RAID-DRIVE/HOLE-Assets/HOLE-Fonts/
├── TTF/     (11,047 fonts)
├── OTF/     (11,047 fonts)
└── WOFF2/   (11,047 fonts)
```
**Performance**: ~10-20 fonts/second scan speed

**Secondary (SLOW - Avoid for bulk operations):**
```
/Volumes/80F9F6D9.../HOLE-Fonts-Master-Claude-Certified/
```
**Contains**: 32,796 fonts (complete master collection)
**Note**: iCloud sync makes this extremely slow - use RAID drive instead

### Key Databases

- `HOLE-Fonts-RAID-Database.json` (8.1 MB) - Full metadata for 11,047 fonts
- `HOLE-Fonts-RAID-Enriched.json` (8.1 MB) - With Typekit enrichments
- `dedup-report.json` (28 KB) - Duplicate analysis (101 real duplicates)

---

## Development Commands

### Environment Setup

```bash
# Install dependencies (after reboot or package changes)
uv sync

# Reinstall package after code changes
uv sync --reinstall-package hole-fonts

# Verify installation
uv run hole-fonts --help
```

### Font Scanning

```bash
# Scan directory and create metadata database
uv run hole-fonts scan <directory> --output database.json

# Scan RAID drive (production library)
uv run hole-fonts scan "/Volumes/HOLE-RAID-DRIVE/HOLE-Assets/HOLE-Fonts" \
  --output HOLE-Fonts-RAID-Database.json
```

### Duplicate Detection

```bash
# Find duplicates in database
uv run hole-fonts dedup database.json --min-confidence 0.60

# Output includes:
# - Match confidence scores (0.0-1.0)
# - Reason for match
# - File size comparison
# - Space savings if deleted
```

### Search & Filter

```bash
# Search by family and weight
uv run hole-fonts search database.json --family "Helvetica" --weight-min 700

# Find all variable fonts
uv run hole-fonts search database.json --variable

# Find sans-serif fonts (requires Typekit enrichment)
uv run hole-fonts search database.json --classification "sans-serif"

# Search by designer/foundry (requires Typekit enrichment)
uv run hole-fonts search database.json --designer "Matthew Carter"
```

### Typekit Enrichment

```bash
# Note: CLI has a bug, use custom script instead
uv run python enrich_fonts.py

# API Key: 459aa874c56344b9c2f44b3a5edde401dc918fca
```

### Font Conversion

```bash
# Simple in-place conversion (creates format subdirectories)
uv run hole-fonts convert-simple <directory>

# Convert with library integration
uv run hole-fonts convert <input> --library main --add-to-database

# Interactive mode (prompts for options)
uv run hole-fonts convert <input> -i
```

### Building for Release

```bash
# Build Python wheel
uv build

# Output: dist/hole_fonts-2.0.0-py3-none-any.whl
```

### Testing

```bash
# Run quick validation on test fonts
uv run hole-fonts scan Input/ --output test-scan.json
uv run hole-fonts search test-scan.json --family "AgencyFB"
```

---

## Architecture

### Core Modules

The system is organized into specialized modules with clear separation of concerns:

**`metadata.py`** - Font metadata extraction
- `FontMetadata` dataclass: Complete font metadata structure
- `FontAnalyzer`: Extracts metadata using FontTools
- `FontDatabase`: Load/save JSON databases
- Extracts: family name, PostScript name, weight (100-900), width, italic, variable axes, glyph count

**`converter.py`** - Font format conversion
- Uses FontTools for TTF ↔ OTF ↔ WOFF2 conversion
- Preserves variable font features
- Batch processing with progress tracking

**`dedup.py`** - Duplicate detection with strict matching
- `DuplicateDetector`: Find duplicate fonts
- **CRITICAL**: Uses strict matching rules (see Quality Standards below)
- Confidence scoring (0.0-1.0)
- SHA256 file hashing

**`search.py`** - Font search and filtering
- `FontSearch`: Search database by criteria
- `SearchCriteria`: Define search parameters
- Filter by: family, weight range, width, italic, variable fonts, axes, format, classification, designer, foundry

**`typekit.py`** - Adobe Typekit API integration
- `TypekitClient`: Rate-limited API client with LRU caching
- `TypekitEnricher`: Batch enrichment with progress callbacks
- Font name normalization for better matching
- Adds: designer, foundry, classifications

**`cli.py`** - Command-line interface
- Commands: scan, dedup, search, enrich, convert, convert-simple, export, info, list, validate
- Uses Click for argument parsing
- Uses Rich for terminal UI (tables, progress bars, panels)

### Data Flow

```
Font Files → FontAnalyzer → FontMetadata → FontDatabase (JSON)
                                              ↓
                                         DuplicateDetector
                                              ↓
                                         FontSearch
                                              ↓
                                     TypekitEnricher (optional)
```

### Configuration System

Configuration is loaded from `config.yaml` with the following structure:

- **libraries**: Multiple library locations (main, legacy, fontbase, web)
- **conversion**: Default mode, preserve originals
- **formats**: Target formats (ttf, otf, woff2)
- **typekit**: API key and settings
- **database**: Auto-scan, auto-dedup, confidence threshold
- **processing**: Parallel workers, skip existing, backup on overwrite
- **export**: FontBase integration settings

Access config via: `get_config('config.yaml')` (returns dict)

---

## Quality Standards & Critical Rules

### Duplicate Detection Rules (STRICT)

The duplicate detection system uses **strict matching rules** to avoid false positives. A bug was fixed where 1,860 false positives were reduced to 101 real duplicates.

**Rules (ALL must match):**
- Weight must be EXACTLY the same (900 ≠ 400)
- Italic status must be EXACTLY the same (italic ≠ regular)
- Width must be EXACTLY the same (condensed ≠ normal)
- Monotype unique IDs must match (6-digit numbers in filename)
- Name similarity must be ≥95% (raised from 80%)

**Example of what is NOT a duplicate:**
- `UniversNext731BasicHeavyItalic` (weight 900) vs `UniversNext431BasicItalic` (weight 400)
- Different weights, different unique IDs (731 vs 431)

See `SESSION-MEMORY.md` for the complete bug fix context and code snippets.

### Performance Guidelines

- **Always use RAID drive** (`/Volumes/HOLE-RAID-DRIVE/...`) for bulk operations
- **Never use iCloud library** (`/Volumes/80F9F6D9.../...`) for scanning or batch processing
- Expected performance: 10-20 fonts/second on RAID drive
- Large databases (8+ MB) should NOT be committed to git

### User Preferences

From `SESSION-MEMORY.md`:
- External organization tool: Use **FontBase** (not building custom solution)
- Simple structure: 3-folder layout (TTF/, OTF/, WOFF2/) - no complex trees
- **Python, not Rust**: User rejected experimental Rust rewrite
- Local storage: iCloud too slow for scanning, use RAID drive

---

## Common Workflows

### After Reboot

```bash
cd /Users/jth/Documents/HOLE-Fonttools-Project
uv sync --reinstall-package hole-fonts
cat PROJECT-STATUS.md
cat SESSION-MEMORY.md
uv run hole-fonts --help
```

### Scanning New Fonts

```bash
# Scan directory
uv run hole-fonts scan <new-fonts-dir> --output new-fonts-db.json

# Find duplicates against main database
uv run hole-fonts dedup HOLE-Fonts-RAID-Database.json --compare new-fonts-db.json

# Search for specific font
uv run hole-fonts search new-fonts-db.json --family "FontName"
```

### AgencyFB Test Case

AgencyFB is the reference test case with 27 unique variants:
- 5 width families (Compressed, Basic, Normal, etc.)
- 5 weights (Regular, Bold, Heavy, etc.)
- Each × 3 formats (TTF, OTF, WOFF2) = 81 total files

Use this for testing search functionality:
```bash
uv run hole-fonts search database.json --family "AgencyFB" --weight-min 400 --weight-max 400 --format woff2
```

### Building a Release

```bash
# Update version in pyproject.toml
# Update CHANGELOG.md with release notes
git add .
git commit -m "chore: bump version to X.Y.Z"
git tag vX.Y.Z
git push origin main --tags
uv build
```

---

## Important Notes

### Package Management

- **Always use `uv`**, never use `pip` directly
- After code changes: `uv sync --reinstall-package hole-fonts`
- After reboot: `uv sync` (reinstalls all dependencies)

### Volume Mounting

If volumes aren't mounted after reboot:
```bash
# Check RAID drive
ls /Volumes/HOLE-RAID-DRIVE

# Mount if needed
diskutil list
diskutil mount "HOLE-RAID-DRIVE"
```

### Database Files

- Database files are 8+ MB (don't commit to git)
- Use `.gitignore` to exclude `*.json` database files
- Databases are portable and can be shared separately

### Metadata Extraction (v2.0.0)

**Designer/Foundry metadata is now extracted directly from font files** (no Typekit needed):
- 93.9% designer coverage (23,257 of 24,767 fonts)
- 94.9% foundry coverage (23,516 of 24,767 fonts)
- 98.9% copyright coverage (24,505 fonts)
- Extracted from font name table (IDs 0, 8, 9, 10, 11, 12)

**Complete database**: `HOLE-Fonts-Complete-Database.json` (24,767 fonts)

### Typekit API (Legacy/Optional)

- API Key: `459aa874c56344b9c2f44b3a5edde401dc918fca` (stored in `config.yaml`)
- Most fonts are NOT in Typekit database (~0.25% coverage)
- **Not needed in v2.0+** - metadata extracted from font files directly
- Enrichment is optional and doesn't affect core functionality

### Claude Desktop Skill

- Skill location: `~/.claude/skills/hole-fonts/`
- Package: `hole-fonts.zip` (for distribution)
- Use `/convert-fonts` in Claude Desktop for interactive conversion

### CLI Deployment (v2.0.0)

**Package is ready for PyPI publication**:
- Built packages in `dist/`: wheel (32 KB) + source (465 KB)
- Complete documentation: INSTALLATION.md, PUBLISHING.md, USER-QUICKSTART.md
- MIT License included
- pyproject.toml configured with full PyPI metadata

**To publish**: See `PUBLISHING.md` for complete workflow
**Status**: Ready for TestPyPI and production PyPI release

---

## Troubleshooting

**"Module not found" errors:**
```bash
uv sync --reinstall-package hole-fonts
```

**"No such file or directory" for volumes:**
- Check if RAID drive is mounted: `ls /Volumes/HOLE-RAID-DRIVE`
- Mount if needed: `diskutil mount "HOLE-RAID-DRIVE"`

**Slow scanning performance:**
- Make sure you're using RAID drive, not iCloud location
- Expected: 10-20 fonts/second on RAID
- iCloud will be 100x slower

**Too many duplicate matches:**
- Check confidence threshold (should be ≥0.60)
- Review strict matching rules in `SESSION-MEMORY.md`
- Different weights/italic/widths should NEVER match

**Typekit enrichment not working:**
- Use `enrich_fonts.py` script instead of CLI command (CLI has a bug)
- Check API key in `config.yaml`
- Most fonts won't be in Typekit database (expected)

---

## Development Priorities

Based on `ROADMAP.md`, the current priorities are:

1. **v2.0.0 Release** (CURRENT) - Production-ready with full metadata, dedup, search
2. **v2.1.0** (Next) - Performance optimization, better error handling
3. **v2.2.0** (Future) - FontBase integration improvements
4. **v3.0.0** (Future) - Web catalog generation, advanced filtering

See `ROADMAP.md` for complete roadmap.

---

**Last Updated**: 2026-01-09
**Version**: 2.0.0
**Status**: Production-ready, tested on 11,047 font collection
