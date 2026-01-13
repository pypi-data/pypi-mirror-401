# HOLE Fonts - Comprehensive Implementation Plan

## Project Overview

**HOLE Fonts** is a font library management system designed to convert, organize, and catalog fonts with comprehensive metadata integration.

### Project Goals
- **v0.1**: Core font conversion and library management system
- **v0.2**: Adobe Typekit API integration for metadata enrichment

---

## Phase 1: Core Font Conversion System (v0.1)

### 1.1 Font Conversion Engine

**Objective**: Build a robust converter that handles TTF, OTF, and WOFF2 formats

**Technical Approach**:
- Use `fontTools.ttLib.TTFont` for reading/writing fonts
- Implement bidirectional conversion (TTF ↔ OTF) using fonttools
- Use `fonttools ttLib.woff2 compress` for WOFF2 generation
- Handle edge cases (invalid fonts, missing tables, format-specific features)

**Key Components**:
```python
# Core conversion functions:
- convert_to_ttf(input_path) → TTF output
- convert_to_otf(input_path) → OTF output
- convert_to_woff2(input_path) → WOFF2 output
- process_font(input_path) → {ttf, otf, woff2}
```

**Implementation Details**:
1. **TTF/OTF Conversion**:
   - Load font using `TTFont(input_path)`
   - Save with appropriate flavor: `font.save(output_path, flavor='woff2')`
   - For OTF→TTF: May need `cu2qu` module for curve conversion

2. **WOFF2 Generation**:
   - Command-line: `fonttools ttLib.woff2 compress input.ttf output.woff2`
   - Python API: `font.flavor = 'woff2'` then `font.save()`

3. **Error Handling**:
   - Validate input files before conversion
   - Log conversion errors with file context
   - Skip corrupted fonts but continue batch processing

### 1.2 Directory Structure & Organization

**Target Structure**:
```
HOLE-Font-Library(Fonttools)/
├── AgencyFB/
│   ├── otf/
│   │   └── AgencyFB-Regular.otf
│   ├── ttf/
│   │   └── AgencyFB-Regular.ttf
│   └── woff2/
│       └── AgencyFB-Regular.woff2
├── Helvetica/
│   ├── otf/
│   ├── ttf/
│   └── woff2/
└── ...
```

**Implementation**:
```python
def organize_font_output(font_name, conversions):
    """
    Create directory structure and move converted files

    Args:
        font_name: Base name of font family
        conversions: Dict with {format: file_path}
    """
    base_dir = LIBRARY_PATH / font_name
    for format in ['otf', 'ttf', 'woff2']:
        format_dir = base_dir / format
        format_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(conversions[format], format_dir)
```

**Considerations**:
- Handle fonts with multiple weights/styles (e.g., AgencyFB-Bold, AgencyFB-Italic)
- Normalize font family names (remove special characters, standardize casing)
- Detect and group related font files by family

### 1.3 Batch Processing System

**Features**:
- Process entire Input/ directory
- Progress tracking with status updates
- Parallel processing for multiple fonts (using multiprocessing)
- Resume capability for interrupted conversions

**CLI Interface**:
```bash
# Process single font
python main.py convert --input Input/AgencyFb/AgencyFB.ttf

# Process entire directory
python main.py convert --input Input/ --batch

# Process with custom output
python main.py convert --input Input/ --output /custom/path
```

### 1.4 Library Management

**Configuration** (`config.yaml`):
```yaml
library:
  path: '/Volumes/80F9F6D9-7BEF-4B9D-BE79-A7E2F900F1ED/Library/Daemon Containers/85C492CA-B246-4619-9E1D-E222C06C5FC9/Data/Library/Mobile Documents/com~apple~CloudDocs/HOLE-Foundation-Stuff/Brand/Fonts/HOLE-Font-Library/HOLE-Font-Library(Fonttools)'

input:
  path: 'Input/'

output:
  temp_path: 'Output/'

formats:
  - ttf
  - otf
  - woff2
```

**Features**:
- Automatic library path validation
- Catalog tracking (maintain index of processed fonts)
- Duplicate detection
- Version management for updated fonts

---

## Phase 2: Claude Code Skill Integration

### 2.1 Skill Structure

**Skill File**: `.claude/skills/hole-fonts/convert-fonts.md`

```yaml
---
name: convert-fonts
description: Convert fonts to TTF, OTF, and WOFF2 formats and organize into HOLE Font Library
---

# Font Conversion Skill

Convert a set of fonts to multiple formats and organize them into the HOLE Font Library.

## Usage
User: "Convert the fonts in Input/AgencyFb"
User: "Process all fonts in the Input directory"
User: "Convert Helvetica.ttf and create a kit"

## Process
1. Identify input fonts
2. Convert to TTF, OTF, and WOFF2
3. Organize into family directories
4. Move to library location
5. Generate conversion report
```

### 2.2 Command-Line Tool

**Features**:
- Simple invocation: `claude convert-fonts <font-path>`
- Integration with Claude Code workflows
- Rich output formatting (tables, progress bars)
- Error reporting with actionable suggestions

---

## Phase 3: Adobe Typekit Integration (v0.2)

### 3.1 API Integration

**API Configuration**:
```python
TYPEKIT_API_KEY = "beea03b82c5b7f168058ef9d33815eb8b15abf4b"
TYPEKIT_BASE_URL = "https://typekit.com/api/v1/json"
```

**Key Endpoints**:
1. **Get Font Family Details**:
   - `GET /families/{family_id}`
   - Returns: name, description, foundry, designer, classifications

2. **Search Families**:
   - `GET /libraries/full`
   - Use for discovering fonts and mapping names to IDs

3. **Get Variations**:
   - Embedded in family details
   - Returns all weights/styles with technical specifications

### 3.2 Metadata Enrichment

**Font Metadata Schema** (`metadata.json` per font family):
```json
{
  "family_name": "Agency FB",
  "designer": "Designer Name",
  "foundry": "Foundry Name",
  "classification": {
    "category": "sans-serif",
    "weight": "normal",
    "width": "normal"
  },
  "history": "Historical context and design notes",
  "variations": [
    {"name": "Regular", "weight": 400, "style": "normal"},
    {"name": "Bold", "weight": 700, "style": "normal"}
  ],
  "license": "License information",
  "year_released": 2020,
  "languages": ["Latin"],
  "source": "Adobe Typekit",
  "retrieved_at": "2025-12-26T12:00:00Z"
}
```

**Implementation**:
```python
async def fetch_font_metadata(font_name):
    """
    Query Typekit API for font metadata

    1. Search for font family by name
    2. Retrieve detailed family information
    3. Extract designer, foundry, history
    4. Save metadata.json alongside font files
    """
    # Search API for family ID
    search_url = f"{TYPEKIT_BASE_URL}/libraries/full"
    # Get family details
    family_url = f"{TYPEKIT_BASE_URL}/families/{family_id}"
    # Parse and structure metadata
```

### 3.3 Metadata Display & Search

**Features**:
- CLI command to view metadata: `python main.py info AgencyFB`
- Search fonts by designer: `python main.py search --designer "Morris Fuller Benton"`
- Search by foundry: `python main.py search --foundry "Adobe"`
- Generate HTML catalog with metadata
- Export metadata to CSV for analysis

---

## Phase 4: Advanced Features (Future)

### 4.1 Font Validation
- OpenType feature validation
- Glyph coverage analysis
- Hinting quality checks
- Web font optimization suggestions

### 4.2 Preview Generation
- Generate font specimen PDFs
- Create web preview pages
- Character set visualization
- CSS @font-face code generation

### 4.3 License Management
- Track font licenses
- Usage rights documentation
- Client project font tracking
- License compliance alerts

---

## Technical Stack

### Core Dependencies
```toml
[dependencies]
fonttools = {extras = ["woff"], version = ">=4.61.1"}
click = ">=8.1.0"  # CLI framework
requests = ">=2.31.0"  # API calls
pyyaml = ">=6.0"  # Configuration
rich = ">=13.0.0"  # Terminal formatting
aiohttp = ">=3.9.0"  # Async API calls
```

### Development Tools
- `pytest` - Testing framework
- `black` - Code formatting
- `mypy` - Type checking
- `ruff` - Linting

---

## Implementation Phases

### Phase 1A: Foundation (Week 1)
- [ ] Set up project structure
- [ ] Implement basic TTF/OTF conversion
- [ ] Create directory organization system
- [ ] Build configuration management

### Phase 1B: Core Features (Week 2)
- [ ] WOFF2 conversion
- [ ] Batch processing
- [ ] Error handling & logging
- [ ] CLI interface with Click

### Phase 1C: Testing & Polish (Week 3)
- [ ] Unit tests for conversion functions
- [ ] Integration tests for batch processing
- [ ] Documentation
- [ ] Claude skill implementation

### Phase 2: Typekit Integration (Week 4)
- [ ] API client implementation
- [ ] Metadata schema design
- [ ] Metadata fetching & storage
- [ ] Search & query functionality

### Phase 3: Enhancement (Week 5-6)
- [ ] Font validation tools
- [ ] Preview generation
- [ ] HTML catalog generator
- [ ] Performance optimization

---

## File Structure

```
HOLE-Fonttools-Project/
├── .claude/
│   └── skills/
│       └── hole-fonts/
│           └── convert-fonts.md
├── src/
│   ├── __init__.py
│   ├── converter.py          # Font conversion logic
│   ├── organizer.py          # Directory management
│   ├── metadata.py           # Typekit integration
│   ├── cli.py                # Command-line interface
│   ├── config.py             # Configuration handling
│   └── utils.py              # Helper functions
├── tests/
│   ├── test_converter.py
│   ├── test_metadata.py
│   └── fixtures/
├── Input/                     # Source fonts
├── Output/                    # Temporary conversion output
├── config.yaml               # User configuration
├── pyproject.toml
├── README.md
└── IMPLEMENTATION_PLAN.md
```

---

## Success Metrics

### v0.1 Success Criteria
- ✓ Successfully convert 100+ fonts without errors
- ✓ Proper organization in library structure
- ✓ Processing time < 5 seconds per font
- ✓ Claude skill functional and documented

### v0.2 Success Criteria
- ✓ Metadata retrieved for 90%+ of fonts
- ✓ Complete metadata schema implementation
- ✓ Search functionality operational
- ✓ Catalog generation working

---

## Risk Mitigation

### Technical Risks
1. **Font Format Incompatibility**: Some fonts may not convert cleanly
   - *Mitigation*: Comprehensive error handling, fallback strategies

2. **API Rate Limiting**: Typekit API may throttle requests
   - *Mitigation*: Implement rate limiting, caching, retry logic

3. **Library Path Access**: External drive may be unmounted
   - *Mitigation*: Path validation, graceful degradation to local storage

### Operational Risks
1. **Data Loss**: Conversion errors could corrupt fonts
   - *Mitigation*: Never delete source files, maintain backups

2. **Metadata Quality**: API data may be incomplete
   - *Mitigation*: Manual override capability, multiple data sources

---

## Next Steps

1. **Immediate Actions**:
   - Set up proper Python package structure
   - Implement basic font conversion (TTF→OTF→WOFF2)
   - Create configuration system
   - Test with existing AgencyFB fonts

2. **Short-term Goals** (This Week):
   - Complete v0.1 core functionality
   - Build CLI interface
   - Create Claude skill
   - Process first batch of fonts

3. **Medium-term Goals** (Next 2 Weeks):
   - Typekit API integration
   - Metadata enrichment
   - Search functionality
   - Documentation completion

---

## Documentation Resources

### FontTools
- [FontTools GitHub](https://github.com/fonttools/fonttools)
- [ttLib Documentation](https://fonttools.readthedocs.io/en/latest/ttLib/)
- WOFF2 CLI: `fonttools ttLib.woff2 compress`

### Adobe Typekit API
- [Typekit API Documentation](https://fonts.adobe.com/docs/api)
- [Font Library Endpoint](https://fonts.adobe.com/docs/api/font_library)
- API Key: `beea03b82c5b7f168058ef9d33815eb8b15abf4b`

### Related Tools
- [otf2ttf conversion](https://github.com/fonttools/fonttools) - CFF to TrueType
- [cu2qu](https://github.com/googlefonts/cu2qu) - Cubic to quadratic curves
