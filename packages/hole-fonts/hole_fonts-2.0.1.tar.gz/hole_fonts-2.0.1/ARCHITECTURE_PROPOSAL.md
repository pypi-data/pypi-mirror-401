# HOLE Fonts - Proposed Architecture v2.0

## Problem Analysis

### Current Issues
1. ❌ **Confusion between conversion and organization**
2. ❌ **Folder structure doesn't match user preference**
3. ❌ **Difficult to reorganize without reconverting**
4. ❌ **Past problems with font family detection**

### User Requirements
```
Desired structure:
Library/
└── AgencyFB/               ← Family folder (from original parent)
    ├── AgencyFB-OTF/      ← Format folders with family prefix
    │   ├── AgencyFB-Bold.otf
    │   ├── AgencyFB-Regular.otf
    │   └── ...
    ├── AgencyFB-TTF/
    │   └── ...
    └── AgencyFB-WOFF2/
        └── ...
```

## Proposed Solution: Two-Module Architecture

### Module 1: Font Converter (Pure Conversion)
**Purpose:** Convert fonts between formats
**Responsibility:** ONLY format conversion
**Output:** Flat directory of converted fonts

```
Output/
├── AgencyFB-Bold.ttf
├── AgencyFB-Bold.otf
├── AgencyFB-Bold.woff2
├── AgencyFB-Regular.ttf
├── AgencyFB-Regular.otf
├── AgencyFB-Regular.woff2
└── ...
```

**Commands:**
```bash
# Convert single font
hole-fonts convert font.ttf

# Convert directory (all fonts flat)
hole-fonts convert Input/AgencyFB/

# Output all conversions to staging area
hole-fonts convert Input/Organized-Folders/ --staging
```

**Features:**
- ✓ TTF ↔ OTF ↔ WOFF2 conversion
- ✓ Variable font detection & preservation
- ✓ Batch processing
- ✓ NO organization decisions
- ✓ Fast, simple, repeatable

### Module 2: Library Organizer (Smart Organization)
**Purpose:** Organize converted fonts into library
**Responsibility:** ONLY organization logic
**Input:** Directory of converted fonts
**Output:** Organized library

```
Library/
└── AgencyFB/
    ├── AgencyFB-OTF/
    ├── AgencyFB-TTF/
    └── AgencyFB-WOFF2/
```

**Commands:**
```bash
# Organize converted fonts
hole-fonts organize Output/ --library Library/

# Organize with family detection
hole-fonts organize Output/ --auto-detect-families

# Organize with manual family name
hole-fonts organize Output/ --family "AgencyFB"

# Interactive mode (ask for each family)
hole-fonts organize Output/ --interactive

# Reorganize existing library
hole-fonts reorganize Library/ --new-structure
```

**Features:**
- ✓ Multiple organization strategies
- ✓ Family detection algorithms
- ✓ Manual overrides
- ✓ Reorganize without reconverting
- ✓ Preview before applying
- ✓ Undo capability

## Organization Strategies

### Strategy 1: Source Folder Name (Recommended)
**Use when:** Fonts are pre-organized in folders by family
**Logic:** Use parent directory name as family
```
Input/AgencyFB/*.ttf → Library/AgencyFB/
Input/Helvetica/*.ttf → Library/Helvetica/
```

### Strategy 2: PostScript Name Analysis
**Use when:** Fonts are mixed in one folder
**Logic:** Parse PostScript name to detect family
```
AgencyFB-Bold.ttf     → AgencyFB
Helvetica-Neue-Bold.ttf → Helvetica-Neue
```

### Strategy 3: Metadata-Based (v0.2)
**Use when:** Typekit metadata available
**Logic:** Use authoritative family name from API
```
Query Typekit → Get official family name
```

### Strategy 4: Manual Mapping
**Use when:** Automatic detection fails
**Logic:** User provides family_map.yaml
```yaml
families:
  AgencyFB:
    - AgencyFB*.ttf
    - 9866*.ttf
  Helvetica:
    - Helvetica*.ttf
    - Helv*.ttf
```

### Strategy 5: Interactive
**Use when:** User wants control
**Logic:** Prompt for each font or group
```
Found: AgencyFB-Bold.ttf, AgencyFB-Regular.ttf
Family name? [AgencyFB]: _
```

## Folder Structure Options

### Option A: Format-Prefixed (Your Request)
```
Library/
└── AgencyFB/
    ├── AgencyFB-OTF/
    ├── AgencyFB-TTF/
    └── AgencyFB-WOFF2/
```

### Option B: Simple Format (Current)
```
Library/
└── AgencyFB/
    ├── otf/
    ├── ttf/
    └── woff2/
```

### Option C: Flat with Suffixes
```
Library/
└── AgencyFB/
    ├── AgencyFB-Bold.otf
    ├── AgencyFB-Bold.ttf
    ├── AgencyFB-Bold.woff2
    └── ...
```

### Option D: Project-Based
```
Library/
├── Projects/
│   └── Website-2025/
│       └── AgencyFB/
└── Foundries/
    └── FontBureau/
        └── AgencyFB/
```

**Configuration:**
```yaml
# config.yaml
library:
  structure: "format-prefixed"  # Options: format-prefixed, simple, flat, project
  naming:
    prefix_format_folders: true  # AgencyFB-OTF vs otf
    use_family_prefix_in_files: false
```

## Implementation Plan

### Phase 1: Separate Modules

**1. Refactor Converter**
```python
# converter.py - Pure conversion, no organization
class FontConverter:
    def convert(self, input_path, output_dir):
        """Convert fonts, output to flat directory"""
        # ONLY converts, does NOT organize

# converter_cli.py
@click.command()
def convert(input_path, output_dir):
    """Convert fonts to multiple formats"""
    # No library organization here
```

**2. Create Organizer**
```python
# organizer.py - Separate module
class LibraryOrganizer:
    def __init__(self, library_path, structure="format-prefixed"):
        self.library_path = library_path
        self.structure = structure

    def organize(self, fonts_dir, strategy="source-folder"):
        """Organize fonts into library"""

    def detect_families(self, fonts_dir):
        """Smart family detection"""

    def preview(self, fonts_dir):
        """Preview organization before applying"""

    def apply(self, plan):
        """Apply organization plan"""

    def reorganize(self, new_structure):
        """Reorganize existing library"""

# organizer_cli.py
@click.command()
def organize(fonts_dir, library, strategy, interactive):
    """Organize converted fonts into library"""
```

**3. Update CLI**
```bash
# Workflow A: Two steps
hole-fonts convert Input/AgencyFB/ --output Staging/
hole-fonts organize Staging/ --library Library/ --family AgencyFB

# Workflow B: One step (convenience)
hole-fonts process Input/AgencyFB/ --family AgencyFB
# (Internally: convert → organize)

# Reorganize existing
hole-fonts reorganize Library/ --structure format-prefixed
```

### Phase 2: Family Detection Engine

**Smart Detection Algorithm:**
```python
def detect_font_family(font_path):
    """
    Multi-strategy family detection

    Returns: FamilyInfo(name, confidence, method)
    """
    strategies = [
        PostScriptNameStrategy(),    # Highest confidence
        FilenameStrategy(),           # Medium confidence
        ParentFolderStrategy(),       # Good for organized input
        MetadataStrategy(),           # Requires Typekit (v0.2)
    ]

    results = [s.detect(font_path) for s in strategies]
    return choose_best(results)  # Pick highest confidence
```

**Family Grouping:**
```python
def group_fonts_by_family(font_paths):
    """
    Group fonts into families

    Returns: {
        'AgencyFB': [font1.ttf, font2.ttf, ...],
        'Helvetica': [font3.ttf, ...]
    }
    """
    families = defaultdict(list)

    for font_path in font_paths:
        family_info = detect_font_family(font_path)

        if family_info.confidence < 0.7:
            # Low confidence - ask user or use fallback
            family_name = ask_user_or_fallback(font_path)
        else:
            family_name = family_info.name

        families[family_name].append(font_path)

    return dict(families)
```

### Phase 3: Reorganization Tool

**Ability to reorganize without reconverting:**
```bash
# Change structure
hole-fonts reorganize Library/ \
    --from simple \
    --to format-prefixed

# Preview changes
hole-fonts reorganize Library/ \
    --to format-prefixed \
    --dry-run

# Merge families
hole-fonts merge-families Library/AgencyFB Library/AgencyFBCompressed \
    --into Library/AgencyFB

# Split family
hole-fonts split-family Library/AgencyFB \
    --by weight \
    --into Library/AgencyFB-{weight}
```

## Benefits of This Architecture

### 1. Separation of Concerns
- Converter: Fast, simple, repeatable
- Organizer: Flexible, intelligent, reversible

### 2. Flexibility
- Try different organizations without reconverting
- Switch structures easily
- Manual intervention when needed

### 3. Error Recovery
- Conversion errors don't affect organization
- Organization errors don't lose conversions
- Can reorganize anytime

### 4. Performance
- Convert once, organize many times
- Parallel conversion possible
- Incremental updates easier

### 5. Future-Proof
- Easy to add new organization strategies
- Can integrate with external tools
- Modular for testing

## Migration from v0.1

**Backward Compatibility:**
```bash
# Old way still works (for simple cases)
hole-fonts convert Input/AgencyFB/
# → Converts AND organizes (using defaults)

# New way (more control)
hole-fonts convert Input/AgencyFB/ --staging
hole-fonts organize Staging/ --family AgencyFB --structure format-prefixed
```

**Reorganize existing library:**
```bash
# Update v0.1 library to v2.0 structure
hole-fonts reorganize Library/ \
    --from simple \
    --to format-prefixed \
    --backup
```

## Example Workflows

### Workflow 1: Simple Project
```bash
# One command (like v0.1)
hole-fonts process Input/MyFont/ --family "MyFont"
```

### Workflow 2: Careful Organization
```bash
# Step by step
hole-fonts convert Input/Mixed-Fonts/ --output Staging/
hole-fonts organize Staging/ --interactive --library Library/
```

### Workflow 3: Batch with Manual Control
```bash
# Convert all
hole-fonts convert Input/Organized-Folders/ --output Staging/

# Preview organization
hole-fonts organize Staging/ --preview > plan.txt
# Review plan.txt

# Apply
hole-fonts organize Staging/ --library Library/ --apply
```

### Workflow 4: Fix Past Mistakes
```bash
# Already converted wrong? Just reorganize!
hole-fonts reorganize Library/ \
    --strategy postscript-name \
    --structure format-prefixed
```

## Recommendation

**Implement the two-module architecture:**

1. **Keep converter simple** - Pure conversion, no organization logic
2. **Make organizer powerful** - Multiple strategies, preview, reorganize
3. **Provide both workflows** - Simple one-step AND detailed two-step
4. **Enable experimentation** - Reorganize without reconverting

This gives you:
- ✅ Control when you need it
- ✅ Simplicity when you don't
- ✅ Ability to fix mistakes
- ✅ Future flexibility

**Next step:** Should I implement this architecture?
