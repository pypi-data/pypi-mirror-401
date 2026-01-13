# HOLE Fonts - Quick Reference Card

## Essential Commands

### Export Fonts (Recommended)
```bash
# Single family
uv run python -m hole_fonts.cli export Input/FamilyName/

# All families (batch)
uv run python -m hole_fonts.cli export Input/Organized-Folders/

# Custom export location
uv run python -m hole_fonts.cli export Input/Fonts/ --to ~/FontBase-Library/

# Different structure
uv run python -m hole_fonts.cli export Input/Fonts/ --structure format-separated
```

### View Library
```bash
# List all families
uv run python -m hole_fonts.cli list

# Family details
uv run python -m hole_fonts.cli info AgencyFB

# Validate structure
uv run python -m hole_fonts.cli validate
```

### Convert Only (Legacy)
```bash
# Convert to library (old way)
uv run python -m hole_fonts.cli convert Input/Fonts/
```

---

## Export Structures

### flat-by-family (Default)
```
Export/
└── AgencyFB/
    ├── AgencyFB-Bold.ttf
    ├── AgencyFB-Bold.otf
    └── AgencyFB-Bold.woff2
```
**Best for:** FontBase

### format-separated
```
Export/
└── AgencyFB/
    ├── OTF/
    ├── TTF/
    └── WOFF2/
```
**Best for:** Manual organization

### single-flat
```
Export/
├── AgencyFB-Bold.ttf
├── AgencyFB-Bold.otf
└── AgencyFB-Bold.woff2
```
**Best for:** Let FontBase organize

---

## FontBase Integration

### Setup (One Time)
1. Download: https://fontba.se/
2. Install and launch
3. Add Folder → `FontBase-Export/`
4. Enable "Watch for changes"

### Daily Use
```bash
# 1. Export new fonts
uv run python -m hole_fonts.cli export Input/NewFonts/

# 2. FontBase auto-imports (if watching)

# 3. Organize in FontBase using Collections
```

---

## File Organization Tips

### Input Directory Structure

**Recommended:**
```
Input/
├── Organized-Folders/
│   ├── AgencyFB/        ← Family folders
│   │   ├── font1.ttf
│   │   └── font2.ttf
│   ├── Helvetica/
│   └── ...
└── New-Downloads/
```

**Rule:** One folder = One family

### Output Structure

**Export directory:**
```
FontBase-Export/
├── AgencyFB/           ← Auto-detected from folder name
├── Helvetica/
└── ...
```

**Add to FontBase:** Point FontBase at `FontBase-Export/`

---

## Variable Fonts

**Automatic detection:**
- System detects fvar table
- Logs variation axes
- Preserves all variation data
- Marks with 🎨 in output

**Formats:**
- Variable fonts work in TTF and WOFF2
- OTF might not preserve variations (CFF2 dependent)

---

## Workflow Examples

### New Font Delivery
```bash
# Client sends fonts in Downloads/
uv run python -m hole_fonts.cli export \
    ~/Downloads/ClientFonts/ \
    --to ~/FontBase-Library/

# Organize in FontBase
# → Create Collection: "Client ABC"
# → Add fonts to collection
```

### Web Project
```bash
# Need WOFF2 only
uv run python -m hole_fonts.cli export \
    Input/WebFonts/ \
    --formats woff2 \
    --to WebProject/public/fonts/
```

### Archive Preparation
```bash
# All formats for archival
uv run python -m hole_fonts.cli export \
    Input/Archive/ \
    --structure format-separated \
    --to Archive-Library/
```

---

## Troubleshooting

### Export failed?
- Check input directory exists
- Verify fonts are valid
- Check disk space
- Review `hole-fonts.log`

### Fonts not in FontBase?
- Refresh folder in FontBase
- Check folder was added
- Verify export directory path

### Variable font not detected?
- Check if font has fvar table
- View logs for detection info
- Some "variable" fonts might be static instances

---

## Configuration

**Edit:** `config.yaml`

```yaml
export:
  default_path: 'FontBase-Export'
  structure: 'flat-by-family'

formats:
  - ttf
  - otf
  - woff2
```

---

## Tips

1. **Always keep originals** - Never delete source fonts
2. **Use Collections** - Virtual organization in FontBase
3. **Activate sparingly** - Only activate fonts you're using
4. **Regular cleanup** - Remove unused fonts
5. **Cloud backup** - Keep Input/ in Dropbox/iCloud

---

## What's Next?

### v0.2: Metadata Integration
- Adobe Typekit API
- Font metadata (designer, foundry)
- Smart duplicate detection
- Search functionality

### v0.3: Advanced Features
- CSS @font-face generation
- Font subsetting
- Web font optimization
- License tracking

---

**HOLE Fonts + FontBase = Professional Font Workflow** ✨
