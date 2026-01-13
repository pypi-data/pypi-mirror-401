---
name: font-converter
description: Convert fonts to TTF, OTF, and WOFF2 formats and export for FontBase. Detects and preserves variable fonts automatically.
---

# HOLE Fonts - Professional Font Conversion

Convert fonts between formats (TTF, OTF, WOFF2) and export to FontBase-ready directory structure. Automatically detects and preserves variable font data.

## What This Skill Does

### Font Conversion
- ✅ Convert between TTF, OTF, WOFF, WOFF2
- ✅ Detect variable fonts automatically
- ✅ Preserve variation axes and instances
- ✅ Batch process entire directories
- ✅ Export in FontBase-friendly structure

### Variable Font Support
- **Auto-detects:** fvar table (font variations)
- **Preserves:** All variation axes (wght, wdth, slnt, opsz, custom)
- **Maintains:** Named instances and axis ranges
- **Indicates:** Variable fonts with 🎨 marker

### Export Structures

**flat-by-family** (Default - Best for FontBase)
```
FontBase-Export/
└── FamilyName/
    ├── Font-Bold.ttf
    ├── Font-Bold.otf
    ├── Font-Bold.woff2
    ├── Font-Regular.ttf
    ├── Font-Regular.otf
    └── Font-Regular.woff2
```

**format-separated** (Organized by format)
```
FontBase-Export/
└── FamilyName/
    ├── OTF/
    ├── TTF/
    └── WOFF2/
```

**single-flat** (All files together)
```
FontBase-Export/
├── Font-Bold.ttf
├── Font-Bold.otf
└── Font-Bold.woff2
```

## Usage Examples

### Example 1: Convert Single Font Family
**User:** "Convert the fonts in Input/Helvetica/ for FontBase"

**What happens:**
```bash
uv run python -m hole_fonts.cli export Input/Helvetica/ --to FontBase-Export/
```

**Result:**
- All fonts converted to TTF, OTF, WOFF2
- Exported to FontBase-Export/Helvetica/
- Variable fonts detected and marked
- Ready to import into FontBase

### Example 2: Batch Convert All Fonts
**User:** "Export all the fonts in Input/Organized-Folders/"

**What happens:**
```bash
uv run python -m hole_fonts.cli export Input/Organized-Folders/ --to FontBase-Export/
```

**Result:**
- Each subdirectory becomes a family
- All families processed in batch
- Progress shown with variable font indicators
- Complete export ready for FontBase

### Example 3: Web Fonts Only
**User:** "I need WOFF2 versions of the fonts in Input/WebProject/"

**What happens:**
```bash
uv run python -m hole_fonts.cli export Input/WebProject/ \
    --formats woff2 \
    --to WebProject/public/fonts/
```

**Result:**
- Only WOFF2 files generated
- Exported directly to web project
- Optimized for web deployment

### Example 4: Custom Export Structure
**User:** "Convert Input/ArchiveFonts/ with formats separated"

**What happens:**
```bash
uv run python -m hole_fonts.cli export Input/ArchiveFonts/ \
    --structure format-separated \
    --to Archive/
```

**Result:**
- Fonts organized by format in subdirectories
- Good for archival purposes
- Easy to find specific format

### Example 5: Specific Format Conversion
**User:** "Convert this font to TTF and OTF only"

**What happens:**
```bash
uv run python -m hole_fonts.cli export Input/Font.woff2 \
    --formats ttf otf
```

**Result:**
- Only TTF and OTF generated
- WOFF2 skipped
- Selective format conversion

## Common Scenarios

### Scenario 1: New Font Delivery
**Situation:** Client just sent fonts in Downloads/

**User:** "Process the new client fonts from Downloads/ClientABC/"

**Response:**
1. Run export command on Downloads/ClientABC/
2. Fonts exported to FontBase-Export/ClientABC/
3. FontBase auto-imports (if watching)
4. User can create Collection in FontBase for this client

### Scenario 2: Web Project Font Prep
**Situation:** Need web fonts for deployment

**User:** "Prepare web fonts from Input/WebsiteRedesign/"

**Response:**
1. Export only WOFF2 format
2. Output to web project directory
3. Fonts ready for CSS @font-face rules
4. Optimized for web delivery

### Scenario 3: Font Library Building
**Situation:** Building comprehensive font library

**User:** "Add these new typefaces to my font library"

**Response:**
1. Export to FontBase-Export/
2. FontBase automatically detects new fonts
3. User organizes with Collections in FontBase
4. Fonts available for activation

### Scenario 4: Variable Font Verification
**Situation:** Need to check if fonts are variable

**User:** "Check if these fonts are variable fonts"

**Response:**
1. Run export with detection enabled
2. Variable fonts marked with 🎨 in output
3. Log shows axis information (wght, wdth, slnt, etc.)
4. User knows which fonts have variations

### Scenario 5: Format-Specific Export
**Situation:** Need only specific formats

**User:** "Give me OTF versions of these fonts"

**Response:**
1. Export with --formats otf
2. Only OTF files generated
3. Faster processing (1/3 the formats)
4. Specific format for specific need

## How It Works

### Step 1: Font Detection
- Scans input directory
- Identifies font files (TTF, OTF, WOFF, WOFF2)
- Detects variable fonts (fvar table)
- Groups fonts by family (folder name)

### Step 2: Conversion
- Loads font with FontTools
- Checks for variable font data
- Converts to requested formats
- Preserves all metadata and tables
- Validates output

### Step 3: Export
- Organizes by chosen structure
- Names files consistently
- Creates family directories
- Exports to destination
- Reports variable fonts

### Step 4: FontBase Import
- User adds FontBase-Export/ to FontBase
- FontBase watches for changes
- New fonts auto-import
- User organizes with Collections
- Fonts ready for activation

## Technical Details

### Supported Input Formats
- TTF (TrueType Font)
- OTF (OpenType Font)
- WOFF (Web Open Font Format)
- WOFF2 (Web Open Font Format 2)

### Output Formats Generated
- TTF (desktop use, web)
- OTF (desktop use, print)
- WOFF2 (web deployment, optimal compression)

### Variable Font Tables Preserved
- fvar (font variations)
- gvar (glyph variations)
- avar (axis variations)
- STAT (style attributes)
- cvar (CVT variations)

### Variation Axes Supported
- **wght** - Weight (100-900)
- **wdth** - Width (50-200)
- **slnt** - Slant (-12 to 12)
- **ital** - Italic (0-100)
- **opsz** - Optical Size (6-72)
- **Custom axes** - SERF, CONT, HGHT, etc.

## Configuration

Edit `config.yaml` to customize:

```yaml
export:
  default_path: 'FontBase-Export'
  structure: 'flat-by-family'

formats:
  - ttf
  - otf
  - woff2
```

## Command Reference

### Basic Export
```bash
uv run python -m hole_fonts.cli export <input-path>
```

### With Custom Destination
```bash
uv run python -m hole_fonts.cli export <input-path> --to <output-path>
```

### With Specific Formats
```bash
uv run python -m hole_fonts.cli export <input-path> --formats ttf otf
```

### With Different Structure
```bash
uv run python -m hole_fonts.cli export <input-path> --structure format-separated
```

### Multiple Options
```bash
uv run python -m hole_fonts.cli export Input/Fonts/ \
    --to ~/FontBase-Library/ \
    --formats woff2 \
    --structure single-flat
```

## FontBase Integration

### Initial Setup (One Time)

1. **Install FontBase**
   - Download: https://fontba.se/
   - Free, modern, professional

2. **Add Folder**
   - In FontBase → Add Folder
   - Select: FontBase-Export/
   - Enable: Watch for changes

3. **Done!**
   - New fonts auto-import
   - Organize with Collections
   - Activate for projects

### Daily Workflow

```bash
# 1. Export new fonts
uv run python -m hole_fonts.cli export Input/NewFonts/

# 2. FontBase shows them immediately (if watching)

# 3. Organize in FontBase
# → Create Collection: "Project XYZ"
# → Add fonts to collection
# → Activate for design work
```

## Tips & Best Practices

### 1. Organization Strategy

**In FontBase, use Collections for:**
- **Projects:** "Website 2025", "Brand Guidelines"
- **Clients:** "Client ABC", "Client XYZ"
- **Foundries:** "Adobe", "Monotype", "Google Fonts"
- **Licenses:** "Commercial", "Personal Use", "Open Source"
- **Styles:** "Sans Serif", "Serif", "Display", "Script"

**Why Collections?**
- Virtual organization (fonts stay in place)
- One font can be in multiple collections
- Easy to reorganize anytime
- No file duplication

### 2. Keep Originals

- Always preserve source fonts in Input/
- Never delete original files
- Use cloud backup (Dropbox, iCloud)
- Can regenerate exports anytime

### 3. Variable Fonts

- Check logs for 🎨 marker
- Variable fonts work best in TTF and WOFF2
- OTF may not preserve all variation data (depends on CFF2)
- FontBase shows variation axes

### 4. Web Projects

- Export only WOFF2 for web use
- Smallest file size
- Best browser support
- Use --formats woff2 flag

### 5. Batch Processing

- Organize Input/ by family in folders
- Folder name becomes family name
- Process entire Input/Organized-Folders/ at once
- Takes 10-20 minutes for 100+ families

## Troubleshooting

### Export Not Working?

**Check:**
- Input path exists and contains fonts
- Fonts are valid (TTF, OTF, WOFF, WOFF2)
- Sufficient disk space
- Review hole-fonts.log for errors

### Variable Font Not Detected?

**Verify:**
- Font actually has fvar table (some "variable" fonts are static)
- Check logs for detection message
- Use font editor to confirm variations

### FontBase Not Showing Fonts?

**Try:**
- Refresh folder in FontBase (right-click → Refresh)
- Check folder path is correct
- Verify fonts exported successfully
- Restart FontBase if needed

## Performance Notes

### Processing Speed
- **Single font:** 2-3 seconds
- **Small family (5 fonts):** 10-15 seconds
- **Large family (50 fonts):** 2-3 minutes
- **Batch (100 families):** 10-20 minutes

### Disk Space
- Each font generates 3 files (TTF, OTF, WOFF2)
- WOFF2 is smallest (~40-60% of TTF)
- Plan for 3x source file size
- Variable fonts same as static (size-wise)

## Advanced Usage

### Custom Destination Per Project
```bash
# Website fonts
uv run python -m hole_fonts.cli export Input/WebFonts/ \
    --to ~/WebProjects/2025/fonts/ \
    --formats woff2

# Print project fonts
uv run python -m hole_fonts.cli export Input/PrintFonts/ \
    --to ~/PrintProjects/fonts/ \
    --formats otf
```

### Selective Format Conversion
```bash
# Desktop only (no web)
uv run python -m hole_fonts.cli export Input/DesktopFonts/ \
    --formats ttf otf

# Web only
uv run python -m hole_fonts.cli export Input/WebFonts/ \
    --formats woff2
```

### Archive Preparation
```bash
# Organized by format for archival
uv run python -m hole_fonts.cli export Input/CompleteLibrary/ \
    --structure format-separated \
    --to Archive/HOLE-Fonts-$(date +%Y%m%d)/
```

## Integration with Other Tools

### With Figma
1. Export fonts from HOLE Fonts
2. Upload to Figma project
3. Use in designs
4. Font metadata preserved

### With Adobe CC
1. Export to FontBase-Export/
2. Activate in FontBase
3. Available in Photoshop, Illustrator, InDesign
4. Deactivate when project done

### With Web Projects
1. Export WOFF2 to project directory
2. Generate CSS @font-face rules (manual or v0.2 feature)
3. Deploy with website
4. Optimal web font delivery

## Examples by User Intent

### "I just downloaded some fonts"
```bash
uv run python -m hole_fonts.cli export ~/Downloads/NewFonts/
```

### "I need web fonts for my project"
```bash
uv run python -m hole_fonts.cli export Input/ProjectFonts/ \
    --formats woff2 \
    --to WebProject/public/fonts/
```

### "Convert everything in my Input folder"
```bash
uv run python -m hole_fonts.cli export Input/Organized-Folders/
```

### "I want to check if these are variable fonts"
```bash
# Run export and check logs for 🎨 markers
uv run python -m hole_fonts.cli export Input/Fonts/
# Variable fonts will show: "🎨 Variable font detected: ..."
```

### "Export for archival with organized formats"
```bash
uv run python -m hole_fonts.cli export Input/Archive/ \
    --structure format-separated
```

## Success Indicators

After running this skill, you should see:

✅ **Progress output** with family names
✅ **✓ marks** for successful conversions
✅ **🎨 markers** for variable fonts (with axis info)
✅ **Export summary** with file counts
✅ **Destination path** for FontBase to watch

## Next Steps After Conversion

### If FontBase Not Installed:
1. Download FontBase: https://fontba.se/
2. Install and launch
3. Add FontBase-Export/ folder
4. Enable "Watch for changes"

### If FontBase Already Set Up:
1. Fonts appear automatically (if watching)
2. Create Collections for organization
3. Activate fonts for your project
4. Start designing!

## Related Documentation

- **FONTBASE_SETUP_GUIDE.md** - Complete FontBase setup
- **QUICK_REFERENCE.md** - Command cheat sheet
- **README.md** - Full project documentation

## Notes

- **Processing time:** Varies by collection size (2-3 sec per font)
- **Disk space:** ~3x source file size (3 formats generated)
- **Variable fonts:** Fully supported, all variation data preserved
- **Font families:** Auto-detected from folder names
- **Duplicate prevention:** Use skip-existing flag (default: true)
- **Error logs:** Check hole-fonts.log for detailed information

## Configuration Options

Set defaults in `config.yaml`:

```yaml
export:
  default_path: 'FontBase-Export'  # Default output
  structure: 'flat-by-family'      # Default structure

formats:                            # Default formats
  - ttf
  - otf
  - woff2
```

## Success Metrics

**What good output looks like:**
```
╭─────────────── HOLE Fonts Exporter ───────────────╮
│ Exporting fonts for FontBase                      │
│ Input: Input/Helvetica                            │
│ Export to: FontBase-Export                        │
│ Structure: flat-by-family                         │
│ Formats: ttf, otf, woff2                          │
╰───────────────────────────────────────────────────╯

Found 10 font families

✓ Helvetica
✓ Helvetica-Bold
✓ Helvetica-Italic
...

Export complete!

→ Add this folder to FontBase: FontBase-Export
```

**With variable fonts:**
```
✓ InterVariable 🎨 Variable (wght: 100-900)
```

## When to Use This Skill

Use this skill when you need to:
- ✅ Convert fonts between formats
- ✅ Prepare fonts for web deployment (WOFF2)
- ✅ Organize fonts for FontBase
- ✅ Detect variable fonts in a collection
- ✅ Create font kits with multiple formats
- ✅ Archive font libraries
- ✅ Prepare fonts for client delivery

## When NOT to Use This Skill

Don't use for:
- ❌ Font editing (use FontForge, Glyphs)
- ❌ Font creation (use design tools)
- ❌ Font subsetting (future v0.3 feature)
- ❌ CSS generation (future v0.2 feature)
- ❌ License management (future feature)

## Future Enhancements (v0.2)

Coming soon:
- 🔜 Adobe Typekit metadata integration
- 🔜 Font metadata enrichment (designer, foundry)
- 🔜 Smart duplicate detection
- 🔜 CSS @font-face generation
- 🔜 Search and filtering

## Support

**Issues?**
- Check `hole-fonts.log` for errors
- Review `full-export.log` for batch processing
- Consult FONTBASE_SETUP_GUIDE.md
- Check README.md for troubleshooting

**Questions?**
- See QUICK_REFERENCE.md for commands
- See IMPLEMENTATION_PLAN.md for technical details

---

**HOLE Fonts + FontBase = Professional Font Workflow** ✨
