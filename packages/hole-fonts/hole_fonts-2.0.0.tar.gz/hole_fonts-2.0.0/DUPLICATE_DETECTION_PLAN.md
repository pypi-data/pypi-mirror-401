# Duplicate Detection System - v0.2 Plan

## Problem Statement

**Current limitation (v0.1):**
- Filename-based duplicate checking only
- Same font with different filename → Creates duplicate
- No content verification
- No version tracking
- No cross-format duplicate detection

**Example issues:**
```
Input/
├── AgencyFB-Bold.ttf        ← Original
└── AgencyFB-Bold-copy.ttf   ← Duplicate (different name)

Result: Both imported as separate fonts ❌
```

## Solution: Font Fingerprinting + Metadata Database

### Architecture

Each font family gets a `metadata.json` file tracking all fonts:

```
Library/
└── AgencyFB/
    ├── metadata.json    ← Font registry
    ├── ttf/
    ├── otf/
    └── woff2/
```

### Metadata Schema

```json
{
  "family_name": "AgencyFB",
  "last_updated": "2025-12-26T12:00:00Z",
  "fonts": [
    {
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "font_identity": {
        "postscript_name": "AgencyFB-Bold",
        "full_name": "Agency FB Bold",
        "version": "1.000",
        "checksum_sha256": "abc123def456...",
        "unique_id": "Adobe:AgencyFB-Bold:2020"
      },
      "source": {
        "original_filename": "9866842-AgencyFBBold.ttf",
        "import_date": "2025-12-26T12:00:00Z",
        "import_path": "Input/AgencyFb/9866842-AgencyFBBold.ttf"
      },
      "variations": {
        "ttf": {
          "filename": "9866842-AgencyFBBold.ttf",
          "checksum": "ttf_checksum...",
          "size": 36112,
          "format_specific": {
            "is_variable": false,
            "tables": ["glyf", "head", "hhea", ...]
          }
        },
        "otf": {
          "filename": "9866842-AgencyFBBold.otf",
          "checksum": "otf_checksum...",
          "size": 34200,
          "format_specific": {
            "is_variable": false,
            "tables": ["CFF ", "head", "hhea", ...]
          }
        },
        "woff2": {
          "filename": "9866842-AgencyFBBold.woff2",
          "checksum": "woff2_checksum...",
          "size": 28000
        }
      },
      "metadata": {
        "designer": "Morris Fuller Benton",
        "foundry": "Font Bureau",
        "license": "Commercial",
        "typekit_id": "gmsj",
        "classifications": {
          "category": "sans-serif",
          "weight": 700,
          "width": "normal"
        }
      },
      "variable_font": null
    }
  ]
}
```

### Duplicate Detection Algorithm

```python
def is_duplicate(new_font_path: Path, family_metadata: dict) -> tuple[bool, str]:
    """
    Check if font is duplicate using multiple signals

    Returns:
        (is_duplicate, matching_uuid or None)
    """
    # Extract font identity
    font = TTFont(new_font_path)
    postscript_name = font['name'].getDebugName(6)  # PostScript name
    version = font['head'].fontRevision
    checksum = calculate_font_checksum(font)

    # Check against existing fonts
    for existing_font in family_metadata['fonts']:
        identity = existing_font['font_identity']

        # Method 1: PostScript name + version (strong signal)
        if (identity['postscript_name'] == postscript_name and
            identity['version'] == version):
            return True, existing_font['uuid']

        # Method 2: Content checksum (strongest signal)
        if identity['checksum_sha256'] == checksum:
            return True, existing_font['uuid']

        # Method 3: Unique ID from name table
        if 'unique_id' in identity and identity['unique_id']:
            font_unique_id = font['name'].getDebugName(3)
            if identity['unique_id'] == font_unique_id:
                return True, existing_font['uuid']

    return False, None


def calculate_font_checksum(font: TTFont) -> str:
    """
    Generate content-based checksum

    Uses stable tables only (ignores timestamps, metadata)
    """
    import hashlib

    # Tables to include in fingerprint (stable content)
    stable_tables = ['glyf', 'CFF ', 'head', 'hhea', 'hmtx',
                     'maxp', 'name', 'post', 'OS/2',
                     'fvar', 'gvar', 'avar']  # Include variable font tables

    hasher = hashlib.sha256()
    for table_tag in sorted(stable_tables):
        if table_tag in font:
            table_data = font.getTableData(table_tag)
            hasher.update(table_data)

    return hasher.hexdigest()
```

### Import Workflow with Duplicate Detection

```python
def import_font(source_path: Path, family_name: str) -> ImportResult:
    """Enhanced import with duplicate detection"""

    # Load family metadata
    metadata_path = library_path / family_name / 'metadata.json'
    metadata = load_or_create_metadata(metadata_path)

    # Check for duplicates
    is_dup, existing_uuid = is_duplicate(source_path, metadata)

    if is_dup:
        logger.info(f"Duplicate detected: {source_path.name}")
        logger.info(f"Matches existing font: {existing_uuid}")

        # Options:
        # 1. Skip entirely
        # 2. Update existing entry (if newer version)
        # 3. Ask user
        return ImportResult(
            status='skipped',
            reason='duplicate',
            existing_uuid=existing_uuid
        )

    # Not a duplicate - proceed with import
    font_uuid = str(uuid.uuid4())

    # Convert to all formats
    converted = converter.convert(source_path, ['ttf', 'otf', 'woff2'])

    # Create metadata entry
    font_entry = create_font_entry(
        uuid=font_uuid,
        source_path=source_path,
        converted_files=converted,
        metadata=extract_metadata(source_path)
    )

    # Add to family metadata
    metadata['fonts'].append(font_entry)
    save_metadata(metadata_path, metadata)

    return ImportResult(status='imported', uuid=font_uuid)
```

## Variable Fonts Support

### Detection

```python
def is_variable_font(font: TTFont) -> bool:
    """Check if font is a variable font"""
    return 'fvar' in font  # fvar table = variable font


def get_variation_axes(font: TTFont) -> list:
    """Extract variation axes from variable font"""
    if 'fvar' not in font:
        return []

    axes = []
    for axis in font['fvar'].axes:
        axes.append({
            'tag': axis.axisTag,
            'name': axis.axisNameID,
            'min': axis.minValue,
            'default': axis.defaultValue,
            'max': axis.maxValue
        })
    return axes
```

### Metadata for Variable Fonts

```json
{
  "uuid": "...",
  "font_identity": {
    "postscript_name": "InterVariable",
    "version": "4.0"
  },
  "variable_font": {
    "is_variable": true,
    "axes": [
      {
        "tag": "wght",
        "name": "Weight",
        "min": 100,
        "default": 400,
        "max": 900
      },
      {
        "tag": "slnt",
        "name": "Slant",
        "min": -10,
        "default": 0,
        "max": 0
      }
    ],
    "instances": [
      "InterVariable-Thin",
      "InterVariable-Regular",
      "InterVariable-Bold"
    ]
  },
  "variations": {
    "ttf": "InterVariable.ttf",
    "woff2": "InterVariable.woff2"
    // Note: Variable fonts usually stay in TTF/WOFF2 format
  }
}
```

## Benefits

### Duplicate Prevention
- ✓ Same font, different filename → Detected
- ✓ Cross-format detection (TTF vs OTF of same font)
- ✓ Version tracking
- ✓ Source attribution

### Version Management
```bash
# Scenario: Importing updated version
Input/
└── AgencyFB-Bold-v2.ttf  # Newer version

# System detects:
# - Same PostScript name: "AgencyFB-Bold"
# - Different version: 2.000 (was 1.000)
# - Different checksum

# Options:
# 1. Keep both versions
# 2. Replace old version
# 3. Mark as update
```

### Cross-Project Deduplication

```json
{
  "usage": {
    "projects": [
      {
        "name": "Website Redesign 2025",
        "date": "2025-01-15",
        "license_verified": true
      },
      {
        "name": "Brand Guidelines",
        "date": "2025-03-20",
        "license_verified": true
      }
    ],
    "total_deployments": 12
  }
}
```

## Implementation Phases

### v0.2 - Core System
- [ ] Metadata schema implementation
- [ ] Font fingerprinting (PostScript name + version + checksum)
- [ ] UUID generation and tracking
- [ ] Basic duplicate detection
- [ ] Variable font detection
- [ ] Metadata persistence

### v0.3 - Advanced Features
- [ ] Version comparison and upgrade workflows
- [ ] Multi-library support with global deduplication
- [ ] Font usage tracking across projects
- [ ] License compliance checking
- [ ] Metadata search and filtering

### v0.4 - Team Features
- [ ] Shared font registry
- [ ] Conflict resolution for team environments
- [ ] Audit logs
- [ ] Font approval workflows

## Migration from v0.1

When upgrading from v0.1 to v0.2:

```python
def migrate_to_metadata_system():
    """Scan existing library and create metadata files"""

    for family_dir in library_path.glob('*/'):
        if not family_dir.is_dir():
            continue

        metadata = {
            "family_name": family_dir.name,
            "last_updated": datetime.now().isoformat(),
            "fonts": []
        }

        # Scan existing fonts
        for ttf_file in (family_dir / 'ttf').glob('*.ttf'):
            font_entry = analyze_and_create_entry(ttf_file)
            metadata['fonts'].append(font_entry)

        # Save metadata
        save_metadata(family_dir / 'metadata.json', metadata)
```

## Summary

**v0.1 (Current):** Filename-based duplicate prevention ✓
**v0.2 (Planned):** Content-based duplicate detection with UUID tracking 🎯
**v0.3+:** Version management, usage tracking, team features 🚀

The UUID/database system will make HOLE Fonts enterprise-ready for managing large font collections across teams and projects.
