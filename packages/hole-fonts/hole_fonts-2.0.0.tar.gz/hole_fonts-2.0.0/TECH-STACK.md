# HOLE Fonts - Technical Stack

**Project:** HOLE Foundation Font Management System
**Version:** v1.0.0
**Date:** December 2025

---

## Core Stack

### Language & Runtime

**Python 3.14**
- Primary development language
- Type hints and modern Python features
- Chosen for: FontTools ecosystem, rich libraries

**Package Manager: uv**
- Fast Python package manager
- Replaces pip + virtualenv
- Dependency resolution
- Lock file management (uv.lock)

**Build System: Hatchling**
- Modern Python build backend
- PEP 517/518 compliant
- Editable installs
- Package distribution

---

## Core Dependencies

### Font Processing

**FontTools 4.61.1+** (with WOFF extras)
- **Purpose:** Core font conversion engine
- **Features:**
  - TTF/OTF reading and writing
  - WOFF2 compression/decompression
  - Variable font support (fvar, gvar, avar, STAT)
  - Font table manipulation
  - Format transformation
- **License:** MIT
- **Repository:** https://github.com/fonttools/fonttools

**Brotli** (via fonttools[woff])
- **Purpose:** WOFF2 compression
- **Features:** Fast compression algorithm
- **Used by:** WOFF2 generation

**Zopfli** (via fonttools[woff])
- **Purpose:** WOFF compression optimization
- **Features:** Better compression than gzip

---

### CLI & UI

**Click 8.1.0+**
- **Purpose:** Command-line interface framework
- **Features:**
  - Command groups
  - Options and arguments
  - Help generation
  - Context passing
- **Usage:** All CLI commands (export, convert, list, info)

**Rich 13.0.0+**
- **Purpose:** Terminal formatting and UI
- **Features:**
  - Beautiful tables
  - Progress bars
  - Syntax highlighting
  - Panels and layout
  - Emoji support (🎨)
- **Usage:** All terminal output, progress tracking

---

### Configuration & Data

**PyYAML 6.0+**
- **Purpose:** Configuration file parsing
- **Features:**
  - YAML reading/writing
  - Safe loading
  - Python object serialization
- **Usage:** config.yaml parsing

**JSON** (built-in)
- **Purpose:** Metadata storage (future v0.2)
- **Features:** Native Python support
- **Usage:** Font metadata database (planned)

---

### HTTP & APIs (Future)

**Requests 2.31.0+**
- **Purpose:** HTTP client for API calls
- **Features:**
  - Simple API interface
  - Session management
  - Error handling
- **Usage:** Adobe Typekit API (v0.2)

**aiohttp** (planned v0.2)
- **Purpose:** Async API calls
- **Features:**
  - Concurrent requests
  - Better performance
- **Usage:** Batch Typekit queries

---

## Development Tools

### Code Quality

**Black** (recommended)
- Code formatting
- PEP 8 compliance

**Ruff** (recommended)
- Fast linting
- Error checking

**mypy** (recommended)
- Type checking
- Static analysis

### Version Control

**Git**
- Source control
- Branch: HOLE-FONTS-Ext
- Repository: Local

---

## External Tools & Services

### Font Management

**FontBase** (Free, Optional)
- **Purpose:** Visual font management
- **Features:**
  - Font browsing and preview
  - Collections
  - Font activation
  - Search and filter
  - Google Fonts integration
- **Website:** https://fontba.se/
- **Usage:** End-user font organization

---

### Cloud Storage (Planned)

**CloudFlare R2**
- **Purpose:** Cloud font storage and CDN delivery
- **Features:**
  - S3-compatible API
  - Low-cost storage
  - No egress fees
  - Global distribution
- **Usage:** Web font hosting, team collaboration

**rclone** (Future)
- **Purpose:** R2 synchronization
- **Features:**
  - Cloud storage sync
  - Multiple cloud providers
  - Bandwidth limiting
- **Usage:** Upload fonts to R2

**macFUSE** (Future)
- **Purpose:** Mount R2 bucket as local drive
- **Features:**
  - FUSE filesystem
  - Cloud storage mounting
  - Appears as local volume
- **Website:** https://osxfuse.github.io/
- **Usage:** Access R2 fonts as local files

---

### APIs & Services

**Adobe Typekit API** (Planned v0.2)
- **Purpose:** Font metadata enrichment
- **Endpoint:** https://typekit.com/api/v1/json
- **API Key:** beea03b82c5b7f168058ef9d33815eb8b15abf4b
- **Data:**
  - Font family information
  - Designer attribution
  - Foundry details
  - Classifications
  - Font history

---

## Platform & System

### Operating System

**macOS** (Primary)
- Darwin kernel
- Version: 25.1.0+
- Tested on: Apple Silicon and Intel

**Cross-platform Support:**
- Linux (supported)
- Windows (supported via WSL or native)

### File Systems

**APFS** (Apple File System)
- Modern macOS filesystem
- Snapshot support
- Space sharing

**External Drives**
- HFS+, exFAT supported
- Network volumes supported
- Cloud sync (iCloud) supported

---

## Project Structure

### Package Layout

```
hole-fonts/
├── hole_fonts/              # Python package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # CLI interface (Click + Rich)
│   ├── converter.py        # Font conversion (FontTools)
│   ├── exporter.py         # Export logic
│   ├── organizer.py        # Library organization (legacy)
│   └── config.py           # Configuration (PyYAML)
├── .claude/
│   └── skills/
│       └── hole-fonts/     # Claude Desktop skill
├── scripts/
│   ├── organize-by-format.py      # Format organization
│   ├── export-and-organize.sh     # Combined workflow
│   └── process-all-fonts.sh       # Batch processing
├── pyproject.toml          # Package metadata (Hatchling)
├── config.yaml             # User configuration (PyYAML)
└── uv.lock                 # Dependency lock file (uv)
```

---

## Data Flow

### Font Conversion Pipeline

```
Input Font (TTF/OTF/WOFF/WOFF2)
    ↓
[FontTools TTFont] Load font
    ↓
[Variable Font Detection] Check fvar table
    ↓
[Format Conversion]
    ├→ TTF (save with glyf tables)
    ├→ OTF (save with CFF tables)
    └→ WOFF2 (compress with Brotli)
    ↓
[Export System]
    ├→ single-flat (all together)
    ├→ flat-by-family (family folders)
    └→ format-separated (family/format)
    ↓
Output Files (TTF, OTF, WOFF2)
    ↓
[organize-by-format.py] (optional)
    ↓
Organized Output (TTF/, OTF/, WOFF2/)
```

### Metadata Flow (Planned v0.2)

```
Font File
    ↓
[FontTools] Extract basic info
    ├→ PostScript name
    ├→ Family name
    ├→ Weight/Width/Style
    └→ Variable axes (if applicable)
    ↓
[Typekit API] Enrich metadata
    ├→ Designer
    ├→ Foundry
    ├→ Classification
    └→ History
    ↓
[Database] Store in JSON
    ↓
[Search System] Query and filter
```

---

## Architecture Patterns

### Design Patterns

**Module Separation:**
- `converter.py` - Pure conversion logic
- `exporter.py` - Export organization
- `cli.py` - User interface
- `config.py` - Configuration management

**Single Responsibility:**
- Each module has one clear purpose
- Easy to test and maintain
- Simple to extend

**Dependency Injection:**
- Config passed to modules
- Testable components
- Flexible configuration

### Code Organization

**Pythonic Conventions:**
- Type hints throughout
- Docstrings for all functions
- PEP 8 style guide
- Clear naming

**Error Handling:**
- Try/except blocks
- Logging for debugging
- Graceful degradation
- User-friendly error messages

---

## Performance Characteristics

### Speed

**Conversion:**
- Single font: 2-3 seconds
- Small batch (10 fonts): 20-30 seconds
- Large batch (1000 fonts): 30-60 minutes
- Variable fonts: Same speed as static

**Organization:**
- Script-based: ~1 second per 100 files
- 10,000 files: ~2 minutes
- 50,000 files: ~10 minutes

### Memory

**Converter:**
- Per font: ~10-50 MB
- Batch processing: ~100-500 MB
- Large fonts (CJK): Up to 200 MB per font

**Organizer:**
- File copy: Minimal memory
- Mostly I/O bound

### Disk I/O

**Bottlenecks:**
- WOFF2 compression (CPU intensive)
- Large font reading (I/O intensive)
- Network drives (slower than local)

**Optimizations:**
- Batch processing where possible
- Efficient file copying
- Progress tracking without slowdown

---

## Technology Choices

### Why Python?

✅ **FontTools ecosystem** - Industry standard
✅ **Rich libraries** - CLI, terminal UI, HTTP
✅ **Type safety** - Type hints for reliability
✅ **Cross-platform** - Works everywhere
✅ **Easy maintenance** - Readable, maintainable code

### Why FontTools?

✅ **Industry standard** - Used by Google Fonts, Adobe
✅ **Complete** - Handles all font formats
✅ **Variable fonts** - Full support
✅ **Maintained** - Active development
✅ **Open source** - MIT license

### Why Click + Rich?

✅ **User-friendly** - Beautiful terminal UI
✅ **Professional** - Industry-standard CLI framework
✅ **Powerful** - Handles complex commands
✅ **Documented** - Excellent documentation

### Why uv?

✅ **Fast** - Rust-based, extremely fast
✅ **Modern** - Better than pip
✅ **Reliable** - Lock files for reproducibility
✅ **Future** - Next-gen Python tooling

---

## Future Stack Additions

### Version 0.2 (Metadata)

**Add:**
- SQLite or JSON database
- Typekit API client
- Search indexing (possibly whoosh or SQLite FTS)

### Version 0.3 (Advanced)

**Add:**
- CSS generator
- Font subsetting (fonttools subset)
- Preview generation (Pillow, ReportLab)

### Version 1.0 (Enterprise)

**Add:**
- Web interface (FastAPI or Flask)
- Authentication (JWT)
- Team features (PostgreSQL)

---

## Integration Points

### Current Integrations

**✅ FontTools**
- Core conversion engine
- Variable font detection
- Format transformation

**✅ Claude Desktop**
- Skill-based invocation
- Natural language interface
- Workflow automation

**✅ File System**
- Local storage
- External drives
- Network volumes
- iCloud sync

### Planned Integrations (v0.2+)

**🔜 Adobe Typekit**
- Metadata enrichment
- Font information

**🔜 CloudFlare R2**
- Cloud storage
- CDN delivery
- Team collaboration

**🔜 macFUSE**
- Cloud drive mounting
- Seamless cloud access

**🔜 FontBase**
- Visual management
- Collections sync
- Search integration

---

## Development Environment

### Required

- Python 3.14+
- uv package manager
- Git
- macOS, Linux, or Windows

### Recommended

- VS Code or PyCharm
- Terminal with color support
- External storage for fonts
- Cloud backup (Dropbox, iCloud)

---

## Deployment

### Installation

```bash
# Clone repository
git clone <repo-url>

# Install dependencies
uv sync

# Run
uv run python -m hole_fonts.cli export Input/
```

### Distribution

**Claude Desktop Skill:**
- Packaged as .zip file
- Install in Claude skills directory
- Natural language invocation

**Standalone Script:**
- Can run without installation
- Portable Python package
- Cross-platform compatible

---

## Technology Summary

**Stack:**
- **Language:** Python 3.14
- **Package Manager:** uv
- **Build:** Hatchling
- **CLI:** Click
- **UI:** Rich
- **Font Engine:** FontTools
- **Config:** PyYAML
- **Future DB:** JSON/SQLite
- **Future API:** Adobe Typekit
- **Future Cloud:** CloudFlare R2
- **Future Mount:** macFUSE

**Philosophy:**
- ✅ Use existing tools (don't reinvent)
- ✅ Simple, practical solutions
- ✅ Professional-grade quality
- ✅ Easy to maintain
- ✅ Ready to scale

---

**Simple stack. Powerful results.** 🚀
