---
name: convert-fonts
description: Convert fonts to TTF, OTF, and WOFF2 formats and organize into HOLE Font Library
---

# Font Conversion Skill

This skill converts a set of fonts to multiple formats (TTF, OTF, WOFF2) and organizes them into the HOLE Font Library with a structured directory layout.

## What This Does

1. **Converts** fonts between formats:
   - Input: TTF, OTF, WOFF, or WOFF2
   - Output: TTF, OTF, and WOFF2 versions

2. **Organizes** fonts into library structure:
   ```
   Library/
   └── FontFamilyName/
       ├── ttf/
       │   └── *.ttf
       ├── otf/
       │   └── *.otf
       └── woff2/
           └── *.woff2
   ```

3. **Auto-detects** font family names and groups related fonts

4. **Skips** existing fonts by default to avoid duplicates

## Usage Examples

**Convert a single font:**
```bash
uv run hole-fonts convert Input/MyFont.ttf
```

**Convert all fonts in a directory:**
```bash
uv run hole-fonts convert Input/FontCollection/
```

**Convert with custom output:**
```bash
uv run hole-fonts convert Input/fonts/ --output CustomOutput/
```

**Convert specific formats only:**
```bash
uv run hole-fonts convert Input/font.ttf --formats woff2
```

**Overwrite existing files:**
```bash
uv run hole-fonts convert Input/fonts/ --overwrite
```

## Other Commands

**List all fonts in library:**
```bash
uv run hole-fonts list
```

**Show font family details:**
```bash
uv run hole-fonts info AgencyFB
```

**Validate library structure:**
```bash
uv run hole-fonts validate
```

## Configuration

Edit `config.yaml` to customize:
- Library path (with automatic fallback if drive unmounted)
- Default formats to generate
- Parallel processing workers
- Skip existing files behavior

## When to Use This Skill

Use this skill when you need to:
- Prepare fonts for web deployment
- Convert fonts between formats
- Organize a font collection
- Create font kits with multiple formats
- Build a structured font library

## Common Scenarios

**Scenario 1: New font acquisition**
"I just downloaded some fonts in TTF format. Convert them and add to the library."
→ `uv run hole-fonts convert Downloads/new-fonts/`

**Scenario 2: Web project font prep**
"I need WOFF2 versions of all our brand fonts."
→ Fonts are already in library with WOFF2 versions ready to deploy

**Scenario 3: Font inventory**
"What fonts do we have in the library?"
→ `uv run hole-fonts list`

**Scenario 4: Quality check**
"Make sure all fonts have all three formats."
→ `uv run hole-fonts validate`

## Notes

- The converter preserves font metadata and features
- Handles multiple weights/styles automatically
- Logs all operations to `hole-fonts.log`
- Safe: never deletes source files
- Smart: skips re-processing existing fonts
